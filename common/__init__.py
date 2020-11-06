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



class SmsRecieved(object):
    
    def __init__(self, raw_event):
        self.id = raw_event['id']
        self.topic = raw_event['topic']
        self.subject = raw_event['subject']
        self.data = SmsData(raw_event_data=raw_event['data'])
        self.event_type = raw_event['eventType']
        self.data_version = raw_event['dataVersion']
        self.metadata_version = raw_event['metadataVersion']
        self.event_time = raw_event['eventTime']
    

class SmsData(object):

    def __init__(self, raw_event_data):
        self.message_id = raw_event_data['messageId']
        self.message_from = raw_event_data['from']
        self.message_to = raw_event_data['to']
        #self.delivery_status = raw_event_data['deliveryStatus']
        #self.delivery_status_details = raw_event_data['deliveryStatusDetails']
        self.received_timestamp = raw_event_data['receivedTimestamp']
        self.message = raw_event_data['message']
        #self.delivery_attempts = [DeliveryAttempt(raw_delivery_attempt=delivery_attempt) for delivery_attempt in raw_event_data['deliveryAttempts']]

class DeliveryAttempt(object):

    def __init__(self, raw_delivery_attempt):
        self.timestamp = raw_delivery_attempt['timestamp']
        self.segments_succeeded = raw_delivery_attempt['segmentsSucceeded']
        self.segments_failed = raw_delivery_attempt['segementsFalied']

