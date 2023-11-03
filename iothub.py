import base64
import hmac
import urllib.parse
import time


class IotHub():
    # Initialize the IoT Hub class with the address, device ID, and shared access key.
    def __init__(self, hub_address, device_id, shared_access_key):
        # Shared access key for authentication
        self.shared_access_key = shared_access_key
        # Create the endpoint URL for the device
        self.endpoint = hub_address + '/devices/' + device_id
        # Set the MQTT username as the hub address and device ID
        self.hub_user = hub_address + '/' + device_id
        # Define the MQTT topic to publish to
        self.hub_topic_publish = 'devices/' + device_id + '/messages/events/'
        # Define the MQTT topic to subscribe to for devicebound messages
        self.hub_topic_subscribe = 'devices/' + device_id + '/messages/devicebound/#'

    # SAS Token Generator Method
    # sas generator from https://github.com/bechynsky/AzureIoTDeviceClientPY/blob/master/DeviceClient.py
    def generate_sas_token(self, expiry=3600):
        # Determine the time when the token will expire (current time + expiry seconds)
        ttl = int(time.time()) + expiry
        # Encode the endpoint URL to be used in the signature
        url_to_sign = urllib.parse.quote(self.endpoint, safe='')
        # Create the string to sign with the encoded URL and the expiry timestamp
        sign_shared_access_key = "%s\n%d" % (url_to_sign, int(ttl))
        # Use HMAC-SHA256 to create a signature from the string to sign
        h = hmac.new(base64.b64decode(self.shared_access_key), msg="{0}\n{1}".format(
            url_to_sign, ttl).encode('utf-8'), digestmod='sha256')
        # URL-encode the base64-encoded signature to get the final signature part of the token
        signature = urllib.parse.quote(base64.b64encode(h.digest()), safe='')
        # Construct the full SAS token with the encoded URL, signature, and expiry time
        return "SharedAccessSignature sr={0}&sig={1}&se={2}".format(url_to_sign, signature, ttl)
