'''
* Writer : hankyul
* Last updated : 2019-08-21
* About what : parse options and delegate user operation to right modules
* contens : function -> main
'''
import argparse
from pose_diff.interface.PoseDifference import PoseDifference
from pose_diff.core.run import *


def main():
    parser = argparse.ArgumentParser(description='Pose Difference')
    parser.add_argument('--user', type=str, default='', help='Select User Type')
    parser.add_argument('--sys', type=int, default=0, help='Select System Operations')
    parser.add_argument('--type', type=str, default=None, help='Select Input Type')

    args = parser.parse_args()

    app = PoseDifference()
    ret_val = app.choose_sys_and_option(args.user, args.sys, args.type)
    return ret_val



if __name__=="__main__":
    main()
