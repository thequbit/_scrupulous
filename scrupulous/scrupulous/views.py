from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    #DBSession,
    Users,
    Comments,
    Projects,
    ProjectAssignments,
    TaskLabels,
    Tasks,
    TicketLabels,
    TicketPriorities,
    Tickets,
    )

import json
import datetime

@view_config(request_method='GET', route_name='home', renderer='templates/index.mak')
def view_home(request):

    '''
    project_assignments = []
    if 'unique' in request.cookies:
        unique = request.cookies['unique']
        user = Users.get_by_unique(unique)
        if not user is None:
            _pa = ProjectAssignments.get_by_user_id(user.id)
            project_assignments = [pa.to_dict() for pa in _pa]
    resp = {'project_assignments': project_assignments}
    print resp
    return resp
    '''
    return {}

def check_payload(request, keys):

    resp = {'code': 0, 'status': 'Success'}
    payload = None
    #try:
    if True:
        #payload = json.loads(request.POST['payload'])
        payload = json.loads(request.body)
    #except:
    #    resp = {'code': 1, 'status': 'Invalid json payload.'}
    if not payload is None:
        if not all(k in payload for k in keys):
            payload = None
            resp = {'code': 2, 'status': 'Mising keys in dict.'}

    #print "\n\n"
    #print payload
    #print keys
    #print all(k in keys for k in payload)
    #print "\n\n"

    return resp, payload

### Users

@view_config(request_method='GET', route_name='users', renderer='json')
def view_users(request):

    users = Users.get_all()
    return {'code': 0, 'status': 'Success', 'users': [u.to_dict() for u in users]}

@view_config(request_method='POST', route_name='users', renderer='json')
def view_users_create(request):

    keys = ['first', 'last', 'email', 'password', 'user_type_id']
    resp, payload = check_payload(request)
    if not payload is None:
        unique = '{0}-{1}'.format(uuid.uuid4(), uuid.uuid4())
        passsalt = hashlib.sha256(uuid.uuid4()).hexdigest()
        passhash = hashlib.sha256('%s%s' % (payload['password'],passsalt)).hexdigest()
        user = Users.add(
            unique = unique,
            first = payload['unique'],
            last = payload['last'],
            email = payload['email'],
            passsalt = passsalt,
            passhash = passhash,
            user_type_id = payload['user_type_id'],
        )
        resp['user_id'] = user.id
    return resp

@view_config(request_method='PUT', route_name='user', renderer='json')
def view_users_create(request):

    keys = ['first', 'last', 'email', 'password', 'user_type_id']
    resp, payload = check_payload(request)
    if not payload is None:
        #unique = '{0}-{1}'.format(uuid.uuid4(), uuid.uuid4())
        passsalt = hashlib.sha256(uuid.uuid4()).hexdigest()
        passhash = hashlib.sha256('%s%s' % (payload['password'],passsalt)).hexdigest()
        user = Users.get_by_id(request.matchdict['id'])
        #user.unique = unique,
        user.first = payload['unique']
        user.last = payload['last']
        user.email = payload['email']
        user.passsalt = passsalt
        user.passhash = passhash
        user.user_type_id = payload['user_type_id']
        Users.update(user)
    return resp

@view_config(request_method='DELETE', route_name='user', renderer='json')
def view_user_delete(request):

   resp = {'code': 0, 'status': 'Scuccess'}
   user = Users.get_by_id(request.matchdict['id'])
   if user is None:
       resp = {'copde': 1, 'status': 'Invalid project ID'}
   else:
       resp['user'] = user.to_dict()
   return resp


### Projects

@view_config(request_method='GET', route_name='projects', renderer='json')
def view_projects(request):

    resp = {'code': 0, 'status': 'Success'}
    #if 'unique' in request.cookies:
    #    unique = request.cookies['unique']
    #    user = Users.get_by_unique(unique)
    #    if not user is None:
    #        resp = ProjectAssignments.get_by_user_id(user.id)
    resp['projects'] = ProjectAssignments.get_by_user_id(1)
    return resp

@view_config(request_method='POST', route_name='projects', renderer='json')
def view_project_create(request):

    keys = ['name', 'description']
    resp, payload = check_payload(request, keys)
    if not payload is None:
        project = Projects.add(
            name = payload['name'],
            description = payload['description'],
            creation_datetime = datetime.datetime.now(),
            current_number = 0,
            user_id = 1,
        )
        assignment = ProjectAssignments.add(
            user_id = 1,
            project_id = project.id,
        )
        resp['project_id'] = project.id
    return resp

