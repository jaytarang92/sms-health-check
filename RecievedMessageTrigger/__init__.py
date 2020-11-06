from datetime import datetime, timezone
from logging import info
from os import environ
from azure import functions as func
from ..common import SimpleMessagingService, SmsRecieved
from json import loads

def main(msg: func.ServiceBusMessage):
    sms_event_data = SmsRecieved(loads(msg.get_body().decode('utf-8')))
    sms = SimpleMessagingService(
        leased_phone_number=environ['LEASED_PHONE_NUMBER'],
        target_phone_numbers=environ['TARGET_PHONE_NUMBERS'],
        comm_service_connection_string=environ['COMM_SERVICE_CONNECTION_STRING']
    )
    sms.send_sms(message_to_send=f'Sent from Other Function: {sms_event_data.data.message}')
