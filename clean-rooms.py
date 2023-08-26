#! python3

import dreame
import mock
import yaml

# create a device from the config file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

device = dreame.DreameVacuumDevice(**config)

try:
    # connect to the device locally
    device.connect_device()

    # connect to the cloud while mocking MD5 hashing to allow using hashes
    # instead of plain text passwords in the config
    @mock.patch('hashlib.md5')
    def connect_cloud_mock_md5(md5_mock):
        md5_mock.return_value.hexdigest.return_value = config['password']
        device.connect_cloud()

    connect_cloud_mock_md5()
finally:
    # stop the communication with the device
    device.disconnect()