@view_config(request_method='GET', route_name='project', renderer='json')
def view_project(request):

   resp = {'code': 0, 'status': 'Scuccess'}
   project = Projects.get_by_id(request.matchdict['id'])
   if project is None:
       resp = {'copde': 1, 'status': 'Invalid project ID'}
   else:
       resp['project'] = project.to_dict()
   return resp 

@view_config(request_method='PUT', route_name='project', renderer='json')
def view_project_update(request):

    keys = ['name', 'description']
    resp, payload = check_payload(request, keys)
    if not payload is None:
        project = Projects.get_by_id(request.matchdict['id'])
        project.name = payload['name']
        project.description = payload['description']
        Projects.update(project)
    return resp

@view_config(request_method='DELETE', route_name='project', renderer='json')
def view_project_delete(request):
   
    resp = {'code': 0, 'status': 'Success'}
    project_assignment = ProjectAssignments.delete_by_project_id(request.matchdict['id'])
    project = Projects.delete_by_id(request.matchdict['id'])
    if project is None:
        resp = {'code': 1, 'status': 'Invalid Project ID.'}
    return resp

### Project Assignments 

@view_config(request_method='GET', route_name='project_assignments', renderer='json')
def view_project_assignments(request):

    # TODO: implement?

    return {}

@view_config(request_method='POST', route_name='project_assignments', renderer='json')
def view_project_assignments_create(request):

    keys = ['project_id', 'user_id']
    resp, payload = check_payload(request)
    if not payload is None:
        project_assignment = ProjectAssignments.add(
            project_id = payload['project_id'],
            user_id = payload['user_id'],
        )
    return resp

# NOTE: No update for project assignments

@view_config(request_method='DELETE', route_name='project_assignment', renderer='json')
def view_project_assignments_delete(request):

    esp = {'code': 0, 'status': 'Success'}
    project_assignment = ProjectAssignments.delete_by_id(request.matchdict['id'])
    if project_assignment is None:
        resp = {'code': 1, 'status': 'Invalid Project ID.'}
    return resp

### Task Labels

@view_config(request_method='GET', route_name='task_labels', renderer='json')
def view_task_labels(request):

    # TODO: implement?

    return {}

@view_config(request_method='POST', route_name='task_labels', renderer='json')
def view_task_labels_create(request):

    keys = ['label', 'forecolor', 'backcolor']
    resp, payload = check_payload(request, keys)
    if not payload is None:
        task_label = TaskLabels.add(
            label = payload['label'],
            forecolor = payload['forecolor'],
            backcolor = payload['backcolor'],
            project_id = payload['project_id'],
        )
        resp['task_label_id'] = task_label.id
    return resp

@view_config(request_method='PUT', route_name='task_label', renderer='json')
def view_task_label_update(request):

    keys = ['label', 'forecolor', 'backcolor']
    resp, payload = check_payload(request, keys)
    if not payload is None:
        task_label = TaskLabels.get_by_id(request.matchdict['id'])
        task_label.label = payload['label']
        task_label.forecolor = payload['forecolor']
        task_label.backcolor = payload['backcolor']
        task_label.project_id = payload['project_id']
        TaskLabels.update(task_label)
    return resp

@view_config(request_method='DELETE', route_name='task_label', renderer='json')
def view_task_label_delete(request):

    resp = {'code': 0, 'status': 'Success'}
    task_label = TaskLabels.delete_by_id(request.matchdict['id'])
    if task_label is None:
        resp = {'code': 1, 'status': 'Invalid Task ID.'}
    return resp

### Tasks

@view_config(request_method='GET', route_name='tasks', renderer='json')
def view_tasks(request):
    
    # TODO: implement?

    return {}

@view_config(request_method='POST', route_name='tasks', renderer='json')
def view_task_create(request):

    keys = ['title', 'contents', 'due_datetime', 'user_id', 'project_id']
    resp, payload = check_payload(request, keys)
    if not payload is None:
        task = Tasks.add(
            title = payload['title'],
            contents = payload['contents'],
            creation_datetime = datetime.datetime.now(),
            due_datetime = datetime.datetime.strptime(payload['due_datetime'], "%Y-%m-%d"),
            user_id = payload['user_id'],
            project_id = payload['project_id'],
        )
        resp['task_id'] = task.id
    return resp

@view_config(request_method='GET', route_name='task', renderer='json')
def view_tasks(requests):

    resp = {'code': 0, 'status': 'Success'}
    task = Tasks.get_by_id(request.matchdict['id'])
    if task is None:
        resp = {'code': 1, 'status': 'Invalid task ID'}
    else:
        resp['task'] = task.to_dict()
    return resp

