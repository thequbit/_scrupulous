var _site = {
    projects: [],
    get_projects: function() {
       console.log('_site.get_projects(): getting projects ...');
       _get_projects(_site._set_projects);
    },
    _set_projects: function(payload) {
        console.log('_site._set_projects(): Projects gotten.');
        _site.projects = payload;
        //_site._do_refresh();
        _site._nav();
    },
    get_project_by_id: function(id) {
        var project = null;
        for(var i=0; i<_site.projects.length; i++) {
            if ( _site.projects[i].project.id == parseInt(id) ) {
                project = _site.projects[i];
                break;
            }
        }
        return project
    },
    get_project_by_name: function(name) {
        var project = null;
        for(var i=0; i<_site.projects.length; i++) {
            if ( _site.projects[i].project.name == name ) {
                project = _site.projects[i];
                break;
            }
        }
        return project 
    },
    get_task_by_id: function(id) {
        var task = null;
        for(var i=0; i<_site.projects.length; i++) {
            for(var j=0; j<_site.projects[i].project.tasks.length; j++) {
                if ( _site.projects[i].project.tasks[j].id == parseInt(id) ) {
                    task = _site.projects[i].project.tasks[j];
                    break;
                }
            }
        }
        return task
    },
    get_ticket_by_id: function(id) {
        var ticket = null;
        for(var i=0; i<_site.projects.length; i++) {
            for(var j=0; j<_site.projects[i].project.tasks.length; j++) {
                for(var k=0; k<_site.projects[i].project.tasks[j].tickets.length; k++) {
                    if ( _site.projects[i].project.tasks[j].tickets[k].id == parseInt(id) ) {
                        ticket = _site.projects[i].project.tasks[j].tickets[k];
                        break;
                    }
                }
            }
        }
        return ticket
    },

    _nav: function() {
    },
    load: function(nav) {
        console.log('_site.load(): refreshing site contents ...');
        _site._nav = nav;
        _site.refresh();
    },
    loaded: function() {
        //alert(JSON.stringify(_site.projects));
    },
    
    //
    // entry point of page render
    //
    set_renderer: function(page) {
        _site._renderer = page.render;
        _site._page_config = page.config;
    },
    _renderer: function() {
    },
    _page_config: function() {
    },
    refresh: function() {
        console.log('_site.refresh(): rendering page.');
        _site.get_projects();
    },
    _do_refresh: function() {
        //_site.nav();
        html = _site._renderer();
        $('#page-contents').html(html);
        _site._page_config()
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
        _site.refresh();
    },
    update_project: function(id, name, description) {
       var payload = {name:name, description: description};
       _update_project(_site.update_project_success, id, payload);
    },
    update_project_success: function() {
        _site.refresh();
    },

    create_project_assignment: function(project_id, user_id) {
        var payload = {project_id: project_id, user_id: user_id};
        _create_project_assignment(_site.create_project_assignment_success, payload);
    },
    create_project_assignment_success: function() {
        _site.refresh();
    },
    update_project_assignment: function(id, project_id, user_id) {
        var payload = {project_id: project_id, user_id: user_id};
        _update_project_assignemnt(_site.update_projcet_assignment_success, id, payload);
    },
    update_project_assignment_success: function() {
        _site.refresh();
    },

    create_task_label: function(project_id, label, forecolor, backcolor) {
        var payload = {label: label, forecolor: forecolor, backcolor: backcolor}; //, project_id: project_id};
        _create_task_label(_site.create_task_label_success, project_id, payload);
    },
    create_task_label_success: function() {
        _site.refresh();
    },
    update_task_label: function(id, label, forecolor, backcolor) {
        var payload = {label: label, forecolor: forecolor, backcolor: backcolor}; //, project_id: project_id};
        _update_task_label(_site.update_task_label_success, id, payload);
    },
    update_task_label_success: function() {
        _site.refresh();
    },

    create_task: function(title, contents, due_datetime, project_id) {
       var payload = {title: title, contents: contents, due_datetime: due_datetime}; //, user_id: user_id, project_id: project_id};
       _create_task(_site.create_task_success, project_id, payload);
    },
    create_task_success: function() {
        _site.refresh();
    },
    update_task: function(id, title, contents, due_datetime, user_id, project_id) {
       var payload = {titke: title, contents: contents, due_datetime: due_datetime, user_id: user_id, project_id: project_id};
       _update_task(_site.update_task_success, id, payload);
    },
    update_task_success: function() {
        _site.refresh();
    },

    create_ticket_label: function(label, forecolor, backcolor, project_id) {
       var payload = {label: label, forecolor: forecolor, backcolor: backcolor, project_id: project_id};
       _create_ticket_label(_site.create_ticket_label_success, payload);
    },
    create_ticket_label_success: function() {
        _site.refresh();
    },
    update_ticket_label: function(id, label, forecolor, backcolor, project_id) {
       var payload = {label: label, forecolor: forecolor, backcolor: backcolor, project_id: project_id};
       _update_ticket_label(_site.update_ticket_label_success, id, payload);
    },
    update_ticket_lable_success: function() {
        _site.refresh();
    },

    create_ticket_priority: function(priority, forecolor, backcolor) {
       var payload = {priority: priority, forecolor: forecolor, backcolor: backcolor, project_id: project_id};
       _create_ticket_priority(_site._site.create_ticket_priority_success, payload);
    },
    create_ticket_priority_success: function() {
        _site.refresh();
    },
    update_ticket_priority: function(id, priority, forecolor, backcolor, project_id) {
       var payload = {priority: priority, forecolor: forecolor, backcolor: backcolor, project_id: project_id};
       _update_ticket_priority(_site.update_ticket_priority_success, id, payload);
    },
    update_ticket_priority_success: function() {
        _site.refresh();
    },

    create_ticket_status: function(status, forecolor, backcolor) {
       var payload = {status: status, forecolor: forecolor, backcolor: backcolor, project_id: project_id};
       _create_ticket_status(_site.create_ticket_status_success, payload);
    },
    create_ticket_status_success: function() {
        _site.refresh();
    },
    update_ticket_status: function(id, status, forecolor, backcolor, project_id) {
       var payload = {status: status, forecolor: forecolor, backcolor: backcolor, project_id: project_id};
       _update_ticket_status(_site.update_ticket_status_success, id, payload);
    },
    update_ticket_status_success: function() {
        _site.refresh();
    },

    create_ticket: function(title, contents, due_datetime, assignee_id, ticket_label_id, ticket_priority_id, ticket_status_id, project_id, task_id) {
        var payload = {title: title, contents: contents, due_datetime: due_datetime,
                       assignee_id: assignee_id, ticket_label_id: ticket_label_id, 
                       ticket_priority_id: ticket_priority_id, ticket_status_id: ticket_status_id};
        _create_ticket(_site.create_ticket_success, project_id, task_id, payload);
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
        _site.refresh();
    },

    create_comment: function(contents, author_id, project_id, task_id, ticket_id) {
        var payload = {contents: contents, author_id: author_id, project_id: project_id, task_id: task_id, ticket_id: ticket_id}
        _create_comment(_site.create_comment_success, payload);
    },
    create_comment_success: function() {
        _site.refresh();
    },
    update_comment: function(id, contents, author_id, project_id, task_id, ticket_id) {
        var payload = {contents: contents, author_id: author_id, project_id: project_id, task_id: task_id, ticket_id: ticket_id}
        _update_comment(_site.update_comment_success, id, payload);
    },
    update_comment_success: function() {
        _site.refresh();       
    },

      
}

