import json

def generate_create_ticket_ui(user_id, agent_list, type_list, group_list):
    # Parse the JSON string into a list of dictionaries
    agent_data = json.loads(agent_list)
    type_data = json.loads(type_list)
    group_data = json.loads(group_list)

    agent_data = agent_data.get("Result", [])
    group_data = group_data.get("Result", [])

    # Filter based on conditions // Filter it by groups
    active_agents = [agent for agent in agent_data if agent["Agent"] == 1 and agent["Enabled"] == 1 and agent["AllowPortalLogin"] == 1]

    active_groups = [group for group in group_data if group["Enabled"] == 1]

    # Construct the list of options for the dropdowns (Agent/Type/Group)
    agent_options = [
        {
            "text": {
                "type": "plain_text",
                "text": agent["Name"]
            },
            "value": str(agent["Id"])
        } 
        for agent in active_agents
    ]

    type_options = [
        {
            "text": {
                "type": "plain_text",
                "text": type["name"]
            },
            "value": str(type["id"])
        } 
        for type in type_data
    ]

    group_options = [
        {
            "text": {
                "type": "plain_text",
                "text": group["Name"]
            },
            "value": str(group["Id"])
        } 
        for group in active_groups
    ]

    create_ticket_ui = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Create Ticket",
            "emoji": True
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Hey <@{user_id}>*, Let's create a ticket in sDesk :"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "subject_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Enter subject"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": ":abc: Subject",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": "description_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Enter description"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": ":spiral_note_pad: Description",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "block_id": "requester_section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":male_supervillain: *Requester*\nChoose a Requester"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Choose list",
                        "emoji": True
                    },
                    "options": agent_options
                }
            },
            {
                "type": "section",
                "block_id": "type_section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":ladybug: *Type*\nChoose a Type"
                },
                "accessory": {
                    "type": "static_select",
                    # "action_id": "type_select", 
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Choose list",
                        "emoji": True
                    },
                    "options": type_options
                }
            },
            {
                "type": "section",
                "block_id": "agent_section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":man_in_tuxedo: *Agent*\nChoose an agent"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Choose list",
                        "emoji": True
                    },
                    "options": agent_options
                }
            },
            {
                "type": "section",
                "block_id": "group_section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":busts_in_silhouette: *Group*\nChoose a group"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Choose list",
                        "emoji": True
                    },
                    "options": group_options
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Create",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": "create",
                        "action_id": "create_button"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Cancel",
                            "emoji": True
                        },
                        "value": "cancel",
                        "action_id": "cancel_button"
                    }
                ]
            }
        ]
    }

    return create_ticket_ui

def generate_help_ui(user_id):
    help_ui = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Hey <@{user_id}>* 👋 I'm sDesk Bot. I'm here to help you create and manage tickets in sDesk.\nI'll provide you a help guide on how to get started :"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*:one: Use the `/login` command*. Type `/login` to authenticate you. Security is the number one priority, isn't it? :nerd_face: "
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*:two: Use the `/create` command*. Type `/create` to create a ticket in sDesk :sweat_smile: "
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*:three: Use the `/mytickets` command*. Type `/mytickets` to view all the tickets assigned to you in sDesk :face_with_monocle: "
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*:four: Use the `/comment` command*. Type `/comment` to comment on a specific ticket in sDesk. You have to specify the request id :writing_hand: "
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*:five: Use the `/resolve` command*. Type `/resolve` to close a ticket in sDesk :partying_face: "
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*:six: Use the `/getcomments` command*. Type `/getcomments` to view comments on a ticket in sDesk :thinking_face: "
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": ":question: Get help at any time with `/help` in a DM with me"
                    }
                ]
            }
        ]
    }

    return help_ui

def generate_login_ui(user_id):
    login_ui = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "App menu",
            "emoji": True
        },
        "callback_id": "login_cb",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Hey <@{user_id}>*, let me authorize you :technologist: :"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "input",
                "element": {
                    "type": "url_text_input",
                    "action_id": "sdesk_url_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": ":link: sDesk URL",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "sdesk_apikey_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": ":key: sDesk API key",
                    "emoji": True
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Login",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": "login",
                        "action_id": "login_button"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Cancel",
                            "emoji": True
                        },
                        "value": "cancel",
                        "action_id": "cancel_button"
                    }
                ]
            }
        ]
    }
    return login_ui

def generate_login_success_ui(user_id):
    login_success_ui = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Hey <@{user_id}>*, welcome! :wave:"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Great to see you here! I can help you to do multiple activites on sDesk right here within Slack. These are just a few things which you will be able to do:"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "• Create tickets \n • View your tickets \n • Comment on a ticket \n • Close a ticket \n • View comments on a ticket"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": ":question: Get help at any time with `/help` in a DM with me"
                    }
                ]
            }
        ]
    }

    return login_success_ui