@view_config(request_method='PUT', route_name='task', renderer='json')
def view_task_update(request):

    keys = ['title', 'contents', 'due_datetime']
    resp, payload = check_payload(request, keys)
    if not payload is None:
        task = Tasks.get_by_id(request.matchdict['id'])
        task.title = payload['title']
        task.contents = payload['contents']
        task.due_datetime = datetime.datetime.strptime(payload['due_datetime'], "%Y-%m-%d")
        task = Tasks.update(task)
    return resp

@view_config(request_method='DELETE', route_name='task', renderer='json')
def view_task_delete(request):

    resp = {'code': 0, 'status': 'Success'}
    task = Tasks.delete_by_id(request.matchdict['id'])
    if task is None:
        resp = {'code': 1, 'status': 'Invalid Task ID.'}
    return resp

### Ticket Labels

@view_config(request_method='GET', route_name='ticket_labels', renderer='json')
def view_ticket_labels(request):

    # TODO: implement?

    return {}

@view_config(request_method='POST', route_name='ticket_labels', renderer='json')
def view_ticket_labels_create(request):

    keys = ['label', 'forecolor', 'backcolor']
    resp, payload = check_payload(request, keys)
    if not payload is None:
        ticket_label = TicketLabels.add(
            label = payload['label'],
            forecolor = payload['forecolor'],
            backcolor = payload['backcolor'],
            project_id = payload['project_id'],
        )
        resp['ticket_label_id'] = ticket_label.id
    return resp

@view_config(request_method='PUT', route_name='ticket_label', renderer='json')
def view_ticket_label_update(request):

    keys = ['label', 'forecolor', 'backcolor']
    resp, payload = check_payload(request, keys)
    if not payload is None:
        ticket_label = TicketLabels.get_by_id(request.matchdict['id'])
        ticket_label.label = payload['label']
        ticket_label.forecolor = payload['forecolor']
        ticket_label.backcolor = payload['backcolor']
        ticket_label.project_id = payload['project_id']
        TicketLabels.update(ticket_label)
    return resp

@view_config(request_method='DELETE', route_name='ticket_label', renderer='json')
def view_ticket_label_delete(request):

    resp = {'code': 0, 'status': 'Success'}
    ticket_label = TicketLabels.delete_by_id(request.matchdict['id'])
    if ticket_label is None:
        resp = {'code': 1, 'status': 'Invalid Ticket ID.'}
    return resp

### Ticket Priorities

@view_config(request_method='GET', route_name='ticket_priorities', renderer='json')
def view_ticket_prioritys(request):

    # TODO: implement?

    return {}

@view_config(request_method='POST', route_name='ticket_priorities', renderer='json')
def view_ticket_prioritys_create(request):

    keys = ['priority', 'forecolor', 'backcolor']
    resp, payload = check_payload(request, keys)
    if not payload is None:
        ticket_priority = TicketPriorities.add(
            priority = payload['priority'],
            forecolor = payload['forecolor'],
            backcolor = payload['backcolor'],
            project_id = payload['project_id'],
        )
        resp['ticket_priority_id'] = ticket_priority.id
    return resp

@view_config(request_method='PUT', route_name='ticket_priority', renderer='json')
def view_ticket_priority_update(request):

    keys = ['priority', 'forecolor', 'backcolor']
    resp, payload = check_payload(request, keys)
    if not payload is None:
        ticket_priority = TicketPriorities.get_by_id(request.matchdict['id'])
        ticket_priority.priority = payload['priority']
        ticket_priority.forecolor = payload['forecolor']
        ticket_priority.backcolor = payload['backcolor']
        ticket_priority.project_id = payload['project_id']
        TicketPriorities.update(ticket_priority)
    return resp

@view_config(request_method='DELETE', route_name='ticket_priority', renderer='json')
def view_ticket_priority_delete(request):

    resp = {'code': 0, 'status': 'Success'}
    ticket_priority = TicketPriorities.delete_by_id(request.matchdict['id'])
    if ticket_priority is None:
        resp = {'code': 1, 'status': 'Invalid Ticket ID.'}
    return resp

### Ticket Statuses

@view_config(request_method='GET', route_name='ticket_statuses', renderer='json')
def view_ticket_statuss(request):

    # TODO: implement?

    return {}

@view_config(request_method='POST', route_name='ticket_statuses', renderer='json')
def view_ticket_statuss_create(request):

    keys = ['status', 'forecolor', 'backcolor']
    resp, payload = check_payload(request, keys)
    if not payload is None:
        ticket_status = TicketStatuses.add(
            status = payload['status'],
            forecolor = payload['forecolor'],
            backcolor = payload['backcolor'],
            project_id = payload['project_id'],
        )
        resp['ticket_status_id'] = ticket_status.id
    return resp

