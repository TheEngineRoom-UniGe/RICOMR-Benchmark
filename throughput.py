import rosbag
import rospy.msg

# Open ROSbag file
bag = rosbag.Bag('./folder/master 15.bag')

# Define the topic you're interested in
topic = '/crowd/0/joint_states'

# Set the time interval for throughput calculation (in seconds)
time_interval = 1.0  # You can adjust this as needed

# Initialize variables for throughput calculation
total_data_size = 0
start_time = None

# Loop through messages in the ROSbag
for _, msg, t in bag.read_messages(topics=[topic]):
    if start_time is None:
        start_time = t.to_sec()  # Convert Time object to seconds
    total_data_size += msg.__sizeof__()
    if t.to_sec() - start_time > time_interval:
        duration = t.to_sec() - start_time
        throughput = total_data_size / duration
        print(f"Throughput on topic {topic}: {throughput} bytes/second")
        # Reset variables for the next interval
        start_time = t.to_sec()
        total_data_size = 0

# Close ROSbag file
bag.close()