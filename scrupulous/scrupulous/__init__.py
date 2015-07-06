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

    config.add_route('project_assignments', '/project/{project_id}/assignments')
    config.add_route('project_assignment', '/project/{project_id}/assignment/{id}')

    config.add_route('task_labels', '/project/{project_id}/task_labels')
    config.add_route('task_label', '/project/{project_id}/task_label/{id}')

    config.add_route('tasks', '/project/{project_id}/tasks')
    config.add_route('task', '/project/{project_id}/task/{id}')

    config.add_route('ticket_labels', '/project/{project_id}/ticket_labels')
    config.add_route('ticket_label', '/project/{project_id}/ticket_label/{id}')

    config.add_route('ticket_priorities', '/project/{project_id}/ticket_priorities')
    config.add_route('ticket_priority', '/project/{project_id}/ticket_priority/{id}')

    config.add_route('ticket_statuses', '/project/{project_id}/ticket_statuses')
    config.add_route('ticket_status', '/project/{project_id}/ticket_status/{id}')

    config.add_route('tickets', '/project/{project_id}/task/{task_id}/tickets')
    config.add_route('ticket', '/project/{project_id}/task/{task_id}/ticket/{id}')

    config.add_route('comments', '/comments')
    config.add_route('comment', '/comment/{id}')

    config.scan()
    return config.make_wsgi_app()
