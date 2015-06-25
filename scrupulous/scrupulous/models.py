import transaction

from sqlalchemy import text

from sqlalchemy import (
    Column,
    Index,
    ForeignKey,
    Integer,
    Float,
    Text,
    Unicode,
    DateTime,
    Boolean,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension(), expire_on_commit=False)
    )
Base = declarative_base()

class CreationMixin():

    @classmethod
    def add(cls, **kwargs):
        with transaction.manager:
            thing = cls(**kwargs)
            DBSession.add(thing)
            transaction.commit()
        return thing

    @classmethod
    def get_all(cls):
        with transaction.manager:
            things = DBSession.query(
                cls,
            ).all()
            retThings = []
            for t in things:
                retThings.append(t.to_dict())
        return retThings

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
            DBSession.delete(thing)
            transaction.commit()
        return thing

    @classmethod
    def update_by_id(cls, id, *args, **kargs):
        with transaction.manager:
             thing = cls.get_by_id(id)
             # TODO: magic
             DBSession.add(thing)
             transaction.commit()
        return thing

class Users(Base, CreationMixin):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    unique = Column(Unicode)
    first = Column(Unicode)
    last = Column(Unicode)
    email = Column(Unicode)
    pass_salt = Column(Unicode)
    pass_hash = Column(Unicode)

    comments = relationship('Comments', backref='user', lazy='joined')
    projects = relationship('Projects', backref='user', lazy='subquery')
    project_assignments = relationship('ProjectAssignments', backref='user', lazy='joined')

    def to_dict(self):
        return {
            'id': self.id,
            'unique': self.unique,
            'first': self.first,
            'last': self.last,
        }

    @classmethod
    def get_by_unique(self, unique):
        with transaction.manager:
            user = DBSession.query(
                Users,
            ).filter(
                Users.unique == unique,
            ).first()
        return user

    @classmethod
    def auth(self, email, password):
        with transaction.manager:
            user = DBSession.query(
                Users,
            ).filter(
                Users.email == email,
            ).first()
            if not user is None:
                pass_hash = str(hashlib.md5(
                    '%s%s' % (password, user.pass_salt
                )).hexdigest())
                if not user.pass_hash == pass_hash:
                    user = None
        return user

class Comments(Base, CreationMixin):

    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    contents = Column(Unicode)
    creation_datetime = Column(DateTime)
    edited = Column(Boolean)

    user_id = Column(Integer, ForeignKey('users.id'))

    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'contents': self.contents,
            'creation_datetime': str(self.creation_datetime),
            'edited': self.edited,
            'user': self.user.to_dict(),
        }

class Projects(Base, CreationMixin):

    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    description = Column(Unicode)
    creation_datetime = Column(DateTime)
    current_number = Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'))
    
    comments = relationship('Comments', backref='project', lazy='joined')
    project_assignments = relationship('ProjectAssignments', backref='project', lazy='joined')
    tasks = relationship('Tasks', backref='task', lazy='joined')

    def to_dict(self):
        print '\n\nUser ID: {0}\n\n'.format(self.user_id)
        return {
            'id': self.id,
             'name': self.name,
             'description': self.description,
             'creation_datetime': str(self.creation_datetime),
             'user': Users.get_by_id(self.user_id).to_dict(), #self.user.to_dict(), # backref
             'comments': [c.to_dict() for c in self.comments],
             'tasks': [t.to_dict() for t in self.tasks],
        }

class ProjectAssignments(Base, CreationMixin):

    __tablename__ = 'project_assignments'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'project': Projects.get_by_id(self.project_id).to_dict(),
            'user': Users.get_by_id(self.user_id).to_dict(),
        }

    @classmethod
    def get_by_user_id(self, user_id):
        with transaction.manager:
            project_assignments = DBSession.query(
                ProjectAssignments,
            ).filter(
                ProjectAssignments.user_id == user_id,
            ).all()
        return project_assignments

class TaskLabels(Base, CreationMixin):

    __tablename__ = 'task_labels'

    id = Column(Integer, primary_key=True)
    label = Column(Unicode)
    forecolor = Column(Unicode)
    backcolor = Column(Unicode)

    #tasks = relationship('Tasks', backref='task_label', lazy='joined')
    task_id = Column(Integer, ForeignKey('tasks.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'forecolor': self.forecolor,
            'backcolor': self.backcolor,
        }

class Tasks(Base, CreationMixin):

    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    title = Column(Unicode)
    contents = Column(Unicode)
    creation_datetime = Column(DateTime)
    due_datetime = Column(Unicode)

    user_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))

    labels = relationship('TaskLabels', backref='task', lazy='joined')
    comments = relationship('Comments', backref='task', lazy='joined')
    tickets = relationship('Tickets', backref='task', lazy='joined')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'contents': self.contents,
            'creation_datetime': str(self.creation_datetime),
            'due_datetime': str(self.due_datetime),
            'user': self.user.to_dict(), # backref
            'labels': [l.to_dict() for l in self.labels],
            'comments': [c.to_dict() for c in self.comments],
            'tickets': [t.to_dict() for t in self.tickets],
        }

class TicketLabels(Base, CreationMixin):

    __tablename__ = 'ticket_labels'
    
    id = Column(Integer, primary_key=True)
    label = Column(Unicode)
    forecolor = Column(Unicode)
    backcolor = Column(Unicode)

    #ticket_id = Column(Integer, ForeignKey('tickets.id'))
    tickets = relationship('Tickets', backref='ticket_label', lazy='joined')

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.lable,
            'forecolor': self.forecolor,
            'backcolor': self.backcolor,
        }

class TicketPriorities(Base, CreationMixin):

    __tablename__ = 'ticket_priorities'

    id = Column(Integer, primary_key=True)
    label = Column(Unicode)
    value = Column(Integer)
    forecolor = Column(Unicode)
    backcolor = Column(Unicode)

    #ticket_id = Column(Integer, ForeignKey('tickets.id'))
    tickets = relationship('Tickets', backref='ticket_priority', lazy='joined')

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.lable,
            'forecolor': self.forecolor,
            'backcolor': self.backcolor,
        }

class Tickets(Base, CreationMixin):

    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    title = Column(Unicode)
    contents = Column(Unicode)
    creation_datetime = Column(DateTime)
    due_datetime = Column(DateTime)
    edited = Column(Boolean)

    task_id = Column(Integer, ForeignKey('tasks.id'))

    ticket_label_id = Column(Integer, ForeignKey('ticket_labels.id'), nullable=True)
    ticket_priority_id = Column(Integer, ForeignKey('ticket_priorities.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'contents': self.contents,
            'creation_datetime': str(self.creation_datetime),
            'due_datetime': str(self.due_datetime),
            'edited': self.edited,
            'label': self.label.to_dict(),
            'priority': self.priority.to_dict(),
        }

