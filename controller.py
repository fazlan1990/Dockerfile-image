import json
import os
from urllib.parse import parse_qs
import requests
from flask import abort, jsonify
from classes.agent import Agent
from classes.ticket import Ticket
from classes.comment import Comment
from data import get_agents, get_groups, get_navigation_types, get_options, get_ticket_comments, get_user_details
from mapper import get_endpoints, post_endpoints
import jsonpickle
from uigenerator import generate_close_ticket_ui, generate_comment_list_ui, generate_comment_ui, generate_create_ticket_ui, generate_error_ui, generate_help_ui, generate_invaild_group_ui, generate_invalid_url_key_ui, generate_list_ui, generate_listing_error_ui, generate_login_error_ui, generate_login_success_ui, generate_login_ui, generate_no_comments_found_ui, generate_no_tickets_found_ui, generate_resolved_comment_ui, generate_search_ui, generate_succesful_comment_ui, generate_successful_creation_ui, update_group_dropdown_component

import logging

from storage import get_record, insert_records
logger = logging.getLogger(__name__)

def process_command(request, command):
    logger.info("Processing command")

    try:
        if command == "login":
            logger.info("Login in progess")
            
            if request.form.get("payload") is not None:
                payload = json.loads(request.form["payload"])
                username = payload["user"]["username"]
                team_domain = payload["team"]["domain"]
                user_id = payload["user"]["id"]

                if payload["type"] == "block_actions":
                    for key, value in payload["state"]["values"].items():
                        # Check if the key contains the required value
                        if "sdesk_url_input" in value:
                            sdesk_url = value["sdesk_url_input"]["value"]
                        elif  "sdesk_apikey_input" in value:
                            sdesk_api_key = value["sdesk_apikey_input"]["value"]

                    # Store API Key in Redis
                    insert_records(username, team_domain, sdesk_url, sdesk_api_key)
                    stored_sdesk_url, stored_sdesk_api_key = get_record(username, team_domain)

                    if sdesk_api_key != stored_sdesk_api_key and sdesk_url != stored_sdesk_url:
                        logger.error("Failed to update sDesk URL and API key")
                        response = generate_login_error_ui()
                    else:
                        # Process the sDesk URL and API key as needed
                        response = generate_login_success_ui(user_id)
            else:
                user_id = request.form["user_id"]
                response = generate_login_ui(user_id)
            return response

        elif command == "help":
            user_id = request.form["user_id"]
            response = generate_help_ui(user_id)
            return response
        
        elif command.startswith("getcomments"):
            logger.info("Searching in GET endpoints")
            
            if request.form.get("payload") is not None:
                payload = json.loads(request.form["payload"])
                username = payload["user"]["username"]
                team_domain = payload["team"]["domain"]
                user_id = payload["user"]["id"]

                # Split the command string
                parts = command.split()

                # Check if there are two parts
                if len(parts) == 2:
                    # Assign values to separate variables
                    command, ticket_id = parts

                else:
                    # If there's only one part, assign it as the operation and set request_id to None
                    command = parts[0]
                    ticket_id = None
                
                api_endpoint = get_endpoints[command]

                if payload["type"] == "block_actions":
                    for key, value in payload["state"]["values"].items():
                        # Check if the key contains the required value
                        if "sdesk_ticket_id_input" in value:
                            ticket_id = value["sdesk_ticket_id_input"]["value"]

                    action = payload['actions'][0]
                    
                    api_endpoint_details = api_endpoint.replace("{request_id}", ticket_id)
                    stored_sdesk_url, stored_sdesk_api_key = get_record(username, team_domain)
                    api_url = stored_sdesk_url + api_endpoint_details + "?apikey=" + stored_sdesk_api_key
                    
                    response = get_ticket_comments(api_url)

                    if (response.status_code == 401):
                        dto = generate_invalid_url_key_ui()
                        return dto
                    dto = process_json(response.content, Comment, "ThreadItems")
                    if dto == "[]":
                        dto = generate_no_comments_found_ui()
                    elif action['action_id'].startswith('search_button'):
                        dto = generate_comment_list_ui(dto, user_id)
                    elif action['action_id'].startswith('page_button_clicked'):
                        # Extract the page number from the action value
                        page_num = int(action['text']['text'])
                        
                        # Generate Block Kit UI for the new page
                        dto = generate_comment_list_ui(dto, user_id, page_num) 
                    return dto
            else:
                user_id = request.form["user_id"]
                response = generate_search_ui(user_id)
                return response
        elif command in get_endpoints:
            if request.form.get("payload") is not None: 
                api_endpoint = get_endpoints[command]               
                payload = json.loads(request.form["payload"])
                action = payload['actions'][0]
                username = payload["user"]["username"]
                team_domain = payload["team"]["domain"]
                user_id = payload["user"]["id"]

                stored_sdesk_url, stored_sdesk_api_key = get_record(username, team_domain)
                api_url = stored_sdesk_url + api_endpoint + "&apikey=" + stored_sdesk_api_key
                response = requests.get(api_url)

                if (response.status_code == 401):
                    dto = generate_invalid_url_key_ui()
                    return dto
                dto = process_json(response.content, Ticket)
                if dto == "[]":
                    dto = generate_no_tickets_found_ui()
                else:
                    if action['action_id'].startswith('page_button_clicked'):
                        # Extract the page number from the action value
                        page_num = int(action['value'])
                        
                        # Generate Block Kit UI for the new page
                        dto = generate_list_ui(dto, user_id, page_num)
                return dto
            else:            
                logger.info("Searching in GET endpoints")
                api_endpoint = get_endpoints[command]

                username = request.form["user_name"]
                team_domain = request.form["team_domain"]
                user_id = request.form["user_id"]
                
                stored_sdesk_url, stored_sdesk_api_key = get_record(username, team_domain)
                api_url = stored_sdesk_url + api_endpoint + "&apikey=" + stored_sdesk_api_key
                response = requests.get(api_url)
                
                if (response.status_code == 401):
                    dto = generate_invalid_url_key_ui()
                    return dto
                dto = process_json(response.content, Ticket)
                if dto == "[]":
                    dto = generate_no_tickets_found_ui()
                else:
                    dto = generate_list_ui(dto, user_id)
                return dto
        
        elif command == "refresh":
            pass
        elif command == "create":
            if request.get("payload") is not None:
                logger.info("Searching in POST endpoints")
                api_endpoint = post_endpoints[command]
                
                payload = json.loads(request["payload"])
                username = payload["user"]["username"]
                team_domain = payload["team"]["domain"]
                print(payload)
                subject_input_value = None
                description_input_value = None
                requester_section_value = None
                type_section_value = None
                agent_section_value = None
                group_section_value = None
               
               
                for key, value in payload['state']['values'].items():
                    if "subject_input" in value:
                        subject_input_value = value['subject_input']['value']
                        break
                for key, value in payload['state']['values'].items():    
                    if "description_input" in value:
                         description_input_value = value['description_input']['value']
                         break
                    
                # Extracting values dynamically from group_section
                group_section_key = next(iter(payload['state']['values']['group_section']))
                group_section_value = payload['state']['values']['group_section'][group_section_key]['selected_option']['value']
                
                # Extracting values dynamically from type_section
                type_section_key = next(iter(payload['state']['values']['type_section']))
                type_section_value = payload['state']['values']['type_section'][type_section_key]['selected_option']['value']
                
                # Extracting values dynamically from requester_section
                requester_section_key = next(iter(payload['state']['values']['requester_section']))
                requester_section_value = payload['state']['values']['requester_section'][requester_section_key]['selected_option']['value']
                
                # Extracting values dynamically from agent_section
                agent_section_key = next(iter(payload['state']['values']['agent_section']))
                agent_section_value = payload['state']['values']['agent_section'][agent_section_key]['selected_option']['value']

                print("group_section_value:", group_section_value)
                print("type_section_value:", type_section_value)
                print("requester_section_value:", requester_section_value)
                print("description_input_value:", description_input_value)
                print("subject_input_value:", subject_input_value)
                print("agent_section_value:", agent_section_value)

                req_payload = {"TypeId":type_section_value,
                                "RequestSubject":subject_input_value,
                                "RequestBody":description_input_value,
                                "RequesterId":requester_section_value,
                                "AgentId":agent_section_value,
                                "GroupId":group_section_value}
                
                print("Req Payload: ", req_payload)

                stored_sdesk_url, stored_sdesk_api_key = get_record(username, team_domain)
                
                # Validate User's Group
                api_endpoint_details = get_endpoints["userdetails"]
                api_endpoint_details = api_endpoint_details.replace("{user_id}", agent_section_value)
                api_url = stored_sdesk_url + api_endpoint_details + "?apikey=" + stored_sdesk_api_key
                user_details_response = get_user_details(api_url)
                user_details = json.loads(user_details_response.text)

                user_groups = user_details.get('AgentGroups', [])

                # Check if the ID matches any AgentGroups id
                id_found = any(group_section_value == str(group['id']) for group in user_groups)

                response_url = payload["response_url"]

                if id_found:
                    print(f"The ID {group_section_value} matches an ID in AgentGroups.")
                else:
                    error_ui_response = generate_invaild_group_ui(group_section_value)
                    requests.post(response_url,json=error_ui_response)
                    return ""

                # Create ticket in sDesk
                api_url = stored_sdesk_url + api_endpoint + "?apikey=" + stored_sdesk_api_key
                response = requests.post(api_url, json=req_payload)

                if (response.status_code == 401):
                    ui_resp = generate_invalid_url_key_ui()
                    requests.post(response_url,json=ui_resp)
                elif (response.status_code == 400):
                    ui_resp = generate_error_ui(response.text)
                    requests.post(response_url,json=ui_resp)
                else:
                    print(response.text)
                    response = json.loads(response.text)
                    ui_response = generate_successful_creation_ui(str(response["Id"])) 
                    requests.post(response_url,json=ui_response)

            else:
                username = request["user_name"]
                team_domain = request["team_domain"]
                response_url = request["response_url"]
                user_id = request["user_id"]
                stored_sdesk_url, stored_sdesk_api_key = get_record(username, team_domain)
                
                api_endpoint = get_endpoints["agentusers"]
                api_url = stored_sdesk_url + api_endpoint + "?apikey=" + stored_sdesk_api_key
                agents_response = get_agents(api_url)

                api_endpoint = get_endpoints["navigationtypes"]
                api_url = stored_sdesk_url + api_endpoint + "?apikey=" + stored_sdesk_api_key
                types_response = get_navigation_types(api_url)

                api_endpoint = get_endpoints["groups"]
                api_url = stored_sdesk_url + api_endpoint + "?apikey=" + stored_sdesk_api_key
                groups_response = get_groups(api_url)

                if (agents_response.text == None or types_response.text == None or groups_response.text == None):
                    ui_resp = generate_listing_error_ui()
                    requests.post(response_url,json=ui_resp) 

                response = generate_create_ticket_ui(user_id, agents_response.text, types_response.text, groups_response.text)
                requests.post(response_url,json=response)  

        elif command in post_endpoints: 
            logger.info("Searching in POST endpoints")
            api_endpoint = post_endpoints[command]

            if request.form.get("payload") is not None:
                payload = json.loads(request.form["payload"])
                username = payload["user"]["username"]
                team_domain = payload["team"]["domain"]

                if payload["type"] == "block_actions":
                    for key, value in payload["state"]["values"].items():
                        # Check if the key contains the required value
                        if "sdesk_ticket_id_input" in value:
                            ticket_id = value["sdesk_ticket_id_input"]["value"]
                        elif  "sdesk_comment_input" in value:
                            comment = value["sdesk_comment_input"]["value"]
                    
                    stored_sdesk_url, stored_sdesk_api_key = get_record(username, team_domain)
                    api_endpoint = api_endpoint.replace("{request_id}", ticket_id)
                    api_url = stored_sdesk_url + api_endpoint + "?apikey=" + stored_sdesk_api_key

                    logger.info("Processing request, %s",api_url)
                    content = {"Attachments":[], "SecondsElapsed":"100", "Text": "<p>"+comment+"</p>"}
                    response = requests.post(api_url, json=content)
                    
                    if (response.status_code == 401):
                        dto = generate_invalid_url_key_ui()
                        return dto
                    if (response.status_code == 400):
                        dto = generate_error_ui(response.text)
                        return dto
                    if (command=="resolve"):
                        dto = generate_resolved_comment_ui(ticket_id)
                    elif(command=="comment"):
                        dto = generate_succesful_comment_ui(ticket_id)
                    return dto     
            else:
                user_id = request.form["user_id"]
                if (command=="resolve"):
                    response = generate_close_ticket_ui(user_id)
                elif(command=="comment"):
                    response = generate_comment_ui(user_id)
                else:
                    response = {"":""}
            return response
        else:
            logger.error("Command not found: %s", command)
            response = {"":""}
            return response
    except Exception as error:
        logger.error("Error while processing command: %s", error)
        abort(500, "Error occcured while processing command")

def process_json(json_string, object, key=None):
    try:
        logger.info("Processing JSON encoding")
        # Decode the bytes object into a string
        json_string_decoded = json_string.decode("utf-8")

        # Parse the JSON string into a Python dictionary
        json_string = json.loads(json_string_decoded)

        if "Results" in json_string:
            data_array = json_string["Results"]
        elif key is not None:
            if key in json_string:
                data_array = json_string[key] 
        else:
            data_array = json_string
        objects = []
        
        for data in data_array:
            value = object(**data)
            objects.append(value)
        
        json_object = jsonpickle.encode(objects, unpicklable=False, indent=4)

        return json_object
    except KeyError:
        logger.error("Results key not found: {json_string}")
        abort(500, "Results key not found in JSON string")
    except Exception as e:
        logger.error(f"Failed to process json {e}")
        abort(500, "Failed to process json")

def send_acknowledgment(response_url):
    # Craft your acknowledgment message
    acknowledgment_message = {
        'text': 'Your request is being processed...'
    }

    # Send the acknowledgment message to Slack
    requests.post(response_url, json=acknowledgment_message)
    return ""
