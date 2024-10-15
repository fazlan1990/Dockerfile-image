import asyncio
import hashlib
import hmac
import os
from dotenv import find_dotenv, load_dotenv

def validate_slack_request(request):
    
    import logging
    logger = logging.getLogger(__name__)
    load_dotenv(find_dotenv(), verbose=True)
    is_valid = False
    request_body = request.get_data().decode("utf-8")

    logger.info("validate_slack_request")

    # Verify request from Slack
    slack_signature = request.headers.get("X-Slack-Signature")
    timestamp = request.headers.get("X-Slack-Request-Timestamp")
    sig_basestring = f"v0:{timestamp}:{request_body}".encode("utf-8")
    slack_signing_secret = os.getenv("SLACK_SECRET")
    my_signature = "v0=" + hmac.new(slack_signing_secret.encode("utf-8"), sig_basestring, hashlib.sha256).hexdigest()

    if hmac.compare_digest(my_signature, slack_signature):
        is_valid = True

    # await asyncio.sleep(1)
    return is_valid