def generate_login_error_ui():
    login_error_ui = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Error"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":warning: Failed to update sDesk URL and API key. Please try `/login` again."
                }
            }
        ]
    }

    return login_error_ui

def generate_slack_error_ui():
    slack_error_ui = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Error"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":warning: Slack validation failed. Please contact your admin."
                }
            }
        ]
    }

    return slack_error_ui

def generate_comment_ui(user_id):
    comment_ui = {
        "title": {
            "type": "plain_text",
            "text": "App menu",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "type": "modal",
        "callback_id": "login_cb",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Hey <@{user_id}>*, let's comment on a ticket in sDesk :"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "sdesk_ticket_id_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Enter request id"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": ":1234: sDesk Request ID",
                    "emoji": True
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": ":question: To get the request ids run `/mytickets` command and get the specific request id you want"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "sdesk_comment_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Enter comment"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": ":abcd: Comment",
                    "emoji": True
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Add Comment",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": "comment",
                        "action_id": "comment_button"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Cancel",
                            "emoji": True
                        },
                        "value": "cancel",
                        "action_id": "cancel_button"
                    }
                ]
            }
        ]
    }

    return comment_ui

def generate_close_ticket_ui(user_id):
    close_ticket_ui = {
        "title": {
            "type": "plain_text",
            "text": "App menu",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "type": "modal",
        "callback_id": "login_cb",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Hey <@{user_id}>*, let's close a ticket in sDesk :"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "sdesk_ticket_id_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Enter request id"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": ":1234: sDesk Request ID",
                    "emoji": True
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": ":question: To get the request ids run `/mytickets` command and get the specific request id you want"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "sdesk_comment_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Enter comment"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": ":abcd: Comment",
                    "emoji": True
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Close Ticket",
                            "emoji": True
                        },
                        "style": "danger",
                        "value": "resolve",
                        "action_id": "confirm_action_button_click"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Cancel",
                            "emoji": True
                        },
                        "value": "cancel",
                        "action_id": "cancel_button"
                    }
                ]
            }
        ]
    }

    return close_ticket_ui

def generate_confirmation_close_ticket_ui(user_id):
    confirmation_close_ticket_ui = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Confirmation"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Are you sure you want to proceed?"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Confirm",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": "confirm_action"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Cancel",
                            "emoji": True
                        },
                        "value": "cancel_action"
                    }
                ]
            }
        ]
    }

    return confirmation_close_ticket_ui

def generate_ticket_section(ticket):
    """
    Generate a Block Kit section for a single ticket.
    """
    ticket_section = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*Request Id:* {ticket['id']}\n*Ticket Id:* {ticket['local_request_id']}\n*Subject:* *_{ticket['subject']}_*\n"
        }
    }
    return ticket_section

def generate_ticket_details_section(ticket):
    """
    Generate a Block Kit section for detailed ticket information.
    """
    ticket_details_section = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*Requester:* {ticket['requester']}\n*Priority:* {ticket['priority']}\n*Status:* {ticket['status']}\n*Created On:* {ticket['datetime_created']}\n*Updated On:* {ticket['datetime_updated']}\n "
        }
    }

    return ticket_details_section

def generate_list_ui(ticket_data, user_id, page_num=1, items_per_page=10):
    """
    Generate Block Kit JSON for displaying a list of tickets.
    """
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hey <@{user_id}> :wave: here are your tickets in sDesk:\n"
            }
        }
    ]

    tickets = json.loads(ticket_data)
    total_pages = (len(tickets) + items_per_page - 1) // items_per_page
    
    start_index = (page_num - 1) * items_per_page
    end_index = min(start_index + items_per_page, len(tickets))
    
    # Generate sections for each ticket
    for ticket in tickets[start_index:end_index]:
        blocks.append(generate_ticket_section(ticket))
        blocks.append(generate_ticket_details_section(ticket))
        blocks.append({"type": "divider"})

     # Add pagination controls with page numbers
    pagination_block = {
        "type": "actions",
        "elements": []
    }

    for i in range(1, total_pages + 1):
        pagination_block["elements"].append({
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": str(i)
            },
            "action_id": f"page_button_clicked_{i}",
            "value": str(i)
        })

    blocks.append(pagination_block)
    
    return {"blocks": blocks}

def generate_no_tickets_found_ui():
    no_tickets_found_ui = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Information"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":relieved: No tickets assigned for you."
                }
            }
        ]
    }

    return no_tickets_found_ui

def generate_no_comments_found_ui():
    no_comments_found_ui = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Information"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":relieved: No comments found for the ticket."
                }
            }
        ]
    }

    return no_comments_found_ui

def generate_invalid_url_key_ui():
    invalid_url_key_ui = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Error"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":warning: Invalid sDesk URL and/or API key. Please execute `/login` command with your sDesk URL and API key."
                }
            }
        ]
    }

    return invalid_url_key_ui

