import os
import argparse, sys
import numpy as np
from distutils.util import strtobool
import random


def main():

    parser=argparse.ArgumentParser()
    parser.add_argument("--namespace", help="robot namespace", default="0")
    
    args=parser.parse_args()
    ns=args.namespace
    positions = [[0.5, 0.5,0.5],
                [0.5, -0.5,0.5],
                [0.5, 0.4,0.2],
                [0.5, 0.0,0.2],
                [0.5, -0.4,0.2],
                [0.7, -0.4,0.2],
                [0.7, 0.4,0.2],
                [0.4, 0.7,0.2],
                [0.4, -0.7,0.2],
                [0.3, 0.3,0.4],
                [0.3, -0.3,0.4]]
    

    while True:
       randSeed = random.randint(0, 10)
       print(positions[randSeed])
       z = positions[randSeed][2]
       x = positions[randSeed][0]
       y = positions[randSeed][1]
       print("python3 moveit2_planner.py --ros-args -r __ns:={3} -p position:=\"[{0}, {1}, {2}]\" -p cartesian:=True".format(x,y,z,ns))
       os.system("python3 moveit2_planner.py --ros-args -r __ns:={3} -p position:=\"[{0}, {1}, {2}]\" -p cartesian:=True".format(x,y,z,ns))
         

if __name__ == '__main__':
  main()
