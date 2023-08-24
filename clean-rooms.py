#! python3

import dreame
import yaml

# create a device from the config file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

device = dreame.DreameVacuumDevice(**config)

try:
    # connect to the device locally and the through the cloud
    device.connect_device()
    device.connect_cloud()
finally:
    # stop the communication with the device
    device.disconnect()
