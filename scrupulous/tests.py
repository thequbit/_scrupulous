import requests
import json
import datetime

BASE_URL = 'http://127.0.0.1:6543'

projects_url = '%s/projects' % BASE_URL
project_url = '%s/project' % BASE_URL

tasks_url = '%s/tasks' % BASE_URL
task_url = '%s/task' % BASE_URL

tickets_url = '%s/tickets' % BASE_URL
ticket_url = '%s/ticket' % BASE_URL

def now(td=0):
    return str(datetime.datetime.now()+datetime.timedelta(days=td)).split(' ')[0]

# POST
def create(url, payload):

    resp = requests.post(url, data=json.dumps(payload))
    return json.loads(resp.text)

# GET
def read(url):

    resp = requests.get(url)
    return json.loads(resp.text)

# PUT
def update(url, payload):

    resp = requests.put(url, data=json.dumps(payload))
    return json.loads(resp.text)

# DELETE
def delete(url):

    resp = requests.delete(url)
    return json.loads(resp.text)

def check_resp(resp):
    if not resp['code'] is 0:
        raise Exception('Bad response: {0}'.format(resp))
    return resp

def test_projects():

    print 'Testing Projects CRUD ...'

    project = {
        'name': 'Test Project 001',
        'description': 'Mah Test Project ... 1.',
    }
    resp = check_resp(create(projects_url, project))

    resp = check_resp(read(projects_url))
    projects = resp['projects']

    if len(projects) is 0:
        raise Exception('Project was not created.')

    if not projects[0]['project']['name'] == project['name'] or \
            not projects[0]['project']['description'] == project['description']:
        raise Exception('Project was not corrected with correct data.')

    project_id = projects[0]['id']

    new_project = {
        'name': 'Test Project 001 - Updated',
        'description': 'Mah Test Project ... 1 ... Updated!',
    }
    resp = check_resp(update('%s/%i' % (project_url, project_id), new_project))

    resp = read(projects_url)
    projects = resp['projects']    

    if not projects[0]['project']['name'] == new_project['name'] or \
            not projects[0]['project']['description'] == new_project['description']:
        raise Exception('Project not updated.')

    resp = delete('%s/%i' %(project_url, project_id))

    resp = read(projects_url)

    if not len(resp['projects']) is 0:
        raise Exception('Project not deleted')

    resp = check_resp(create(projects_url, {
        'name': 'Test Project 001',
        'description': 'Mah Test Project ... 1.',
    }))
    resp = check_resp(read(projects_url))
    projects = resp['projects']

    if not len(projects) is 1:
        raise Exception('Test Project not created.')

    print "Done.\n"

    return projects[0]['project']

def get_tasks():

    resp = check_resp(read(projects_url))
    projects = resp['projects']
    tasks = []
    for project in projects:
        for task in project['project']['tasks']:
            tasks.append(task)
    return tasks

def test_tasks(project):

    print "Testing Tasks CRUD ..."

    task = {
        'title': 'Test Task',
        'contents': 'Do things.  All of them.',
        'due_datetime': now(10),
        'user_id': 1,
        'project_id': project['id'],
    }
    resp = check_resp(create(tasks_url, task))

    tasks = get_tasks()

    if len(tasks) is 0:
        raise Exception('Task not created.')

    task_id = tasks[0]['id']

    if not tasks[0]['title'] == task['title'] or \
            not tasks[0]['contents'] == task['contents'] or \
            not tasks[0]['due_datetime'] == task['due_datetime'] or \
            not tasks[0]['owner']['id'] == task['user_id']: # or \
            #not tasks[0]['project_id'] == task['project_id']:
        print get_tickets()
        raise Exception('Task not created successfully.')

    new_task = {
        'title': 'Test Ticket - Updated',
        'contents': 'Do things.  All of them. MEOW!',
        'due_datetime': now(5),
        'user_id': 1,
        'project_id': project['id'],

    }
    resp = check_resp(update('%s/%i' % (task_url, task_id), new_task))

    tasks = get_tasks()

    if not tasks[0]['title'] == new_task['title'] or \
            not tasks[0]['contents'] == new_task['contents'] or \
            not tasks[0]['due_datetime'] == new_task['due_datetime'] or \
            not tasks[0]['owner']['id'] == new_task['user_id']: # or \
            #not tasks[0]['project_id'] == task['project_id']:
        raise Exception('Task not updated successfully.')

    resp = check_resp(delete('%s/%i' % (task_url, task_id)))

    tasks = get_tasks()

    if not len(tasks) is 0:
        raise Exception('Task not deleted.')

    resp = check_resp(create(tasks_url, task))

    task = get_tasks()[0]

    print 'Done.\n'

    return task

def get_tickets():

    resp = check_resp(read(projects_url))
    projects = resp['projects']
    tickets = []
    for project in projects:
        for task in project['project']['tasks']:
            for ticket in task['tickets']:
                tickets.append(ticket)
    return tickets

def test_tickets(task):

    print "Testing Tickets CRUD ..."

    ticket = {
        'title': 'Test ticket',
        'contents': 'Fix all the things!',
        'due_datetime': now(10),
        'edited': False,
        'task_id': task['id'],
        'owner_id': 1,
        'assignee_id': 1,
        'ticket_label_id': None,
        'ticket_priority_id': None,
        'ticket_status_id': None,
    }
    resp = check_resp(create(tickets_url, ticket))

    tickets = get_tickets()

    if len(tickets) is 0:
        raise Exception('ticket not created.')

    ticket_id = tickets[0]['id']

    if not tickets[0]['title'] == ticket['title'] or \
            not tickets[0]['contents'] == ticket['contents'] or \
            not tickets[0]['due_datetime'] == ticket['due_datetime'] or \
            not tickets[0]['owner']['id'] == ticket['owner_id'] or \
            not tickets[0]['assignee']['id'] == ticket['assignee_id']: #or \
        print get_tickets()
        raise Exception('ticket not created successfully.')

    new_ticket = {
        'title': 'Test ticket - Updated!',
        'contents': 'Fix all the things! Like ... yesterday.',
        'due_datetime': now(5),
        'edited': False,
        'task_id': task['id'],
        'owner_id': 1,
        'assignee_id': 1,
        'ticket_label_id': None,
        'ticket_priority_id': None,
        'ticket_status_id': None,
    }
    resp = check_resp(update('%s/%i' % (ticket_url, ticket_id), new_ticket))

    tickets = get_tickets()

    if not tickets[0]['title'] == new_ticket['title'] or \
            not tickets[0]['contents'] == new_ticket['contents'] or \
            not tickets[0]['due_datetime'] == new_ticket['due_datetime'] or \
            not tickets[0]['owner']['id'] == new_ticket['owner_id'] or \
            not tickets[0]['assignee']['id'] == new_ticket['assignee_id']: #or \
        raise Exception('Ticket not updated successfully.')
    resp = check_resp(delete('%s/%i' % (ticket_url, ticket_id)))

    tickets = get_tickets()

    if not len(tickets) is 0:
        raise Exception('ticket not deleted.')

    resp = check_resp(create(tickets_url, ticket))

    ticket = get_tickets()[0]

    print 'Done.\n'

if __name__ == '__main__':

    project = test_projects()

    task = test_tasks(project)

    ticket = test_tickets(task)

    print "\n"

    resp = check_resp(read(projects_url))
    projects = resp['projects']
    print json.dumps(projects)

    print "\nDone"
