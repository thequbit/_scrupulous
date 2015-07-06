function _get(url, callback) {
    $.ajax({
        type: 'GET',
        url: url,
        contentType: 'application/json',
        dataType: 'json',
        success: function(data) {
            callback(data);
        }
    });
}

function _create(url, callback, payload) {
    console.log(url);
    $.ajax({
        type: 'POST',
        url: url,
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
        url: url,
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
        url: url,
        contentType: 'application/json',
        dataType: 'json',
        success: function(data) {
            callback(data);
        }
    });
}

/* User */
function _get_users(callback) {
    _get('/users', callback);
}
function _create_user(callback, payload) {
    _create('/users', callback, payload);
}
function _update_user(callback, id, payload) {
    _update('/user/'+id, callback, payload);
}
function _delete_user(callback, id) {
    _delete('/user/'+id, callback);
}

/* Project */
function _get_projects(callback) {
    _get('/projects', callback);
}
function _create_project(callback, payload) {
    _create('/projects', callback, payload);
}
function _update_project(callback, id, payload) {
    _update('/project/'+id, callback, payload);
}
function _delete_project(callback, id) {
    _delete('/project/'+id, callback);
}

/* Project Assignment */
function _get_project_assignments(callback) {
    _get('/project_assignments', callback);
}
function _create_project_assignment(callback, payload) {
    _create('/projects_assignment', callback, payload);
}
function _update_project_assignment(callback, id, payload) {
    _update('/project_assignment/'+id, callback, payload);
}
function _delete_project_assignment(callback, id) {
    _delete('/project_assignment/'+id, callback, id);
}


/* Task Label */
function _get_task_labels(callback, pid) {
    _get('/project/'+pid+'/task_labels', callback);
}
function _create_task_label(callback, pid, payload) {
    _create('/project/'+pid+'/task_labels', callback, payload);
}
function _update_task_label(callback, id, payload) {
    _update('/project/'+pid+'/task_label/'+id, callback, payload);
}
function _delete_task_label(callback, id) {
    _delete('/project/'+pid+'/task_label/'+id, callback);
}

/* Task */
function _get_tasks(callback, pid) {
    _get('/project/'+pid+'/tasks', callback);
}
function _create_task(callback, pid, payload) {
    _create('/project/'+pid+'/tasks', callback, payload);
}
function _update_task(callback, pid, id, payload) {
    _update('/project/'+pid+'/task/'+id, callback, id, payload);
}
function _delete_task(callback, pid, id) {
    _delete('/project/'+pid+'/task/'+id, callback, id);
}

/* Ticket Label */
function _get_ticket_labels(callback, pid) {
    _get('/project/'+pid+'/ticket_labels', callback);
}
function _create_ticket_label(callback, pid, payload) {
    _create('/project/'+pid+'/ticket_labels', callback, payload);
}
function _update_ticket_label(callback, pid, id, payload) {
    _update('/project/'+pid+'/ticket_label/'+id, callback, id, payload);
}
function _delete_ticket_label(callback, pid, id) {
    _delete('/project/'+pid+'/ticket_label/'+id, callback, id);
}

/* Ticket Priority */
function _get_ticket_priorities(callback) {
    _get('/project/'+pid+'/ticket_priorities', callback);
}
function _create_ticket_priority(callback, payload) {
    _create('/project/'+pid+'/ticket_priorites', callback, payload);
}
function _update_ticket_priority(callback, id, payload) {
    _update('/project/'+pid+'/ticket_priority/+id', callback, id, payload);
}
function _delete_ticket_priority(callback, id) {
    _delete('/project/'+pid+'/ticket_priority/'+id, callback, id);
}

/* Ticket Status */
function _get_ticket_statuses(callback) {
    _get('/project/'+pid+'/ticket_statuses', callback);
}
function _create_ticket_status(callback, payload) {
    _create('/project/'+pid+'/ticket_statuses', callback, payload);
}
function _update_ticket_status(callback, id, payload) {
    _update('/project/'+pid+'/ticket_status/'+id, callback, id, payload);
}
function _delete_ticket_status(callback, id) {
    _delete('/project/'+pid+'/ticket_status/'+id, callback, id);
}

/* Ticket */
function _get_tickets(callback, pid) {
    _get('/project/'+pid+'/tickets', callback);
}
function _create_ticket(callback, pid, tid, payload) {
    _create('/project/'+pid+'/task/'+tid+'/tickets', callback, payload);
}
function _update_ticket(callback, pid, tid, id, payload) {
    _update('/project/'+pid+'/task/'+tid+'ticket/'+id, callback, id, payload);
}
function _delete_ticket(callback, id) {
    _delete('/project/'+pid+'/ticket/'+id, callback, id);
}

/* Comment */
function _get_comments(callback) {
    _get('/comments', callback);
}
function _create_comment(callback, payload) {
    _create('/comments', callback, payload);
}
function _update_comment(callback, id, payload) {
    _update('/comment/'+id, callback, id, payload);
}
function _delete_comment(callback, id) {
    _delete('/comment/'+id, callback, id);
}

