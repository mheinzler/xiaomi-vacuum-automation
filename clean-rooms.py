#! python3

import argparse
import dreame
import logging
import mock
import time
import yaml

SLEEP_INTERVAL = 0.25

# parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', metavar='FILE',
                    default='config.yaml',
                    help='device configuration file (default: config.yaml)')
parser.add_argument('-t', '--timeout', metavar='SECONDS', type=int,
                    default=10,
                    help='timeout for map retrieval (default: 10 seconds)')

parser.add_argument('-v', '--verbose',
                    default=logging.WARNING,
                    dest='loglevel', action='store_const', const=logging.INFO,
                    help='enable verbose output')
parser.add_argument('-d', '--debug',
                    dest='loglevel', action='store_const', const=logging.DEBUG,
                    help='enable debug output')

args = parser.parse_args()

# configure logging
logging.basicConfig(
    level=args.loglevel,
    format='%(asctime)s %(name)-13s %(levelname)-8s %(message)s')

# create a device from the config file
with open(args.config, 'r') as file:
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

    # wait for the map to be available
    logging.info('Waiting for map ...')
    status = device.status
    for i in range(int(args.timeout / SLEEP_INTERVAL)):
        if status.current_map:
            break

        time.sleep(SLEEP_INTERVAL)

    if status.current_map:
        logging.info('Received map from device')

        segments = status.segments
        logging.info('Rooms: %s',
                     [[id, seg.name] for id, seg in segments.items()])
    else:
        logging.error('Timeout while waiting for map')
finally:
    # stop the communication with the device
    device.disconnect()
