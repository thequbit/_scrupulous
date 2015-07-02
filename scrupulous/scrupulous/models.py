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
            thing = DBSession.query(
                cls,
            ).filter(
                cls.id == id,
            ).first()
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

    @classmethod
    def update(cls, thing):
        with transaction.manager:
            DBSession.add(thing)
            transaction.commit()
        return thing

class UserTypes(Base, CreationMixin):

    __tablename__ = 'user_types'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    description = Column(Unicode)

    users = relationship('Users', backref='user_type', lazy='joined')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }

class Users(Base, CreationMixin):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    unique = Column(Unicode)
    first = Column(Unicode)
    last = Column(Unicode)
    email = Column(Unicode)
    pass_salt = Column(Unicode)
    pass_hash = Column(Unicode)

    user_type_id = Column(Integer, ForeignKey('user_types.id'))

    comments = relationship('Comments', backref='user', lazy='joined')
    projects = relationship('Projects', backref='user', lazy='joined')
    project_assignments = relationship('ProjectAssignments', backref='user', lazy='joined')
    tasks = relationship('Tasks', backref='user', lazy='joined')
    tickets_owned = relationship('Tickets', backref='owner', lazy='joined', foreign_keys='Tickets.owner_id')
    tickets_assigned = relationship('Tickets', backref='assignee', lazy='joined', foreign_keys='Tickets.assignee_id')

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

    author_id = Column(Integer, ForeignKey('users.id'))

    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'contents': self.contents,
            'creation_datetime': str(self.creation_datetime).split(' ')[0],
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
    #project_assignments = relationship('ProjectAssignments', backref='project', lazy='joined')
    task_labels = relationship('TaskLabels', backref='project', lazy='joined')
    tasks = relationship('Tasks', backref='project', lazy='joined')
    ticket_labels = relationship('TicketLabels', backref='project', lazy='joined')
    ticket_priorities = relationship('TicketPriorities', backref='project', lazy='joined')
    ticket_statuses = relationship('TicketStatuses', backref='project', lazy='joined')
    assignees = relationship('ProjectAssignments', backref='project', lazy='joined')

    def to_dict(self):
        return {
             'id': self.id,
             'name': self.name,
             'description': self.description,
             'creation_datetime': str(self.creation_datetime).split(' ')[0],
             'owner': self.user.to_dict(), #self.user.to_dict(), # backref
             'comments': [c.to_dict() for c in self.comments],
             'task_labels': [l.to_dict() for l in self.task_labels],
             'tasks': [t.to_dict() for t in self.tasks],
             'ticket_labels': [t.to_dict() for t in self.ticket_labels],
             'ticket_priorities': [t.to_dict() for t in self.ticket_priorities],
             'ticket_statuses': [t.to_dict() for t in self.ticket_statuses],
             'users': [a.user.to_dict() for a in self.assignees],
        }

class ProjectAssignments(Base, CreationMixin):

    __tablename__ = 'project_assignments'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'project': self.project.to_dict(), #Projects.get_by_id(self.project_id).to_dict(),
            'user': self.user.to_dict(), #Users.get_by_id(self.user_id).to_dict(),
        }

    @classmethod
    def get_by_user_id(cls, user_id):
        with transaction.manager:
            resp = DBSession.query(
                cls,
            ).filter(
                cls.user_id == user_id,
            ).all()
            project_assignments = []
            for pa in resp:
                project_assignments.append(pa.to_dict())
        return project_assignments

    @classmethod
    def delete_by_project_id(cls, project_id):
        with transaction.manager:
            project_assignments = DBSession.query(
                ProjectAssignments,
            ).filter(
                ProjectAssignments.project_id == int(project_id),
            ).all()
        for project_assignment in project_assignments:
            ProjectAssignments.delete_by_id(project_assignment.id)
        return project_assignments

