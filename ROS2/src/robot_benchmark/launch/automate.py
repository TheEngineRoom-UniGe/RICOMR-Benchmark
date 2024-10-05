import os
import argparse, sys
import numpy as np
import random
from random import choice
from distutils.util import strtobool


def main():

    parser=argparse.ArgumentParser()
    parser.add_argument("--namespace", help="robot namespace", default="0")
    
    args=parser.parse_args()
    ns=args.namespace
    

    while True:
       z = 0.4
       x = random.uniform(0.3, 0.5)
       y = random.uniform(0.3, 0.5)
       print("python3 moveit2_planner.py --ros-args -r __ns:={3} -p position:=\"[{0}, {1}, {2}]\" -p cartesian:=True".format(x,y,z,ns))
       os.system("python3 moveit2_planner.py --ros-args -r __ns:={3} -p position:=\"[{0}, {1}, {2}]\" -p cartesian:=True".format(x,y,z,ns))
         

if __name__ == '__main__':
  main()
