import os
from twilio.rest import Client
import logging
import requests

logger = logging.getLogger()


# Sending an SMS
def send_Mes():
    url = "https://www.fullstack.co.il/smsGateWay.php"

    params = {
        'token': 's5gjs84rjfoewjru4',
        'to': '0547630500',
        'message': 'Violation of rules'
    }

    response = requests.get(url, params = params)
