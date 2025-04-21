import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import QoSProfile
from rclpy.qos import QoSDurabilityPolicy, QoSReliabilityPolicy
from rosidl_runtime_py.utilities import get_message as get_message_class

class FieldSubscriber(Node):
    def __init__(self):
        super().__init__('field_subscriber')

        # Declare parameters for topic name, field, and message type
        self.declare_parameter('topic_name', '/example_topic')
        self.declare_parameter('field_name', 'data')
        self.declare_parameter('message_type', 'std_msgs/msg/String') # Add default

        # Get parameter values
        self.topic_name = self.get_parameter('topic_name').get_parameter_value().string_value
        self.field_name = self.get_parameter('field_name').get_parameter_value().string_value
        self.message_type_str = self.get_parameter('message_type').get_parameter_value().string_value

        # Create a subscription
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.VOLATILE,
            depth=10
        )

        # Dynamically determine the message type from the parameter
        try:
            # Use get_message_class (renamed from get_message for clarity)
            msg_type = get_message_class(self.message_type_str)
            self.subscription = self.create_subscription(
                msg_type,
                self.topic_name,
                self.listener_callback,
                qos_profile
            )
            self.get_logger().info(
                f"Subscribed to topic: {self.topic_name} "
                f"with type: {self.message_type_str}"
            )
        except (ValueError, AttributeError, ModuleNotFoundError, Exception) as e:
            self.get_logger().error(
                f"Failed to import message type '{self.message_type_str}' "
                f"or create subscription for topic '{self.topic_name}': {e}"
            )
            self.subscription = None

    def listener_callback(self, msg):
        # Extract the specified field from the message
        try:
            field_value = getattr(msg, self.field_name)
            self.get_logger().info(f"Field '{self.field_name}' value: {field_value}")
        except AttributeError:
            self.get_logger().error(
                f"Field '{self.field_name}' does not exist in message type "
                f"'{self.message_type_str}' on topic '{self.topic_name}'."
            )

def main(args=None):
    rclpy.init(args=args)
    node = FieldSubscriber()

    try:
        # Check if subscription was created successfully before spinning
        if node.subscription is None:
            node.get_logger().error("Subscription could not be created. Shutting down.")
        else:
            rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
