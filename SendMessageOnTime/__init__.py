from azure import functions as func
from azure.communication.sms import PhoneNumber, SendSmsOptions, SmsClient, SendSmsResponse
from datetime import datetime, timezone
from logging import info
from os import environ


class SimpleMessagingService:

    def __init__(self, leased_phone_number, target_phone_numbers, comm_service_connection_string):
        self.leased_phone_number = leased_phone_number
        self.target_phone_numbers = target_phone_numbers
        self.connection_string = comm_service_connection_string
        self.sms_client = SmsClient.from_connection_string(self.connection_string)

    def send_sms(self, message_to_send: str, delivery_report_bool: bool = False) -> SendSmsResponse:
        sms_response = self.sms_client.send(
            from_phone_number=PhoneNumber(self.leased_phone_number),
            to_phone_numbers=[PhoneNumber(phone_number) for phone_number in self.target_phone_numbers.split(',')],
            message=message_to_send,
            send_sms_options=SendSmsOptions(enable_delivery_report=delivery_report_bool))
        print(sms_response.__dict__)
        return sms_response

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
