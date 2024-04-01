import sys
import json
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

import asyncio
from autobahn.asyncio.websocket import (WebSocketClientProtocol,
                                        WebSocketClientFactory)

class web_indep(Node):
    def __init__(self):
        super().__init__("scanner")
        self.subscription = self.create_subscription(LaserScan,"/scan",self.cb,10)
        self.path = self.declare_parameter('host', "172.18.139.75/")
        self.band = self.declare_parameter('port', 9092)
        host = self.get_parameter("host").get_parameter_value().string_value
        port = self.get_parameter("port").get_parameter_value().integer_value
        if len(sys.argv) > 1:
            host = sys.argv[1]
        url = 'ws://{0}:{1}'.format(host, port)
        self.factory = WebSocketClientFactory(url)
        self.factory.protocol = TestClientProtocol
        loop = asyncio.get_event_loop()
        coro = loop.create_connection(self.factory, host, port)
    def cb(self,data):
        self.factory.protocol._sendDictSub(data.data)
        

class TestClientProtocol(WebSocketClientProtocol):
    def onOpen(self):
        self._sendDict({
            'op': 'advertise',
            'topic': '/scan',
            'type': 'sensor_msgs/LaserScan',
        })
        time.sleep(0.5)

    def _sendDict(self, msg_dict):
        msg = json.dumps(msg_dict).encode('utf-8')
        self.sendMessage(msg)

    def _sendDictSub(self,data):
        msg_dict = {
                'op': 'publish',
                'topic': '/scan',
                'msg': { 'data': data }
            }
        msg = json.dumps(msg_dict).encode('utf-8')
        self.sendMessage(msg)

    def onMessage(self, payload, binary):
        self.__class__.received.append(payload)

if __name__ == '__main__':
    rclpy.init()
    webIndep = web_indep()
    rclpy.spin(webIndep)
