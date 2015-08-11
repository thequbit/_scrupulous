
function build_masks() {

    masks = {
        status: [],
        labels: [],
        users: []
    }

    var things = [
        'status',
        'labels',
        'users'
    ];

    for( var i=0; i<things.length; i++ ) {
        var checkboxes = $(document).find('.' + things[i] +'-mask-checkbox');
        for( var j=0; j<checkboxes.length; j++) {
            if ( $(checkboxes[j]).is(':checked') ) {
                var text = $(checkboxes[j]).data('value');
                masks[things[i]].push(text);
            }
        }
    }

    console.log(masks);

    return masks;

}

$(document).ready(function() {

    $('.mask-checkbox').change(function() {
        console.log('changed');
        //var checked = $(this).is(':checked');
        //var status = $(this).val();
        masks = build_masks();
        //site.refresh_entities(masks);
        site.apply_masks(masks);
    });

    $('#status-masks-select-all').on('click', function() {
        console.log('hi');
        for( var checkbox in $(document).find('.status-mask-checkbox') ) {
            $(checkbox).checked = true;
        }
    });

});

function containsObject(list, obj) {
    var i;
    if ( list.length == 0 )
        return false;
    var exists = null;
    for (i = 0; i < list.length; i++) {
        exists = true;
        for( var key in obj ) {
            if (list[i][key] !== undefined && list[i][key] == obj[key]) {
                // still good
            } else {
                exists = false;
            }
        }
        if ( exists )
            return true
    }
    return false;
}
var site = {

    // PRIVATE //
    _entities: [],
    _labels: [],
    _users: [],
    
    // PUBLIC //
    init: function() {
        // init site
        
    },
    load_entity: function(entity) {
        site._entities.push(entity);
    },
    refresh_masks: function(existing) {
        if ( existing === undefined ) {
            existing = {
                labels: [],
                users: []
            }
        } 
        site._labels = [];
        site._users = [];
        for(var i=0; i<site._entities.length; i++) {
            var entity = site._entities[i];
            for(var j=0; j<entity.tickets.length; j++) {
                var ticket = entity.tickets[j];
                if ( ticket.assignee !== undefined ) {
                    var user = {first: ticket.assignee.first, last: ticket.assignee.last};
                    if ( !containsObject(site._users, user) ) {
                        site._users.push(user);
                    }
                }
                if ( ticket.label !== undefined && ticket.label != null && ticket.label != '' ) {
                    var label = {label: ticket.label, label_color: ticket.label_color};
                    if ( !containsObject(site._labels, label) ) {
                        site._labels.push(label);
                    }
                }
            }
        }

        var html = '';
        for( var i=0; i<site._labels.length; i++ ) {
            var checked = '';
            if ( existing.labels.indexOf(site._labels[i].label) != -1 ) {
                checked = 'checked';
            }
            html += '<input class="labels-mask-checkbox mask-checkbox" data-value="' + site._labels[i].label + '"type="checkbox" ' + checked + '></input>';
            html += '<div class="ticket-label" style="background-color: ' + site._labels[i].label_color + '">' + site._labels[i].label + '</div></br>';
        }
        $('#label-masks').html(html);
        
        var html = '';
        for( var i=0; i<site._users.length; i++ ) {
            var checked = '';
            if ( existing.labels.indexOf(site._users[i].label) != -1 ) {
                checked = 'checked';
            }
            html += '<input class="users-mask-checkbox mask-checkbox" data-value="' + site._users[i].first + '_' + site._users[i].last + '" type="checkbox" ' + checked + '>' + site._users[i].first + ' ' + site._users[i].last + '</input></br>';
        }
        $('#user-masks').html(html);

    },
    load_entities: function(masks) {
        $('#entities').html('loading ...');
        if ( masks === undefined ) {
            masks = {
                labels: [],
                users: [],
            }
        }
        var html = '';
        for(var i=0; i<site._entities.length; i++) {
            var entity = site._entities[i];
            var closed_count = 0;
            var _html = '';
            for(var j=0; j<entity.tickets.length; j++) {
                var ticket = entity.tickets[j];
                //var t = '';
                var assignee = 'unassigned';
                if ( ticket.assignee !== undefined ) {
                    assignee = ticket.assignee.first + '_' + ticket.assignee.last;
                }
                _html += '<div id="'+ entity.name + '-ticket-' + ticket.number + '"' + 
                         'class="ticket ticket-status-' + ticket.status + '" ' + 
                         'data-status="' + ticket.status + '" ' + 
                         'data-label="' + ticket.label + '" ' + 
                         'data-assignee="' + assignee + '">';
                if ( ticket.label !== undefined ) {
                    _html += '<div class="ticket-label" style="background-color: ' + ticket.label_color + '">' + ticket.label + '</div>';
                }
                _html += ticket.title;
                if ( ticket.assignee !== undefined ) {
                    _html += '<div class="right">' + ticket.assignee.first.charAt(0).toUpperCase() + ticket.assignee.last.charAt(0).toUpperCase() + '</div>';
                }
                _html += '</div>';
            }
            var percent = (closed_count / entity.tickets.length * 100).toFixed(0);
            var complete = ' <small>' + percent + '% ( ' + closed_count + '/' + entity.tickets.length + ' )</small>';
            _html = '<h5>' + entity.name + complete + '</h5>' + _html;
            html += '<div class="entity-column">' + _html + '</div>';
        }
        $('#entities').html(html);
    },
    apply_masks: function(masks) {
        console.log('applying masks:');
        console.log(masks);
        var tickets = $(document).find('.ticket');
        for( var i=0; i<tickets.length; i++) {
            var ticket = tickets[i];

            var status_show = false;
            for( var j=0; j<masks.status.length; j++ ) {
                if ( $(ticket).data('status') == masks.status[j] ) {
                    status_show = true;
                }
            }

            var label_show = false;
            for( var j=0; j<masks.labels.length; j++ ) {
                console.log($(ticket).data('label') + ' ?= ' + masks.labels[j]);
                if ( $(ticket).data('label') == masks.labels[j] ) {
                    label_show = true;
                }
            }

            var user_show = true;

            if ( status_show && label_show && user_show ) {
                $(ticket).fadeIn(100);
            } else {
                $(ticket).fadeOut(100);
            }
        }
    }
}