@view_config(request_method='PUT', route_name='ticket_status', renderer='json')
def view_ticket_status_update(request):

    keys = ['status', 'forecolor', 'backcolor']
    resp, payload = check_payload(request, keys)
    if not payload is None:
        ticket_status = TicketStatuses.get_by_id(request.matchdict['id'])
        ticket_status.status = payload['status']
        ticket_status.forecolor = payload['forecolor']
        ticket_status.backcolor = payload['backcolor']
        ticket_status.project_id = payload['project_id']
        TicketStatuses.update(ticket_status)
    return resp

@view_config(request_method='DELETE', route_name='ticket_status', renderer='json')
def view_ticket_status_delete(request):

    resp = {'code': 0, 'status': 'Success'}
    ticket_status = TicketStatuses.delete_by_id(request.matchdict['id'])
    if ticket_status is None:
        resp = {'code': 1, 'status': 'Invalid Ticket ID.'}
    return resp

### Tickets

@view_config(request_method='GET', route_name='tickets', renderer='json')
def view_tickets(requests):

    #TODO: implement?

    return {}

@view_config(request_method='POST', route_name='tickets', renderer='json')
def view_tickets_create(request):

    keys = ['title', 'contents', 'due_datetime', 'task_id',
            'owner_id', 'assignee_id', 'ticket_label_id',
            'ticket_priority_id', 'ticket_status_id']
    resp, payload = check_payload(request, keys)
    if not payload is None:
        ticket = Tickets.add(
            title = payload['title'],
            contents = payload['contents'],
            creation_datetime = datetime.datetime.now(),
            due_datetime = datetime.datetime.strptime(payload['due_datetime'], "%Y-%m-%d"),
            edited = False,
            task_id = payload['task_id'],
            owner_id = payload['owner_id'],
            assignee_id = payload['assignee_id'],
            ticket_label_id = payload['ticket_label_id'],
            ticket_priority_id = payload['ticket_priority_id'],
            ticket_status_id = payload['ticket_status_id'],
        )
        resp['ticket_id'] = ticket.id
    return resp

@view_config(request_method='PUT', route_name='ticket', renderer='json')
def view_tickets_update(request):

    keys = ['title', 'contents', 'due_datetime', 'task_id',
            'owner_id', 'assignee_id', 'ticket_label_id',
            'ticket_priority_id', 'ticket_status_id']
    resp, payload = check_payload(request, keys)
    if not payload is None:
        ticket = Tickets.get_by_id(request.matchdict['id'])
        ticket.title = payload['title']
        ticket.contents = payload['contents']
        ticket.due_datetime = datetime.datetime.strptime(payload['due_datetime'], "%Y-%m-%d")
        ticket.edited = True
        ticket.task_id = payload['task_id']
        ticket.assignee_id = payload['assignee_id']
        ticket.ticket_label_id = payload['ticket_label_id']
        ticket.ticket_priority_id = payload['ticket_priority_id']
        ticket.ticket_status_id = payload['ticket_status_id']
        Tickets.update(ticket)
    return resp

@view_config(request_method='DELETE', route_name='ticket', renderer='json')
def view_tickets_delete(request):

    resp = {'code': 0, 'status': 'Success'}
    ticket = Tickets.delete_by_id(request.matchdict['id'])
    if ticket is None:
        resp = {'code': 1, 'status': 'Invalid Ticket ID.'}
    return resp

### Comments

@view_config(request_method='GET', route_name='comments', renderer='json')
def view_comments(request):

    # TODO: implement?

    return {}

@view_config(request_method='POST', route_name='comments', renderer='json')
def view_comments_create(request):

    keys = ['contents', 'author_id', 'project_id', 'task_id', 'ticket_id']
    resp, payload = check_payload(request, keys)
    if not payload is None:
        comment = Comments.add(
            contents = payload['contents'],
            creation_datetime = datetime.datetime.now(),
            edited = False,
            author_id = payload['author_id'],
            project_id = payload['project_id'],
            task_id = payload['task_id'],
            ticket_id = payload['ticket_id'],
        )
    return resp

@view_config(request_method='PUT', route_name='comment', renderer='json')
def view_comments_update(request):

    keys = ['contents', 'author_id']
    resp, payload = check_payload(request, keys)
    if not payload is None:
        comment = Comments.get_by_id(request.matchdict['id'])
        contents = payload['contents']
        author_id = payload['author_id'],
        project_id = payload['project_id'],
        task_id = payload['task_id'],
        ticket_id = payload['ticket_id'],
        edited = True
        author_id = author_id
    return resp

@view_config(request_method='DELETE', route_name='comment', renderer='json')
def view_comments_delete(request):

    resp = {'code': 0, 'status': 'Success'}
    comment = Comments.delete_by_id(request.matchdict['id'])
    if comment is None:
        resp = {'code': 1, 'status': 'Invalid Ticket ID.'}
    return resp

