from confluent_kafka.admin import (AdminClient, NewTopic, 
                                   ConfigResource)
import config



class KafkaAdmin:
    def __init__(self, bootstrap_serv, api_key, api_secret):
        self.kafka_admins = AdminClient({
          'bootstrap.servers': bootstrap_serv,
          'sasl.mechanism': 'PLAIN',
          'security.protocol': 'SASL_PLAINTEXT',
          #'security.protocol': 'SASL_SSL',
          'sasl.username': api_key,
          'sasl.password': api_secret
      })
        
    def create_topic(self, topic_name):
        new_topic = NewTopic(topic_name, num_partitions=3, replication_factor=3) 
        result_dict = self.kafka_admins.create_topics([new_topic])

        for topic, future in result_dict.items():
            try:
                future.result()  # The result itself is None
                print("Topic {} created".format(topic))
            except Exception as e:
                print("Failed to create topic {}: {}".format(topic, e))

    def topic_exists(self,topic):
        metadata = self.kafka_admins.list_topics()
        for t in iter(metadata.topics.values()):
            if t.topic == topic:
                return True
        return False
