function _get(target, callback) {
    $.ajax({
        type: 'GET',
        url: '/' + target,
        contentType: 'application/json',
        dataType: 'json',
        success: function(data) {
            callback(data);
        }
    });
}

function _create(target, callback, payload) {
    $.ajax({
        type: 'POST',
        url: '/' + target,
        data: JSON.stringify(payload),
        contentType: 'application/json',
        dataType: 'json',
        success: function(data) {
            callback(data);
        },
    });
}

function _update(target, callback, id, payload) {
    $.ajax({
        type: 'PUT',
        url: '/' + target + '/' + id,
        data: JSON.stringify(payload),
        contentType: 'application/json',
        dataType: 'json',
        success: function(data) {
            callback(data);
        },
    });
}

function _delete(target, callback, id) {
    $.ajax({
        type: 'DELETE',
        url: '/' + target + '/' + id,
        contentType: 'application/json',
        dataType: 'json',
        success: function(data) {
            callback(data);
        }
    });
}

/* User */
function _get_users(callback) {
    _get('users', callback);
}
function _create_user(callback, payload) {
    _create('users', callback, payload);
}
function _update_user(callback, id, payload) {
    _update('user', callback, id, payload);
}
function _delete_user(callback, id) {
    _delete('user', callback, id);
}

/* Project */
function _get_projects(callback) {
    _get('projects', callback);
}
function _create_project(callback, payload) {
    _create('projects', callback, payload);
}
function _update_project(callback, id, payload) {
    _update('project', callback, id, payload);
}
function _delete_project(callback, id) {
    _delete('project', callback, id);
}

/* Project Assignment */
function _get_project_assignments(callback) {
    _get('project_assignments', callback);
}
function _create_project_assignment(callback, payload) {
    _create('projects_assignment', callback, payload);
}
function _update_project_assignment(callback, id, payload) {
    _update('project_assignment', callback, id, payload);
}
function _delete_project_assignment(callback, id) {
    _delete('project_assignment', callback, id);
}


/* Task Label */
function _get_task_labels(callback) {
    _get('task_labels', callback);
}
function _create_task_label(callback, payload) {
    _create('task_labels', callback, payload);
}
function _update_task_label(callback, id, payload) {
    _update('task_label', callback, id, payload);
}
function _delete_task_label(callback, id) {
    _delete('task_label', callback, id);
}

/* Task */
function _get_tasks(callback) {
    _get('tasks', callback);
}
function _create_task(callback, payload) {
    _create('tasks', callback, payload);
}
function _update_task(callback, id, payload) {
    _update('task', callback, id, payload);
}
function _delete_task(callback, id) {
    _delete('task', callback, id);
}

/* Ticket Label */
function _get_ticket_labels(callback) {
    _get('ticket_labels', callback);
}
function _create_ticket_label(callback, payload) {
    _create('ticket_labels', callback, payload);
}
function _update_ticket_label(callback, id, payload) {
    _update('ticket_label', callback, id, payload);
}
function _delete_ticket_label(callback, id) {
    _delete('ticket_label', callback, id);
}

/* Ticket Priority */
function _get_ticket_priorities(callback) {
    _get('ticket_priorities', callback);
}
function _create_ticket_priority(callback, payload) {
    _create('ticket_priorites', callback, payload);
}
function _update_ticket_priority(callback, id, payload) {
    _update('ticket_priority', callback, id, payload);
}
function _delete_ticket_priority(callback, id) {
    _delete('ticket_priority', callback, id);
}

/* Ticket Status */
function _get_ticket_statuses(callback) {
    _get('ticket_statuses', callback);
}
function _create_ticket_status(callback, payload) {
    _create('ticket_statuses', callback, payload);
}
function _update_ticket_status(callback, id, payload) {
    _update('ticket_status', callback, id, payload);
}
function _delete_ticket_status(callback, id) {
    _delete('ticket_status', callback, id);
}

/* Ticket */
function _get_tickets(callback) {
    _get('tickets', callback);
}
function _create_ticket(callback, payload) {
    _create('tickets', callback, payload);
}
function _update_ticket(callback, id, payload) {
    _update('ticket', callback, id, payload);
}
function _delete_ticket(callback, id) {
    _delete('ticket', callback, id);
}

/* Comment */
function _get_comments(callback) {
    _get('comments', callback);
}
function _create_comment(callback, payload) {
    _create('comments', callback, payload);
}
function _update_comment(callback, id, payload) {
    _update('comment', callback, id, payload);
}
function _delete_comment(callback, id) {
    _delete('comment', callback, id);
}

