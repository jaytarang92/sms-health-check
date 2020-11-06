from azure.communication.sms import PhoneNumber, SendSmsOptions, SmsClient, SendSmsResponse

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