def generate_error_ui(error=""):
    error_ui = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Error"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":warning: Unexpected error response received from sDesk. Please try again or contact the support. [Insight -> {error}]"
                }
            }
        ]
    }

    return error_ui

def generate_listing_error_ui():
    error_listing_ui = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Error"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":warning: Unexpected error response received from sDesk. Please try again or contact the support."
                }
            }
        ]
    }

    return error_listing_ui

def generate_succesful_comment_ui(ticket_id):
    succesful_comment_ui = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Information"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":smile: You have added a comment on ticket {ticket_id} ."
                }
            }
        ]
    }

    return succesful_comment_ui

def generate_resolved_comment_ui(ticket_id):
    succesful_comment_ui = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Information"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":tada: You have resolved ticket {ticket_id} ."
                }
            }
        ]
    }

    return succesful_comment_ui

def loading_ui():
    loading_ui = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "The request is processing.... :hourglass_flowing_sand:"
                },
            },
            # {
            #     "type": "image",
            #     "image_url": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTA5cW4xcWFwZXA1dDVzOGY5NHF3MHl4OWJvMjJpMTlreG5ia29sMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QBd2kLB5qDmysEXre9/giphy.gif",
            #     "alt_text": "Loading GIF"
            # }
        ]
    }

    return loading_ui

def update_group_dropdown_component(group_list):
    group_data = json.loads(group_list)

    group_options = [
        {
            "text": {
                "type": "plain_text",
                "text": group["name"]
            },
            "value": str(group["id"])
        } 
        for group in group_data["group"]
    ]

    update_group_dropdown = {
            "type": "section",
            "block_id": "group_section",
            "text": {
                "type": "mrkdwn",
                "text": ":busts_in_silhouette: *Group*\nChoose a group"
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Choose list",
                    "emoji": True
                },
                "options": group_options
            }
        }
    

    return update_group_dropdown

def generate_successful_creation_ui(ticket_id):
    succesful_creation_ui = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Information"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":sunglasses: Your ticket {ticket_id} has been created ."
                }
            }
        ]
    }

    return succesful_creation_ui

def generate_invaild_group_ui(ticket_id):
    invalid_group_ui = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Error"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":warning: Agent doesn't belong to the Group, please try again ."
                }
            }
        ]
    }

    return invalid_group_ui

def generate_search_ui(user_id):
    search_ui = {
        "title": {
            "type": "plain_text",
            "text": "App menu",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "type": "modal",
        "callback_id": "login_cb",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Hey <@{user_id}>*, let's get the latest comments on a ticket in sDesk :"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "sdesk_ticket_id_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Enter request id"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": ":1234: sDesk Request ID",
                    "emoji": True
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": ":question: To get the request ids run `/mytickets` command and get the specific request id you want"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Search",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": "getcomments",
                        "action_id": "search_button"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Cancel",
                            "emoji": True
                        },
                        "value": "cancel",
                        "action_id": "cancel_button"
                    }
                ]
            }
        ]
    }

    return search_ui

def generate_comment_section(comment):
    """
    Generate a Block Kit section for a single comment.
    """
    comment_section = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*Request Id:* {comment['requestid']}\n*Ticket Id:* {comment['localrequestid']}\n*Comment:* *_{comment['bodytext']}_*\n"
        }
    }
    return comment_section

def generate_comment_details_section(comment):
    """
    Generate a Block Kit section for detailed comment information.
    """
    comment_details_section = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*Commented By:* {comment['agentname']}\n*Commented On:* {comment['datetime_created']}\n*From (Name):* {comment['fromname']}\n*From (Email):* {comment['fromemail']}\n*Type:* {'Internal' if comment['threadtype'] == 3 else 'External'}\n "
        }
    }

    return comment_details_section

def generate_comment_list_ui(comment_data, user_id, page_num=1, items_per_page=10):
    """
    Generate Block Kit JSON for displaying a list of comments.
    """
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hey <@{user_id}> :wave: here are your comments in sDesk:\n"
            }
        }
    ]

    comments = json.loads(comment_data)
    total_pages = (len(comments) + items_per_page - 1) // items_per_page
    
    start_index = (page_num - 1) * items_per_page
    end_index = min(start_index + items_per_page, len(comments))
    
    # Generate sections for each ticket
    for comment in comments[start_index:end_index]:
        blocks.append(generate_comment_section(comment))
        blocks.append(generate_comment_details_section(comment))
        blocks.append({"type": "divider"})

     # Add pagination controls with page numbers
    pagination_block = {
        "type": "actions",
        "elements": []
    }

    data = json.loads(comment_data)
    val = "getcomments "+ str(data[0]['requestid'])

    for i in range(1, total_pages + 1):
        pagination_block["elements"].append({
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": str(i)
            },
            "action_id": f"page_button_clicked_{i}",
            "value": val
        })

    blocks.append(pagination_block)
    
    return {"blocks": blocks}