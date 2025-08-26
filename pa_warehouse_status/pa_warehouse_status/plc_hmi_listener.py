import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json

class plc_hmi_listener(Node):
    def __init__(self, node_name='plc_hmi_listener'):
        super().__init__(node_name)
        self.sub = self.create_subscription(
            String,
            '/hmi/unified_status',
            self.cb,
            10
        )

    def cb(self, msg: String):
        try:
            data = json.loads(msg.data)   # parse JSON string into Python dict
            stamp = data["stamp"]
            box   = data["box"]
            counts = data["counts"]

            print("📥 Received unified HMI status:")
            print(f"  ⏱ Time: {stamp['sec']}.{stamp['nanosec']}")
            print(f"  📦 Box weight raw={box['weight_raw']}")
            print(f"  📍 Location: {box['location']}")
            print(f"  🔢 Counts: big={counts['big']}, medium={counts['medium']}, "
                  f"small={counts['small']}, total={counts['total']}")
            print()  # 👈 empty line at the end
        except Exception as e:
            self.get_logger().error(f"Failed to parse JSON: {e}\nRaw msg={msg.data}")

def main():
    rclpy.init()
    node = plc_hmi_listener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
