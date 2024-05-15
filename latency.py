import rosbag
from datetime import datetime


# Convert nanoseconds to seconds
timestamp_seconds = 298088000000.00 / 1e9

# Convert seconds to a datetime object
timestamp_datetime = datetime.fromtimestamp(timestamp_seconds)

print("Timestamp (seconds):", timestamp_seconds)
print("Datetime:", timestamp_datetime)

exit()

# Open ROSbags
publisher_bag = rosbag.Bag('./folder/master 15.bag')
subscriber_bag = rosbag.Bag('./folder/slave 15.bag')

# Define the topic you're interested in
topic = '/crowd/0/joint_states'

MAX_TIME_DIFFERENCE = 0.05

# Initialize latency list
latencies = []

# Iterate through messages in the publisher's ROSbag
for _, _, t_publisher in publisher_bag.read_messages(topics=[topic]):
    # Find the nearest received message in the subscriber's ROSbag
    closest_time_diff = float('inf')

    for _, _, t_subscriber in subscriber_bag.read_messages(topics=[topic]):
        time_diff = abs((t_publisher - t_subscriber).to_sec())

        if time_diff < closest_time_diff:
            closest_time_diff = time_diff

    # Add the closest time difference to the latencies list
    latencies.append(closest_time_diff)
    print(closest_time_diff)

# Close ROSbags
publisher_bag.close()
subscriber_bag.close()

# Calculate average latency
if latencies:
    avg_latency = sum(latencies) / len(latencies)
    print(f"Average latency on topic {topic}: {avg_latency} seconds")
else:
    print("No matching messages found on the specified topic.")
