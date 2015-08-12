import logging
import json
import datetime

#from pyramid.response import Response
#from pyramid.view import view_config

#from sqlalchemy.exc import DBAPIError

from cornice import Service
from cornice.schemas import validate_colander_schema
from cornice.resource import resource, view

from .models import (
    DBSession,
    Users,
    Projects,
    Entities,
    Tickets,
    TicketAssignments,
    TicketActions,
    )

from .validators import validator_from_model

log = logging.getLogger(name='scrupulous.{}'.format(__name__))

class ResourceMixin(object):
    cls = None

    def __init__(self, request):
        self.request = request

    @property
    def rsrc(self):
        return self.cls.__name__.lower()

    def validate_req(self, request):
        validate_colander_schema(validator_from_model(self.cls), request)

    def collection_get(self):
        log.debug("collection_get on {}".format(self.rsrc))
        return {
            self.rsrc: [i.to_dict() for i in self.cls.get_all()]
        }

    @view(content_type="application/json", validators=('validate_req', ))
    def collection_post(self):
        log.debug("collection_post on {} with {}".format(
            self.rsrc, json.dumps(self.request.validated)))
        self.request.validated['creation_datetime'] = datetime.datetime.now()
        item = self.cls.add(**self.request.validated)
        self.request.response.status = 201
        return item.to_dict()

    def get(self):
        item = self.cls.get_by_id(self.request.matchdict['id'])
        if item is None:
            self.request.response.status = 404
            return {'error': 'Not found'}
        return item.to_dict()

    @view(content_type="application/json", validators=('validate_req', ))
    def put(self):
        item = self.cls.update_by_id(
            self.request.matchdict['id'],
            **self.request.validated)

        if item is None:
            self.request.response.status = 404
            return {'error': 'Not found'}

        self.request.response.status = 201
        return item.to_dict()

    def delete(self):
        item = self.cls.delete_by_id(self.request.matchdict['id'])
        if item is None:
            self.request.response.status = 404
            return {'error': 'Not found'}
        return item.to_dict()

@resource(collection_path='/users', path='/users/{id}')
class UsersResource(ResourceMixin):
    """
    [GET, POST             ] /users
    [GET,       PUT, DELETE] /users/:{id}
    """
    cls = Users

@resource(collection_path='/projects', path='/projects/{id}')
class ProjectssResource(ResourceMixin):
    """
    [GET, POST             ] /projects
    [GET,       PUT, DELETE] /projects/:{id}
    """
    cls = Projects

@resource(collection_path='/entities', path='/entities/{id}')
class EntitiesResource(ResourceMixin):
    """
    [GET, POST             ] /entities
    [GET,       PUT, DELETE] /entities/:{id}
    """
    cls = Entities

@resource(collection_path='/tickets', path='/tickets/{id}')
class TicketsResource(ResourceMixin):
    """
    [GET, POST             ] /tickets
    [GET,       PUT, DELETE] /tickets/:{id}
    """
    cls = Tickets

@resource(collection_path='/ticket_actions', path='/ticket_actions/{id}')
class TicketActionsResource(ResourceMixin):
    """
    [GET, POST             ] /ticket_actions
    [GET,       PUT, DELETE] /ticket_actions/:{id}
    """
    cls = Users

