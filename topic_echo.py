import os
import threading
import time
import argparse, sys
from distutils.util import strtobool

topics = ['/crowd/0/joint_states','/crowd/1/joint_states','/crowd/2/joint_states','/crowd/3/joint_states','/crowd/4/joint_states']

def echo_topic(topic_id):
    os.system("rostopic echo {0}".format(topic_id))


def main():

    parser=argparse.ArgumentParser()
    parser.add_argument("--robots", type=int,help="number of robots", default=1)
    
    args=parser.parse_args()
    
    for x in range(args.robots):
        topic_listener = threading.Thread(target=echo_topic, args=[topics[x]])
        topic_listener.start()


if __name__ == "__main__":
    main()
