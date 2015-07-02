import os
import sys
import transaction

import datetime

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Base,
    Users,
    Comments,
    Projects,
    ProjectAssignments,
    TaskLabels,
    Tasks,
    TicketLabels,
    TicketPriorities,
    TicketStatuses,
    Tickets,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    #with transaction.manager:
    #    model = MyModel(name='one', value=1)
    #    DBSession.add(model)

    user = Users.add(
        #session = DBSession,
        unique = u'1234',
        first = u'test',
        last = u'user',
        email = 'utest_user@example.com',
        pass_salt = u'',
        pass_hash = u'',
    )

    '''
    project = Projects.add(
        #session = DBSession,
        name = u'Test Project',
        description = u'A test project.  For testing.',
        creation_datetime = datetime.datetime.now(),
        user_id = user.id,
    )

    project_assignment = ProjectAssignments.add(
        #session = DBSession,
        project_id = project.id,
        user_id = user.id,
    )

    task_label = TaskLabels.add(
        label = u'High Priority',
        forecolor = u'white',
        backcolor = u'red',
        project_id = project.id,
    )

    task = Tasks.add(
        number = 1,
        title = u'Test Task A',
        contents = u'This is a task that needs to be completed',
        creation_datetime = datetime.datetime.now(),
        due_datetime = datetime.datetime.now() + datetime.timedelta(days=1),
        user_id = user.id,
        project_id = project.id,
        task_label_id = task_label.id,
    )

    ticket_label = TicketLabels.add(
        label = u'Bug',
        forecolor = u'white',
        backcolor = u'orange',
        project_id = project.id,
    )

    ticket_priority = TicketPriorities.add(
        label = u'High',
        value = 100,
        forecolor = u'white',
        backcolor = u'red',
        project_id = project.id,
    )

    ticket_status = TicketStatuses.add(
        label = u'Open',
        description = u'Not closed.',
        value = 1,
    )

    ticket = Tickets.add(
        number = 2,
        title = u'Test Ticket 001',
        contents = u'Do the things.  ***now***.',
        creation_datetime = datetime.datetime.now(),
        due_datetime = datetime.datetime.now() + datetime.timedelta(days=1),
        edited = False,
        task_id = task.id,
        owner_id = user.id,
        assignee_id = None,
        ticket_label_id = ticket_label.id,
        ticket_priority_id = ticket_priority.id,    
        ticket_status_id = ticket_status.id,
    )
    '''
