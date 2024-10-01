import os
import argparse, sys
import numpy as np
from distutils.util import strtobool


def main():

    parser=argparse.ArgumentParser()
    parser.add_argument("--namespace", help="robot namespace", default="0")
    
    args=parser.parse_args()
    ns=args.namespace
    

    while True:
       z = np.random.uniform(-0.8, 0.8, 1)
       phi = np.random.uniform(-np.pi, np.pi, 1)
       rxy = np.sqrt(1 - z**2)
       x = rxy * np.cos(phi)
       y = rxy * np.sin(phi)
       print("python3 moveit2_planner.py --ros-args -r __ns:={3} -p position:=\"[{0}, {1}, {2}]\" -p cartesian:=True".format(x[0],y[0],z[0],ns))
       os.system("python3 moveit2_planner.py --ros-args -r __ns:={3} -p position:=\"[{0}, {1}, {2}]\" -p cartesian:=True -p quat_xyzw:=\"[-0.003336178036526443, -0.707098688830761, -0.7070978857887898, 0.0035908331833641657]\"".format(x[0],y[0],z[0],ns))
         

if __name__ == '__main__':
  main()