import json
import os
import requests
from flask import abort
from classes.ticket import Ticket
from mapper import get_endpoints, post_endpoints
import jsonpickle
import logging

from storage import get_record, insert_records, store_data, retrieve_data
logger = logging.getLogger(__name__)

# @celery.task
def get_agents(url):
    if "agentusers" in get_endpoints: 
        response = requests.get(url)
        return response
    else:
        pass

def get_navigation_types(url):
    if "navigationtypes" in get_endpoints: 
        response = requests.get(url)
        return response
    else:
        pass

def get_options(url):
    if "options" in post_endpoints: 
        response = requests.post(url)
        return response
    else:
        pass

def get_groups(url):
    if "groups" in get_endpoints:
        response = requests.get(url)
        return response
    else:
        pass

def get_user_details(url):
    if "userdetails" in get_endpoints:
        response = requests.get(url)
        return response
    else:
        pass

def get_ticket_comments(url):
    if "getcomments" in get_endpoints:
        response = requests.get(url)
        return response
    else:
        pass