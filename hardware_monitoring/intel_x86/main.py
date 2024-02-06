#!/usr/bin/env python
# Markham Lee (C) 2023
# K3s Data Platform
# https://github.com/MarkhamLee/k3s-data-platform-IoT
# Script to monitor the CPU and NVME temperatures on Intel x86 Nodes
# only monitoring temps with this for now as the Prometheus stack
# handles the rest: compute, disk space, ram, etc.

import time
import gc
import logging
import os
from intel_x86 import Intelx86
from influxdb_client import Point

# create logger for logging errors, exceptions and the like
logging.basicConfig(filename='hardwareDataLinuxCPU.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s\
                        : %(message)s')


def monitor(client: object, get_data: object, BUCKET: str, ORG: str,
            TABLE: str):

    while True:

        time.sleep(5)

        # get CPU, GPU and NVME temperatures
        core_temp, nvme_temp = get_data.getTemps()

        point = (
            Point(TABLE)
            .tag("cluster_nodes", "node temps")
            .field("nvme_temp", nvme_temp)
            .field("core_temp", core_temp)
        )

        client.write(bucket=BUCKET, org=ORG, record=point)

        del nvme_temp, core_temp
        gc.collect()


def main():

    TOKEN = os.environ['TOKEN']
    ORG = os.environ['ORG']
    URL = os.environ['URL']
    BUCKET = os.environ['BUCKET']
    TABLE = os.environ['TABLE']

    # instantiate utilities class
    device_data = Intelx86()

    # get client
    client = device_data.influx_client(TOKEN, ORG, URL)

    monitor(client, device_data, BUCKET, ORG, TABLE)


if __name__ == '__main__':
    main()
