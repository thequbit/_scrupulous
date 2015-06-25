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
        unique = '1234',
        first = 'test',
        last = 'user',
        email = 'test_user@example.com',
        pass_salt = '',
        pass_hash = '',
    )

    project = Projects.add(
        #session = DBSession,
        name = 'Test Project',
        description = 'A test project.  For testing.',
        creation_datetime = datetime.datetime.now(),
        user_id = user.id,
    )

    project_assignment = ProjectAssignments.add(
        #session = DBSession,
        project_id = project.id,
        user_id = user.id,
    )

    task = Tasks.add(
        number = 1,
        title = 'Test Task A',
        contents = 'This is a task that needs to be completed',
        creation_datetime = datetime.datetime.now(),
        due_datetime = datetime.datetime.now() + datetime.timedelta(days=1),
        user_id = user.id,
        project_id = project.id,
    )

    task_label = TaskLabels.add(
        label = 'High Priority',
        forecolor = 'white',
        backcolor = 'red',
        task_id = task.id,
    )

    ticket = Tickets.add(
        number = 2
        title = 'Test Ticket 001',
        
    )

    ticket_label = TicketLabels.add(
        label = 'High Priority',
        forecolor = 'white',
        backcolor = 'red',
        ticket_id = ticket.id,
    )
