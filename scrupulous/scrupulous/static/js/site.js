var _site = {
    projects: [],
    get_projects: function() {
       _get_projects(_site._set_projects);
    },
    _set_projects: function(payload) {
        console.log('_site._set_projects(): Projects gotten.');
        _site.projects = payload.projects;
        _site.refresh();
    },
    get_project_by_id: function(id) {
        var project = null;
        console.log(_site.projects.length);
        console.log('start.');
        for(var i=0; i<_site.projects.length; i++) {
            if ( _site.projects[i].project.id == parseInt(id) ) {
                project = _site.projects[i];
                break;
            }
        }
        console.log('out.');
        return project
    },
    load: function() {
        console.log('_site.load(): Getting projects ...');
        _site.get_projects();
    },
    loaded: function() {
        //alert(JSON.stringify(_site.projects));
    },
    
    //
    // entry point of page render
    //
    set_renderer: function(renderer, page_config) {
        _site._renderer = renderer;
        _site._page_config = page_config;
    },
    refresh: function() {
        console.log('_site.refresh(): rendering page.');
        html = _site._renderer();
        $('#page-contents').html(html);
        _site._page_config()
    },

    render_page_home: function() {
    },

    // CRUD Functions
    create_user: function(first, last, email, password, user_type_id) {
        var payload = {first: first, last: last, email: email, password: password, user_type_id: user_type_id};
        _create_user(_site.create_user_success, payload);
    },
    create_user_success: function() {

    },
    update_user: function(first, last, email, password, user_type_id) {
       var payload = {first: first, last: last, email: email, password: password, user_type_id: user_type_id};
       _update_user(_site.update_user_success, id, payload);
    },
    update_user_success: function() {

    },

    create_project: function(name, description) {
       var payload = {name: name, description: description};
       _create_project(_site.create_project_success, payload);
    },
    create_project_success: function() {

    },
    update_project: function(id, name, description) {
       var payload = {name:name, description: description};
       _update_project(_site.update_project_success, id, payload);
    },
    update_project_success: function() {

    },

    create_project_assignment: function(project_id, user_id) {
        var payload = {project_id: project_id, user_id: user_id};
        _create_project_assignment(_site.create_project_assignment_success, payload);
    },
    create_project_assignment_success: function() {

    },
    update_project_assignment: function(id, project_id, user_id) {
        var payload = {project_id: project_id, user_id: user_id};
        _update_project_assignemnt(_site.update_projcet_assignment_success, id, payload);
    },
    update_project_assignment_success: function() {

    },

    create_task_label: function(label, forecolor, backcolor, project_id) {
        var payload = {label: label, forecolor: forecolor, backcolor: backcolor, project_id: project_id};
        _create_task_label(_site.create_task_label_success, payload);
    },
    create_task_label_success: function() {

    },
    update_task_label: function(id, label, forecolor, backcolor, project_id) {
        var payload = {label: label, forecolor: forecolor, backcolor: backcolor, project_id: project_id};
        _update_task_label(_site.update_task_label_success, id, payload);
    },
    update_task_label_success: function() {
        
    },

    create_task: function(title, contents, due_datetime, user_id, project_id) {
       var payload = {title: title, contents: contents, due_datetime: due_datetime, user_id: user_id, project_id: project_id};
       _create_task(_site.create_task_success, payload);
    },
    create_task_success: function() {

    },
    update_task: function(id, title, contents, due_datetime, user_id, project_id) {
       var payload = {titke: title, contents: contents, due_datetime: due_datetime, user_id: user_id, project_id: project_id};
       _update_task(_site.update_task_success, id, payload);
    },
    update_task_success: function() {

    },

    create_ticket_label: function(label, forecolor, backcolor, project_id) {
       var payload = {label: label, forecolor: forecolor, backcolor: backcolor, project_id: project_id};
       _create_ticket_label(_site.create_ticket_label_success, payload);
    },
    create_ticket_label_success: function() {
        
    },
    update_ticket_label: function(id, label, forecolor, backcolor, project_id) {
       var payload = {label: label, forecolor: forecolor, backcolor: backcolor, project_id: project_id};
       _update_ticket_label(_site.update_ticket_label_success, id, payload);
    },
    update_ticket_lable_success: function() {

    },

    create_ticket_priority: function(priority, forecolor, backcolor) {
       var payload = {priority: priority, forecolor: forecolor, backcolor: backcolor, project_id: project_id};
       _create_ticket_priority(_site._site.create_ticket_priority_success, payload);
    },
    create_ticket_priority_success: function() {

    },
    update_ticket_priority: function(id, priority, forecolor, backcolor, project_id) {
       var payload = {priority: priority, forecolor: forecolor, backcolor: backcolor, project_id: project_id};
       _update_ticket_priority(_site.update_ticket_priority_success, id, payload);
    },
    update_ticket_priority_success: function() {

    },

    create_ticket_status: function(status, forecolor, backcolor) {
       var payload = {status: status, forecolor: forecolor, backcolor: backcolor, project_id: project_id};
       _create_ticket_status(_site.create_ticket_status_success, payload);
    },
    create_ticket_status_success: function() {
        
    },
    update_ticket_status: function(id, status, forecolor, backcolor, project_id) {
       var payload = {status: status, forecolor: forecolor, backcolor: backcolor, project_id: project_id};
       _update_ticket_status(_site.update_ticket_status_success, id, payload);
    },
    update_ticket_status_success: function() {

    },

    create_ticket: function(title, contents, due_datetime, task_id, owner_id, assignee_id, ticket_label_id, ticket_priority_id, ticket_status_id) {
        var payload = {title: title, contents: contents, due_datetime: due_datetime, task_id: task_id,
                       owner_id: owner_id, assignee_id: assignee_id, ticket_label_id: ticket_label_id, 
                       ticket_priority_id: ticket_priority_id, ticket_status_id: ticket_status_id};
        _create_ticket(_site.create_ticket_success, payload);
    },
    create_ticket_success: function() {

    },
    update_ticket: function(id, title, contents, due_datetime, task_id, owner_id, assignee_id, ticket_label_id, ticket_priority_id, ticket_status_id) {
        var payload = {title: title, contents: contents, due_datetime: due_datetime, task_id: task_id,
                       owner_id: owner_id, assignee_id: assignee_id, ticket_label_id: ticket_label_id, 
                       ticket_priority_id: ticket_priority_id, ticket_status_id: ticket_status_id};
        _update_ticket(_site.update_ticket_success, id, payload);
    },
    update_ticket_success: function() {

    },

    create_comment: function(contents, author_id, project_id, task_id, ticket_id) {
        var payload = {contents: contents, author_id: author_id, project_id: project_id, task_id: task_id, ticket_id: ticket_id}
        _create_comment(_site.create_comment_success, payload);
    },
    create_comment_success: function() {
        
    },
    update_comment: function(id, contents, author_id, project_id, task_id, ticket_id) {
        var payload = {contents: contents, author_id: author_id, project_id: project_id, task_id: task_id, ticket_id: ticket_id}
        _update_comment(_site.update_comment_success, id, payload);
    },
    update_comment_success: function() {
        
    },

      
}

