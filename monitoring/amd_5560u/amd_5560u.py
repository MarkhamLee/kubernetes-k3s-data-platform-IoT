# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/k3s-data-platform-IoT
# script to retrieve CPU related data on an AMD x86 machine
# and then write to InfluxDB

import psutil
import logging
import influxdb_client # noqa E402
from influxdb_client.client.write_api import SYNCHRONOUS

# create logger for logging errors, exceptions and the like
logging.basicConfig(filename='hardwareDataLinuxCPU.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s\
                        : %(message)s')


class AMD5560Data():

    def __init__(self):

        # get the # of cores, as we can use that to iterate through and
        # get things like current speed for all CPU cores
        self.core_count = psutil.cpu_count(logical=False)

    # get average clock speed for all cores
    def getFreq(self, all_cpu=False):

        all_freq = psutil.cpu_freq(percpu=all_cpu)[0]
        all_freq = round(all_freq, 1)

        return all_freq, self.core_count

    # get frequency per core
    @staticmethod
    def freqPerCore(self, all_cpu=True):

        per_core_freq = self.buildPayload(psutil.cpu_freq(percpu=all_cpu))

        return per_core_freq

    # CPU load
    @staticmethod
    def getCPUData():

        cpu_util = (psutil.cpu_percent(interval=1))
        cpu_util = round(cpu_util, 1)

        return cpu_util

    # get current RAM used
    @staticmethod
    def getRamData():

        ram_use = (psutil.virtual_memory()[3]) / 1073741824
        ram_use = round(ram_use, 2)

        return ram_use

    @staticmethod
    def amd_linux_data():

        nvme_temp = psutil.sensors_temperatures()['nvme'][0].current
        cpu_temp = psutil.sensors_temperatures()['k10temp'][0].current
        amdgpu_temp = psutil.sensors_temperatures()['amdgpu'][0].current

        return nvme_temp, cpu_temp, amdgpu_temp

    @staticmethod
    def influx_client(token: str, org: str, url: str) -> object:

        # create client
        write_client = influxdb_client.InfluxDBClient(url=url,
                                                      token=token, org=org)
        write_api = write_client.write_api(write_options=SYNCHRONOUS)

        return write_api
