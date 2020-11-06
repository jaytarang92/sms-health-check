from datetime import datetime, timezone
from json import loads
from logging import info
from os import environ
from azure import functions as func
from ..common import SimpleMessagingService
from ..common.models import SmsRecieved

def main(msg: func.ServiceBusMessage):
    sms_event_data = SmsRecieved(loads(msg.get_body().decode('utf-8')))
    sms = SimpleMessagingService(
        leased_phone_number=environ['LEASED_PHONE_NUMBER'],
        target_phone_numbers=environ['TARGET_PHONE_NUMBERS'],
        comm_service_connection_string=environ['COMM_SERVICE_CONNECTION_STRING']
    )
    sms.send_sms(message_to_send=f'Sent from {sms_event_data.data.message_from}: {sms_event_data.data.message}')
