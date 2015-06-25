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


@view_config(route_name='home', renderer='templates/index.mak')
def my_view(request):

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