class TaskLabels(Base, CreationMixin):

    __tablename__ = 'task_labels'

    id = Column(Integer, primary_key=True)
    label = Column(Unicode)
    forecolor = Column(Unicode)
    backcolor = Column(Unicode)

    project_id = Column(Integer, ForeignKey('projects.id'))

    #tasks = relationship('Tasks', backref='task_label', lazy='joined')
    #task_id = Column(Integer, ForeignKey('tasks.id'))

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

    task_label_id = Column(Integer, ForeignKey('task_labels.id'))

    label = relationship('TaskLabels', backref='task', lazy='joined')
    comments = relationship('Comments', backref='task', lazy='joined')
    tickets = relationship('Tickets', backref='task', lazy='joined')

    def to_dict(self):
        label = None
        if not self.label is None:
            label = self.label.to_dict()
        return {
            'id': self.id,
            'title': self.title,
            'contents': self.contents,
            'creation_datetime': str(self.creation_datetime).split(' ')[0],
            'due_datetime': str(self.due_datetime).split(' ')[0],
            'owner': self.user.to_dict(), # backref
            'label': label,
            'comments': [c.to_dict() for c in self.comments],
            'tickets': [t.to_dict() for t in self.tickets],
        }

class TicketLabels(Base, CreationMixin):

    __tablename__ = 'ticket_labels'
    
    id = Column(Integer, primary_key=True)
    label = Column(Unicode)
    forecolor = Column(Unicode)
    backcolor = Column(Unicode)

    project_id = Column(Integer, ForeignKey('projects.id'))

    #ticket_id = Column(Integer, ForeignKey('tickets.id'))
    tickets = relationship('Tickets', backref='ticket_label', lazy='joined')

    def to_dict(self):
        resp = {
            'id': self.id,
            'label': self.label,
            'forecolor': self.forecolor,
            'backcolor': self.backcolor,
        }
        return resp

class TicketPriorities(Base, CreationMixin):

    __tablename__ = 'ticket_priorities'

    id = Column(Integer, primary_key=True)
    label = Column(Unicode)
    value = Column(Integer)
    forecolor = Column(Unicode)
    backcolor = Column(Unicode)

    project_id = Column(Integer, ForeignKey('projects.id'))

    #ticket_id = Column(Integer, ForeignKey('tickets.id'))
    tickets = relationship('Tickets', backref='ticket_priority', lazy='joined')

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'value': self.value,
            'forecolor': self.forecolor,
            'backcolor': self.backcolor,
        }

class TicketStatuses(Base, CreationMixin):

    __tablename__ = 'ticket_statuses'

    id = Column(Integer, primary_key=True)
    label = Column(Unicode)
    description = Column(Unicode)
    value = Column(Integer)

    project_id = Column(Integer, ForeignKey('projects.id'))

    tickets = relationship('Tickets', backref='ticket_status', lazy='joined')

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'description': self.description,
            'value': self.value,
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
    #project_id = Column(Integer, ForeignKey('projects.id'))

    owner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    assignee_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    #owner = relationship(Users, foreign_keys=owner_id)
    #assignee = relationship(Users, foreign_keys=assignee_id)

    ticket_label_id = Column(Integer, ForeignKey('ticket_labels.id'), nullable=True)
    ticket_priority_id = Column(Integer, ForeignKey('ticket_priorities.id'), nullable=True)
    ticket_status_id = Column(Integer, ForeignKey('ticket_statuses.id'), nullable=True)

    def to_dict(self):
        assignee = {}
        if not self.assignee is None:
            assignee = self.assignee.to_dict()
        ticket_label = {}
        if not self.ticket_label is None:
            ticket_label = self.ticket_label.to_dict()
        ticket_priority = {}
        if not self.ticket_priority is None:
            ticket_priority = self.ticket_priority.to_dict()
        ticket_status = {}
        if not self.ticket_status is None:
            ticket_status = self.ticket_status.to_dict()
        resp = {
            'id': self.id,
            'title': self.title,
            'contents': self.contents,
            'creation_datetime': str(self.creation_datetime).split(' ')[0],
            'due_datetime': str(self.due_datetime).split(' ')[0],
            'edited': self.edited,
            'owner': self.owner.to_dict(),
            'assignee': assignee,
            'label': ticket_label,
            'priority': ticket_priority,
            'status': ticket_status,
        }

        return resp

