from uuid import uuid4

from sqlalchemy.sql import func
from sqlalchemy_utils import UUIDType
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    UnicodeText,
    DateTime,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    relationship,
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension
import transaction

DBSession = scoped_session(sessionmaker(
    extension=ZopeTransactionExtension(keep_session=True),
    expire_on_commit=False))
Base = declarative_base()


class TimeStampMixin(object):
    creation_datetime = Column(DateTime, server_default=func.now())
    modified_datetime = Column(DateTime, server_default=func.now())

class CreationMixin():

    id = Column(UUIDType(binary=False), primary_key=True)

    @classmethod
    def add(cls, **kwargs):
        with transaction.manager:
            thing = cls(**kwargs)
            if thing.id is None:
                thing.id = uuid4()
            DBSession.add(thing)
            transaction.commit()
        return thing

    @classmethod
    def get_all(cls):
        with transaction.manager:
            things = DBSession.query(
                cls,
            ).all()
        return things

    @classmethod
    def get_by_id(cls, id):
        with transaction.manager:
            thing = DBSession.query(
                cls,
            ).filter(
                cls.id == id,
            ).first()
        return thing

    @classmethod
    def delete_by_id(cls, id):
        with transaction.manager:
            thing = cls.get_by_id(id)
            if thing is not None:
                DBSession.delete(thing)
            transaction.commit()
        return thing

    @classmethod
    def update_by_id(cls, id, **kwargs):
        with transaction.manager:
            keys = set(cls.__dict__)
            thing = cls.get_by_id(id)
            if thing is not None:
                for k in kwargs:
                    if k in keys:
                        setattr(thing, k, kwargs[k])
                DBSession.add(thing)
                transaction.commit()
        return thing

    @classmethod
    def reqkeys(cls):
        keys = []
        for key in cls.__table__.columns:
            if '__required__' in type(key).__dict__:
                keys.append(str(key).split('.')[1])
        return keys

    def to_dict(self):
        return {
            'id': str(self.id),
            'creation_datetime': str(self.creation_datetime),
        }

class Users(Base, CreationMixin, TimeStampMixin):

    __tablename__ = 'users'
    
    first = Column(UnicodeText, nullable=False)
    last = Column(UnicodeText, nullable=False)
    email = Column(UnicodeText, nullable=False)

    tickets = relationship('Tickets', backref='assignee', lazy='joined')

    def to_dict(self):
        resp = super(Users, self).to_dict()
        #resp.update(
        #
        #)
        return resp

class Projects(Base, CreationMixin, TimeStampMixin):

    __tablename__ = 'projects'

    name = Column(UnicodeText, nullable=False)

    def to_dict(self):
        resp = super(Projects, self).to_dict()
        resp.update(
            name = self.name,
        )
        return resp

class TicketAssignments(Base, CreationMixin, TimeStampMixin):

    __tablename__ = 'ticket_assignments'

    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=False)
    entity_id = Column(Integer, ForeignKey('entities.id'), nullable=False)

class Entities(Base, CreationMixin, TimeStampMixin):

    __tablename__ = 'entities'

    name = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=False)

    tickets = relationship(
        'Tickets',
        secondary=TicketAssignments.__table__,
        backref='entity'
    )

    def to_dict(self):
        resp = super(Entities, self).to_dict()
        resp.update(
            name=self.name,
            description=self.description,
            tickets=[t.to_dict for t in self.tickets],
        )
        return resp

class Tickets(Base, CreationMixin, TimeStampMixin):

    __tablename__ = 'tickets'

    name = Column(UnicodeText, nullable=False)
    priority = Column(UnicodeText, nullable=False)
    label = Column(UnicodeText, nullable=True)
    label_color = Column(UnicodeText, nullable=True)
    assignee_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    parent_ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=True)
    #entity_id = Column(Integer, ForeignKey('entities.id'), nullable=True)

    def to_dict(self):
        resp = super(Ticket, self).to_dict()
        resp.update(
            name=self.name,
            priority=self.priority,
            label=self.label,
            label_color=self.label_color,
            assignee=self.assignee if self.assignee != None else {},
        )
        return resp

class TicketActions(Base, CreationMixin, TimeStampMixin):

    __tablename__ = 'ticket_comments'

    action = Column(UnicodeText, nullable=False)
    contents = Column(UnicodeText, nullable=False)

    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        resp = super(TicketActions, self).to_dict()
        resp.update(
            action=self.action,
            contents=self.contents,
            author=self.author.to_dict()
        )
        return resp

