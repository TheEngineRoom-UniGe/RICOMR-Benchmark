import rosbag

# Open ROSbag file
bag = rosbag.Bag('./folder/master 15.bag')

# Define the topic you're interested in
topic = '/crowd/0/joint_states'

# Set the time interval for frequency calculation (in seconds)
time_interval = 1.0  # You can adjust this as needed

# Initialize variables for frequency calculation
msg_count = 0
start_time = None


# Loop through messages in the ROSbag
for _, _, t in bag.read_messages(topics=[topic]):
    if start_time is None:
        start_time = t.to_sec()  # Convert Time object to seconds
    if t.to_sec() - start_time > time_interval:
        frequency = msg_count / (t.to_sec() - start_time)
        print(f"Frequency on topic {topic}: {frequency} Hz")
        # Reset variables for the next interval
        start_time = t.to_sec()
        msg_count = 0
    msg_count += 1

# Close ROSbag file
bag.close()