class Config():
    # The constructor takes a connection string and parses it into a configuration dictionary.
    def __init__(self, connectionString):
        # The connection string is split into parts separated by semi-colons,
        # then each part is split by the first equal sign into key and value,
        # and added into a dictionary. This dictionary will contain the components
        # of the connection string such as HostName, DeviceId, and SharedAccessKey.
        self.config = dict(map(lambda x: x.split(
            '=', 1), connectionString.split(';')))

    # The @property decorator is used to define a getter for the IoT hub address.
    # When 'hub_address' is accessed, it returns the 'HostName' part of the connection string.
    @property
    def hub_address(self):
        return self.config['HostName']

    # The @property decorator is used to define a getter for the device ID.
    # When 'device_id' is accessed, it returns the 'DeviceId' part of the connection string.
    @property
    def device_id(self):
        return self.config['DeviceId']

    # The @property decorator is used to define a getter for the shared access key.
    # When 'shared_access_key' is accessed, it returns the 'SharedAccessKey' part of the connection string.
    @property
    def shared_access_key(self):
        return self.config['SharedAccessKey']
