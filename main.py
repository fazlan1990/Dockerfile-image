import asyncio
import json
from threading import Thread

from flask import Flask, jsonify, request
import requests
# from celeryworker import make_celery
from controller import process_command, send_acknowledgment
from security import validate_slack_request
from logger import configure_logger 
from uigenerator import generate_slack_error_ui, loading_ui

app = Flask(__name__)
logger = configure_logger()
app.debug=True

# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# celery = make_celery(app)

# workspaces = {
#     "workspace1_id": {"name": "iVedha", "access_token": "access_token_1"},
#     "workspace2_id": {"name": "Workspace 2", "access_token": "access_token_2"},
#     # Add more workspaces as needed
# }

# def authenticate_workspace(workspace_id, access_token):
#     # Check if workspace ID exists and access token matches
#     if workspace_id in workspaces and workspaces[workspace_id]["access_token"] == access_token:
#         return True
#     return False

# @app.before_request
# def check_workspace_auth():
#     workspace_id = request.headers.get("X-Slack-Team-ID")  # Extract workspace ID from request headers
#     access_token = request.headers.get("Authorization")  # Extract access token from request headers
#     if not workspace_id or not access_token:
#         abort(401)  # Unauthorized if workspace ID or access token is missing
#     if not authenticate_workspace(workspace_id, access_token):
#         abort(403)  # Forbidden if authentication fails for the workspace

# @app.route("/slack", methods=["POST"])
# def interactive_controller():
#     # Extract payload from the request
#     payload = request.form.to_dict()


#     nested_dict_str = payload.get("payload", {})
#     # Convert the string to a dictionary object
#     nested_dict = json.loads(nested_dict_str)

#     # Extract trigger_id from the payload
#     trigger_id = nested_dict.get("trigger_id")

#     # Construct your Block Kit UI JSON
#     block_kit_json = {
#         "trigger_id": trigger_id,
#         "view": {
#             "type": "modal",
#             "title": {
#                 "type": "plain_text",
#                 "text": "My Modal"
#             },
#             "blocks": [
#                 {
#                     "type": "section",
#                     "text": {
#                         "type": "mrkdwn",
#                         "text": "Hello from your Flask app!"
#                     }
#                 }
#             ],
#             "callback_id": "modal-identifier"
#         }
#     }

#     requests.post(nested_dict["response_url"], json=block_kit_json)

#     # Send the Block Kit UI JSON as the response to Slack
#     return ""


# @app.route("/slack/login", methods=["POST"])
# def slash_response():                
#     """ endpoint for receiving all slash command requests from Slack """

#     # blocks defintion from message builder
#     # converting from JSON to array
#     blocks = json.loads("""[
#         {
#             "type": "section",
#             "text": {
#                 "type": "plain_text",
#                 "text": "Please select an option:",
#                 "emoji": true
#             }
#         },
#         {
#             "type": "actions",
#             "elements": [
#                 {
#                     "type": "button",
#                     "text": {
#                         "type": "plain_text",
#                         "text": "Click me",
#                         "emoji": true
#                     },
#                     "value": "button_1"
#                 }
#             ]
#         }
#     ]""")

#     # compose response message    
#     response = {
#         "blocks": blocks
#     }

#     ## convert response message into JSON and send back to Slack
#     return jsonify(response)

@app.route("/slack", methods=["POST"])
def interactive_response():                
    data = json.loads(request.form["payload"])
    actions = data.get("actions")
    command = actions[0].get("value")
    if (command == None and actions[0].get("action_id") == "type_select") or command == "create":
        command = "create"
        thr = Thread(target=process_command, args=[request.form,command])
        thr.start()
        return ""
    elif actions[0].get("action_id").startswith('page_button_clicked'):
        if command:
            command = command
        else:
            command = "mytickets"
        response = process_command(request, command)
    response = process_command(request, command)
    requests.post(data["response_url"], json=response)
    return ""

@app.route("/slack/<command>", methods=["POST"])
def slack_command(command):
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Slack Command: %s", command)
    
    is_valid = validate_slack_request(request)
    logger.info("Is Valid: %s", is_valid)
    # await asyncio.sleep(1)
    # is_valid = True
    if (is_valid):
        if (command == "create"):
            thr = Thread(target=process_command, args=[request.form,command])
            thr.start()
            return loading_ui()
        response = process_command(request, command)
        print(response)
        return jsonify(response)
    else:
        response = generate_slack_error_ui()
        return response
    
@app.route("/health", methods=["GET"])
def health_check():                
    return jsonify({'status': 'ok'}), 200