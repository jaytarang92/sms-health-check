from datetime import datetime, timezone
from logging import info
from os import environ
from azure import functions as func
from ..common import SimpleMessagingService

def main(sendMessageTimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()

    if sendMessageTimer.past_due:
        info('The timer is past due!')

    sms = SimpleMessagingService(
        leased_phone_number=environ['LEASED_PHONE_NUMBER'],
        target_phone_numbers=environ['TARGET_PHONE_NUMBERS'],
        comm_service_connection_string=environ['COMM_SERVICE_CONNECTION_STRING']
    )
    sms.send_sms(message_to_send=f'Message from FunctionApp sent at: {utc_timestamp}')
    info(f'Message was successfully sent at: {utc_timestamp}')
