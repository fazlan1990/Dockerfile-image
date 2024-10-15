# Map commands to API endpoints

get_endpoints = {
    "mytickets": "/api/view/myrequests?orderby=&ascending=",
    "agentusers": "/api/agent/user",
    "navigationtypes": "/api/options/request/navigation-types",
    "groups": "/api/admin/group",
    "userdetails": "/api/v2/user/{user_id}",
    "getcomments": "/api/v2/request/{request_id}/thread"
}

post_endpoints = {
    "resolve": "/api/itil/request/{request_id}/thread/resolution",
    "comment": "/api/itil/request/{request_id}/thread/comment",
    "create": "/api/itil/request",
    "options": "/api/itil/request/options/type/{navigation_type}/v2",
}