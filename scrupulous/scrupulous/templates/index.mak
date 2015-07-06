<%inherit file="base.mak"/>

<style>
    .box {
        margin-top: 10px;
        margin-bottom: 10px;
        margin-left: 10px;
        margin-right: 10px;
        padding: 25px;
        box-shadow: 0px 0px 0px 1px #DDD, 0px 4px 8px rgba(221, 221, 221, 0.9);
    }
    .contents {
        background-color: #F0F0F0;
    }
    .spacer {
        height: 20px;
    }
    .single-indent {
        padding-left: 10px;
    }
    .bottom-space {
        padding-bottom: 20px;
    }
    .top-space {
        padding-top: 20px;
    }
</style>

<div class="row">
  <div class="columns small-12">
    <div id="bread-crumbs"></div> 
  </div>
</div>

<div class="row">
  <div class="columns medium-12">
    <div id="page-contents"></div>
  </div>
</div>

<script>

    var page_home = {

        build_rows: function(project) {
            var rows = []
            console.log('project:');
            console.log(project);
            if ( project.project.tasks.length == 0 ) {
                rows.push({
                    project: {
                        name: project.project.name, 
                        id: project.project.id,
                    },
                    task: null,
                    ticket: null
                });
            } else {
                for( var i=0; i<project.project.tasks.length; i++ ) {
                    if ( project.project.tasks[i].tickets.length == 0 ) {
                        rows.push({
                            project: {
                                name: project.project.name, 
                                id: project.project.id,
                            },
                            task: {
                                name: project.project.tasks[i].title,
                                id: project.project.tasks[i].id,
                            },
                            ticket: null
                        });
                    } else {
                        for( var j=0; j<project.project.tasks[i].tickets.length; j++ ) {
                            rows.push({
                                project: {
                                    name: project.project.name,
                                    id: project.project.id,
                                },
                                task: {
                                    name: project.project.tasks[i].title,
                                    id: project.project.tasks[i].id,
                                },
                                ticket: {
                                    name: project.project.tasks[i].tickets[j].title,
                                    id: project.project.tasks[i].tickets[j].id,
                                }
                            });
                        }
                    }
                }
            }
            return rows;
        },

        build_project_rows: function (project) {
            var html = '';
            var rows = page_home.build_rows(project);
            var current_project = '';
            var current_task = '';
            html += '<tbody>';
            for( var i=0; i<rows.length; i++) {
                var row = rows[i];
                html += '<tr>';
                if ( row.project.name != current_project ) {
                    html += '<td><a href="#/project/' + row.project.id + '">' + row.project.name + '</a></td>';
                    current_project = row.project.name;
                    current_task = '';
                } else {
                    html += '<td></td>';
                }
                if ( row.task != null ) {
                    if ( row.task.name != current_task ) {
                        console.log(row);
                        html += '<td><a href="#/project/' + row.project.id + '/task/' + row.task.id + '">' + row.task.name + '</a></td>';
                        current_task = row.task.name;
                    } else {
                        html += '<td></td>';
                    }
                    if ( row.ticket != null ) {
                        var ticket = _site.get_ticket_by_id(row.ticket.id);
                        /*if ( ticket.assignee.id !== undefined ) {
                            html += '<td>';
                            //html += '<a href="#/user/' + ticket.assignee.id + '">';
                            html += ticket.assignee.first + ' ' + ticket.assignee.last;
                            //html += '</a>';
                            html += '</td>';
                        } else {
                            html += '<td></td>';
                            html += '<td></td>';
                        }*/
                        html += '<td><a href="#/project/' + row.project.id + '/task/' + row.task.id + '/ticket/' + row.ticket.id +'">' + row.ticket.name + '</a></td>';
                    } else {
                        //html += '<td></td>';
                        html += '<td><h4><small><i>None</i></small></h4></td>';
                    }
                } else {
                    html += '<td></td>';
                    //html += '<td></td>';
                    html += '<td></td>';
                }
                html += '</tr>';
            }
            html += '</tbody>';
            return html;
        },

        build_project_table: function(projects) {
            var html = '';
            html += '<table id="projects-table">';
            html += '  <thead><tr>';
            html += '    <th>Project</td>';
            html += '    <th>Task</td>';
            //html += '    <th>Asingee</th>';
            html += '    <th>Ticket</td>';
            html += '  </tr></thead>';
            for( var i=0; i<projects.length; i++ ) {
                html += page_home.build_project_rows(projects[i]);
            }
            html += '</table>';
            return html;
        },

        _projects_table: null,
        set_searchable_table: function() {
            page_home._projects_table = $('#projects-table').dataTable({
                "bSort": false,
            });
        },
        remove_searchable_table: function() {
            if ( page_home._projects_table != null ) {
                page_home._projects_table.fnDestroy();
            }
        },
        config: function() {
            //console.log('page loaded'); 
            $('#searchable-table-select').change(function() {
                if($(this).is(":checked")) {
                    page_home.set_searchable_table();
                } else {
                    page_home.remove_searchable_table();
                }
            });
            page_home.remove_searchable_table(); 
        },

        render: function() {
            var html = '';
            html += '<h3>Scrupulous</h3>';
            html += '<input type="checkbox" id="searchable-table-select"></input> Searchable Table';
            html += page_home.build_project_table(_site.projects);
            return html;
        }
    }

    var page_project = {
        _project_id: null,
        _task_id: null,
        _ticket_id: null,
        set_id: function(id) {
            page_project._project_id = id;
        },
        config: function() {
            console.log('Project.configure(): Start.');
        },
        render: function() {
            console.log('Project.render(): Start.');
            var html = '';
            html += build_bread_crumbs(page_project);
            html += '<h4>' + _site.get_project_by_id(page_project._project_id).project.name + '<small> Project</small></h4>';
            return html;
        }
    }

    function submit_project_comment(project_id) {
        submit_comment('project', project_id, null, null);
    }

    function submit_task_comment(task_id) {
        submit_comment('task', null, task_id, null);
    }

    function submit_ticket_comment(ticket_id) {
        submit_comment('ticket', null, null, ticket_id);
    }

    function submit_comment(prefix, project_id, task_id, ticket_id) {
       var contents =  $('#' + prefix + '-comment-contents').val();
       _site.create_comment(contents, 1, project_id, task_id, ticket_id);
    }

    var page_task = {
        _project_id: null,
        _task_id: null,
        _ticket_id: null,
        set_id: function(id) {
            page_task._task_id = id;
        },
        set_project_id(id) {
            page_task._project_id = id;
        },   
        build_task_html: function(task) {
            var html = '';
            html += '<h3>' + task.title + '<small> Task</small></h3>';
            html += '<div class="spacer"></div>';
            html += '<i>Created by ' + task.owner.first + ' ' + task.owner.last + ' on ' + task.creation_datetime + '</i>';
            html += '<div class="box contents">';
            html += task.contents;
            html += '</div>';
            html += '<hr>';
            html += build_comments_html(task.comments);
            html += '<hr>';
            html += '<textarea id="task-comment-contents" rows="8"></textarea>';
            html += '<a class="button" onclick="submit_task_comment(' + task.id + ');">Submit</a>'
            return html;
        },
        config: function() {
            console.log('Task.config(): Start.');
        },
        render: function() {
            console.log('Task.render(): Start.');
            var html = '';
            var task = _site.get_task_by_id(page_task._task_id);
            if ( task != null ) {
                html += build_bread_crumbs(page_task);
                html += page_task.build_task_html(task);
            } else {
                // invalid task ID
                window.location = '/';
            }
            return html;
        }
    }

    var page_ticket = {
        _project_id: null,
        _task_id: null,
        _ticket_id: null,
        set_id: function(id) {
            page_ticket._ticket_id = id;
        },
        set_project_id: function(id) {
            page_ticket._project_id = id;
        },
        set_task_id: function(id) {
            page_ticket._task_id = id;
        },
        config: function() {
            console.log('Ticket.config(): Start.');
        },
        render: function() {
            console.log('Ticket.render(): Start.');
            console.log('Ticket.render(): project_id: ' + page_ticket._project_id);
            var html = '';
            html += build_bread_crumbs(page_ticket);
            html += '<h4><small>Ticket</small> ' + _site.get_ticket_by_id(page_ticket._ticket_id).title + '</h4>';
            return html;
        }
    }

    function build_comments_html(comments) {
        console.log(comments);
        var html = '';
        html += '<h5 class="bottom-space">Comments:</h5>';
        if ( comments.length == 0 ) {
            html += '<h4><small><i class="single-indent">no comments yet.</i></small></h4>'; 
        } else {
            for( var i=comments.length-1; i>-1; i-- ) {
                html += '<h4 class="top-space"><small><i class="single-indent">';
                html += comments[i].user.first + ' ' + comments[i].user.last + ' wrote on ' + comments[i].creation_datetime + ':';
                html += '</i></small></h4>';
                html += '<div class="box">';
                html += comments[i].contents;
                html += '</div>';
            }
        }
        return html;
    }

    function build_bread_crumbs(page) {
        console.log(page);
        var html = '';
        html += '<a href="/">Home</a>';
        if ( page._project_id !== undefined && page._project_id != null ) {
            html += ' &gt; <a href="#/project/' + page._project_id + '">';
            html += _site.get_project_by_id(page._project_id).project.name;
            html += '</a>';
        }
        if ( page._task_id !== undefined && page._task_id != null ) {
            html += ' &gt; <a href="#/project/' + page._project_id + '/task/' + page._task_id + '">';
            html += _site.get_task_by_id(page._task_id).title;
            html += '</a>';
        }
        if ( page._ticket_id !== undefined && page._ticket_id != null ) {
            html += 'i &gt; <a href="#/project/' + page._project_id + '/task/' + page._task_id + '/ticket/' + page._ticket_id + '">';
            html += _site.get_ticket_by_id(page._ticket_id).title;
            html += '</a>';
        }
        html += '<hr>';
        return html;
    }

    function nav(parts) {
        // this function handles the internal page routing
        //  #/project/1/task/1/ticket/1
        var parts = location.hash.slice(1).split('/').slice(1);
        console.log('nav(): ' + location.hash);
        //console.log(parts);
        var page = page_home;
        if ( parts !== undefined ) {
            if ( parts[0] == 'project' ) {
                if ( parts[1] == 'new' ) {
                    console.log('nav(): New Project');
                    page = page_new_project;
                } else {

                    // if task
                    if ( parts.length > 2 ) {
                        if ( parts[2] == 'task' ) {
                            if ( parts[3] == 'new' ) {
                                console.log('nav(): New Task.')
                                page = page_new_task;
                            } else {

                                // if ticket
                                if ( parts.length > 4 ) {
                                    if ( parts[4] == 'ticket' ) {
                                        if ( parts[5] == 'new' ) {
                                            page_new_ticket.set_project_id(parseInt(parts[1]));
                                            page_new_ticket.set_task_id(parseInt(parts[3]));
                                            page = page_new_ticket;
                                        } else {
                                            page_ticket.set_project_id(parseInt(parts[1]))
                                            page_ticket.set_task_id(parseInt(parts[3]));
                                            page_ticket.set_id(parseInt(parts[5]));
                                            page = page_ticket;
                                        }
                                    }
                                } else {
                                    console.log('nav(): Open Task');
                                    page_task.set_project_id(parseInt(parts[1]));
                                    page_task.set_id(parseInt(parts[3]));
                                    page = page_task;
                                }
                            }
                        }
                    } else {
                        console.log('nav(): Open Project');
                        page_project.set_id(parseInt(parts[1]));
                        page = page_project;
                    }
                }
            }

 
        }
        _site.set_renderer(page);
        _site._do_refresh();
    }

    window.onhashchange = function() {
        nav();
    }

    _site.load(nav);
    
</script>
