<%inherit file="base.mak"/>

    <style>

        .top-indent {
            margin-top: 10px;
        }

        .single-indent {
            margin-left: 20px;
        }

        .double-indent {
            margin-left: 40px;
        }

        .tripple-indent {
            margin-left: 60px;
        }

        .quadruple-indent {
            margin-left: 80px; 
        }

        .contents-box {
            display: none;
            margin-top: 5px;
            margin-bottom: 5px;
            margin-right: 20px;
            padding: 10px;
            box-shadow: 0px 0px 0px 1px #DDD, 0px 4px 8px rgba(221, 221, 221, 0.9);
        }

        .box {
            padding: 10px;
            margin: 25px;
            border: 1px solid #DDD;
        }

        .small-box {
            margin-left: 5px;
            border-radius: 5px;
            padding-left: 5px;
            padding-right: 5px;
            display: inline-block;
        }

        .task-entry {
            display: none;
        }

        .ticket-entry {
            display: none;
        }

    </style>

    <div id="add-project-modal" class="reveal-modal" data-reveal aria-labelledby="Project" aria-hidden="true" role="dialog">
        <div id="add-project-modal-contents">
            <label>Name</label>
            <input type="text"></input>
            <label>Description</label>
            <textarea rows="8"></textarea>
            <div class="right"><a class="button">Create</a></div>
        </div>
        <a class="close-reveal-modal" aria-label="Close">&#215;</a>
    </div>

    <div id="project-modal" class="reveal-modal" data-reveal aria-labelledby="Project" aria-hidden="true" role="dialog">
        <div id="project-modal-contents"></div>
        <a class="close-reveal-modal" aria-label="Close">&#215;</a>
    </div>

    <div id="add-task-modal" class="reveal-modal" data-reveal aria-labelledby="task" aria-hidden="true" role="dialog">
        <div id="add-task-modal-contents">
            <h3>New Task</h3>
            <label>Title</label>
            <input type="text"></input>
            <label>Contents</label>
            <textarea rows="8"></textarea>
            <div class="right"><a class="button">Create</a></div>
        </div>
        <a class="close-reveal-modal" aria-label="Close">&#215;</a>
    </div>

    <div id="task-modal" class="reveal-modal" data-reveal aria-labelledby="task" aria-hidden="true" role="dialog">
        <div id="task-modal-contents"></div>
        <a class="close-reveal-modal" aria-label="Close">&#215;</a>
    </div>

    <div id="add-ticket-modal" class="reveal-modal" data-reveal aria-labelledby="ticket" aria-hidden="true" role="dialog">
        <div id="add-ticket-modal-contents">
            <h3>New Ticket</h3>
            <label>Title</label>
            <input type="text"></input>
            <label>Contents</label>
            <text rows="8"></textarea>
            <div class="right"><a class="button">Create</a></div>
        </div>
        <a class="close-reveal-modal" aria-label="Close">&#215;</a>
    </div>

    <div id="ticket-modal" class="reveal-modal" data-reveal aria-labelledby="ticket" aria-hidden="true" role="dialog">
        <div id="ticket-modal-contents"></div>
        <a class="close-reveal-modal" aria-label="Close">&#215;</a>
    </div>



    <div class="single-indent" id="page-contents"></div>

    <script>

        String.prototype.fupper = function() {
            return this.charAt(0).toUpperCase() + this.slice(1);
        }

        function get_style(thing) {
            var ret_style = '';
            ret_style += 'color: ' + thing.forecolor + '; ';
            ret_style += 'background-color: ' + thing.backcolor + '; ';
            return ret_style;
        }

        function build_contents_html(type, thing, indent) {
            var html = '';
            html += '<div class="' + indent + '-indent contents-box" id="contents-' + type + '-' + thing.id + '">';
            html += '<i><a href="#/user/' + thing.owner.id + '">' + thing.owner.first + ' ' + thing.owner.last + '</a> opened this ' + type + ' on ' + thing.creation_datetime + '.</i>';
            if ( thing.assignee !== undefined && thing.assignee.id !== undefined )
                html += '</br><a href="#/user/' + thing.assignee.id + '">' + thing.assignee.first + ' ' + thing.assignee.last + '</a> is currently assigned to this ' + type + '.'; 
            html += '<p><div class="box">' + thing.contents + '</div></p>';
            html += '</div>';
            return html;
        }

        function build_ticket_html(ticket) {
            var html = '';
            html += '<div class="ticket-entry">';
            html += '<h5 class="top-indent double-indent">';
            html += '<a class="expand-ticket" ticket-id="'+ ticket.id + '"> + </a>';
            html += 'Ticket: <a href="#/ticket/' + ticket.id +'">' + ticket.title + '</a>';
            if ( ticket.label.id !== undefined )
                html += '<div class="small-box" style="' + get_style(ticket.label) + '">' + ticket.label.label + '</div>';
            if ( ticket.priority.id !== undefined )
                html += '<div class="small-box" style="' + get_style(ticket.priority) + '">' + ticket.priority.label + '</div>';
            if ( ticket.status.id !== undefined )
                html += '<div class="small-box" style="' + get_style(ticket.status) + '">' + ticket.status.label + '</div>'; 
            html += '</h5>';
            html += build_contents_html('ticket', ticket, 'tripple');
            html += '</div>';
            return html;
        }

        function build_task_html(task) {
            var html = '';
            html += '<div class="task-entry">';
            html += '<h4 class="top-indent single-indent">';
            html += '<a class="expand-task" task-id="' + task.id + '"> + </a>';
            html += 'Task: <a href="#/task/' + task.id +'">' + task.title + '</a>';
            html += '</h4>';
            html += '<div id="ticket-list-' + task.id + '">';
            if ( task.tickets.length == 0 ) {
                // display task contents if there are no tickets
                html += build_contents_html('task', task, 'double'); 
            } else {
                task.tickets.forEach(function(ticket) {
                    html += build_ticket_html(ticket);
                });
            }
            html += '</div>';
            html += '</div>';
            return html;
        }

        function build_project_html(project) {
            var html = '';
            html += '<h3 class="top-indent">';
            html += '<a class="expand-project" project-id="' + project.project.id + '"> + </a>';
            html += '<a href="#/project/'+ project.project.id +'">' + project.project.name + '</a>';
            html += '</h3>';
            html += '<div id="task-list-' + project.project.id + '">';
            if ( project.project.tasks.length == 0 ) {
            } else {
                project.project.tasks.forEach(function(task) {
                    html += build_task_html(task);
                });
            }
            html += '</div>';
            return html;
        }

        function _renderer_home() {
            html = '';
            _site.projects.forEach(function(project) {
                html += build_project_html(project);
            });
            return html;
        }

        function _configure_page() { 
            $('.expand-project').on('click', function() {
                var state = $(this).html().trim();
                var sign = '';
                var project_id = $(this).attr('project-id');
                if ( state == '+' ) {
                    sign = ' &#8211; ';
                    var tasks = $('#task-list-' + project_id).find('div');
                    for( var i=0; i<tasks.length; i++) {
                        if ( $(tasks[i]).hasClass('task-entry') )
                            $(tasks[i]).show();
                    }
                } else {
                    sign = ' + ';
                    var tasks = $('#task-list-' + project_id).find('div');
                    for( var i=0; i<tasks.length; i++) {
                        if ( $(tasks[i]).hasClass('task-entry') )
                            $(tasks[i]).hide();
                    }
                }
                $(this).html(sign);
            });
            $('.expand-task').on('click', function() {
                var state = $(this).html().trim();
                var sign = '';
                var task_id = $(this).attr('task-id');
                if ( state == '+' ) {
                    sign = ' &#8211; ';
                    var tickets = $('#ticket-list-' + task_id).find('div');
                    for( var i=0; i<tickets.length; i++) {
                        if ( $(tickets[i]).hasClass('ticket-entry') ) 
                            $(tickets[i]).show();
                    }
                    $('#contents-task-' + task_id).show(); 
                } else {
                    sign = ' + ';
                    var tickets = $('#ticket-list-' + task_id).find('div');
                    for( var i=0; i<tickets.length; i++) {
                        if ( $(tickets[i]).hasClass('ticket-entry') ) 
                            $(tickets[i]).hide();
                    }
                    $('#contents-task-' + task_id).hide();
                }
                $(this).html(sign);
            });
            $('.expand-ticket').on('click', function() {
                var state = $(this).html().trim();
                var sign = '';
                var task_id = $(this).attr('ticket-id');
                if ( state == '+' ) {
                    sign = ' &#8211; ';
                    $('#contents-ticket-' + task_id).show();
                } else {
                    sign = ' + ';
                    $('#contents-ticket-' + task_id).hide();
                }
                $(this).html(sign);
            });

        }

        function build_comments_html(comments) {
            var html = '';
            html += '<label>Comments</lable>';
            comments.forEach(function(comment) {
                html += '<i><a href="/user/' + comments.user.id + '">' + comments.user.first + ' ' + comments.user.last + '</a> commented on ' + comments.creation_datetime + '</i>';
                html += '<div class="box">' + comment.contents + '</div>';
            });
            return html
        }

        function build_project_modal_html(project) {
            var html = '';
            html += '<label>Name</label>';
            html += '<input type="text" value="' + project.project.name + '"></input>';
            html += '<label>Description</label>';
            html += '<textarea rows="8">' + project.project.description + '</textarea>'; 
            html += build_comments_html(project.project.comments);
            return html;
        }

        function nav(type, id) {
            var html = 'Error.';
            switch(type) {
                case 'project':
                    var project = _site.get_project_by_id(id)
                    html = build_project_modal_html(project);
                    break;
                case 'task':
                    html = build_task_modal_html(id);
                    break;
                case 'ticket':
                    html = build_ticket_modal_html(id);
                    break;
                case '':
                default:
                    break;
            }
            $('#' + type + '-modal-contents').html(html);
            $('#' + type + '-modal').foundation('reveal','open');
        }

        _site.set_renderer(_renderer_home, _configure_page);

    </script>
