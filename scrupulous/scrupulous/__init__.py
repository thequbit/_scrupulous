from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')

    config.add_route('users', '/users')
    config.add_route('user', '/user/{id}')

    config.add_route('projects', '/projects')
    config.add_route('project', '/project/{id}')

    config.add_route('project_assignments', '/project_assignments')
    config.add_route('project_assignment', '/project_assignment/{id}')

    config.add_route('task_labels', '/task_labels')
    config.add_route('task_label', '/task_label/{id}')

    config.add_route('tasks', '/tasks')
    config.add_route('task', '/task/{id}')

    config.add_route('ticket_labels', '/ticket_labels')
    config.add_route('ticket_label', '/ticket_label/{id}')

    config.add_route('ticket_priorities', '/ticket_priorities')
    config.add_route('ticket_priority', '/ticket_priority/{id}')

    config.add_route('ticket_statuses', '/ticket_statuses')
    config.add_route('ticket_status', '/ticket_status/{id}')

    config.add_route('tickets', '/tickets')
    config.add_route('ticket', '/ticket/{id}')

    config.add_route('comments', '/comments')
    config.add_route('comment', '/comment/{id}')

    config.scan()
    return config.make_wsgi_app()
