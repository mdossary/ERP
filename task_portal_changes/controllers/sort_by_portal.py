
from collections import OrderedDict
from operator import itemgetter
from markupsafe import Markup

from odoo import conf, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem

from odoo.osv.expression import OR, AND


class ProjectCustomerPortal(CustomerPortal):
    def _prepare_tasks_values(self, page, date_begin, date_end, sortby, search, search_in, groupby, url="/my/tasks", domain=None, su=False):
        values = self._prepare_portal_layout_values()

        Task = request.env['project.task']
        milestone_domain = AND([domain, [('allow_milestones', '=', 'True')]])
        milestones_allowed = Task.sudo().search_count(milestone_domain, limit=1) == 1
        searchbar_sortings = dict(sorted(self._task_get_searchbar_sortings(milestones_allowed).items(),
                                         key=lambda item: item[1]["sequence"]))
        searchbar_inputs = self._task_get_searchbar_inputs(milestones_allowed)
        searchbar_groupby = self._task_get_searchbar_groupby(milestones_allowed)

        if not domain:
            domain = []
        if not su and Task.check_access_rights('read'):
            domain = AND([domain, request.env['ir.rule']._compute_domain(Task._name, 'read')])
        Task_sudo = Task.sudo()

        # default sort by value
        if not sortby or (sortby == 'milestone' and not milestones_allowed):
            sortby = 'name'
        order = searchbar_sortings[sortby]['order']

        # default group by value
        if not groupby or (groupby == 'milestone' and not milestones_allowed):
            groupby = 'project'

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search reset if needed
        if not milestones_allowed and search_in == 'milestone':
            search_in = 'all'
        # search
        if search and search_in:
            domain += self._task_get_search_domain(search_in, search)

        # content according to pager and archive selected
        order = self._task_get_order(order, groupby)

        def get_grouped_tasks(pager_offset):
            tasks = Task_sudo.search(domain, order=order, limit=self._items_per_page, offset=pager_offset)
            request.session['my_project_tasks_history' if url.startswith('/my/projects') else 'my_tasks_history'] = tasks.ids[:100]

            tasks_project_allow_milestone = tasks.filtered(lambda t: t.allow_milestones)
            tasks_no_milestone = tasks - tasks_project_allow_milestone

            groupby_mapping = self._task_get_groupby_mapping()
            group = groupby_mapping.get(groupby)
            if group:
                if group == 'milestone_id':
                    grouped_tasks = [Task_sudo.concat(*g) for k, g in groupbyelem(tasks_project_allow_milestone, itemgetter(group))]

                    if not grouped_tasks:
                        grouped_tasks = [tasks_no_milestone]
                    else:
                        if grouped_tasks[len(grouped_tasks) - 1][0].milestone_id and tasks_no_milestone:
                            grouped_tasks.append(tasks_no_milestone)
                        else:
                            grouped_tasks[len(grouped_tasks) - 1] |= tasks_no_milestone

                else:
                    grouped_tasks = [Task_sudo.concat(*g) for k, g in groupbyelem(tasks, itemgetter(group))]
            else:
                grouped_tasks = [tasks]

            task_states = dict(Task_sudo._fields['kanban_state']._description_selection(request.env))
            if sortby == 'status':
                if groupby == 'none' and grouped_tasks:
                    grouped_tasks[0] = grouped_tasks[0].sorted(lambda tasks: task_states.get(tasks.kanban_state))
                else:
                    grouped_tasks.sort(key=lambda tasks: task_states.get(tasks[0].kanban_state))
            return grouped_tasks

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_tasks': get_grouped_tasks,
            'allow_milestone': milestones_allowed,
            'page_name': 'task',
            'default_url': url,
            'task_url': 'tasks',
            'pager': {
                "url": url,
                "url_args": {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'groupby': groupby, 'search_in': search_in, 'search': search},
                "total": Task_sudo.search_count(domain),
                "page": page,
                "step": self._items_per_page
            },
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'groupby': groupby,
        })
        return values
