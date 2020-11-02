from azure import functions as func
from azure.communication.sms import PhoneNumber, SendSmsOptions, SmsClient
from datetime import datetime, timezone
from logging import info
from os import environ


class SimpleMessagingService:

    def __init__(self, leased_phone_number, to_phone_number, comm_service_connection_string):
        self.leased_phone_number = leased_phone_number
        self.to_phone_number = to_phone_number
        self.connection_string = comm_service_connection_string
        self.sms_client = SmsClient.from_connection_string(self.connection_string)

    def send_sms(self, message_to_send: str):
        sms_response = self.sms_client.send(
            from_phone_number=PhoneNumber(self.leased_phone_number),
            to_phone_numbers=[PhoneNumber(self.to_phone_number)],
            message=message_to_send,
            send_sms_options=SendSmsOptions(enable_delivery_report=True))
        return sms_response

def main(sendMessageTimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()

    if sendMessageTimer.past_due:
        info('The timer is past due!')

    sms = SimpleMessagingService(
        leased_phone_number=environ['LEASED_PHONE_NUMBER'],
        to_phone_number=environ['TO_PHONE_NUMBER'],
        comm_service_connection_string=environ['COMM_SERVICE_CONNECTION_STRING']
    )
    sms.send_sms(message_to_send=f'Message from function App {utc_timestamp}')
    info('Python timer trigger function ran at %s', utc_timestamp)
