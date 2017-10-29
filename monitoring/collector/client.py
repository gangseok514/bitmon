import os
from influxdb import InfluxDBClient

class Client:
  __instance = None

  @classmethod
  def __getInstance(cls):
    return cls.__instance

  @classmethod
  def instance(cls, *args, **kargs):
    influxdb_url = os.getenv('INFLUXDB_URL', 'influxdb')
    cls.__instance = InfluxDBClient(influxdb_url, 8086, 'root', 'root', 'bitmon')
    cls.instance = cls.__getInstance
    return cls.__instance