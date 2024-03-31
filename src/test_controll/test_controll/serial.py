import rclpy
from rclpy.node import Node
from std_msgs.msg import Char
import serial

class serial_indep(Node):
    def __init__(self):
        super().__init__("serial_indep")
        self.path = self.declare_parameter('path', '/dev/ttyACM0')
        self.band = self.declare_parameter('band', 115200)
        self.writer = serial.Serial(self.get_parameter('path').get_parameter_value().string_value,self.get_parameter('band').get_parameter_value().integer_value,timeout=0.1)
        self.subscription = self.create_subscription(Char,"Serial_data",self.cb,10)
        #self.get_logger().info("send: %s" % self.get_parameter('path').get_parameter_value().string_value)
    def cb(self,data):
        a = data.data
        self.writer.write(a.encode())
        self.get_logger().info("send: %c" % a)

def main():
    rclpy.init()
    serialIndep = serial_indep()
    rclpy.spin(serialIndep)