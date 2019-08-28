'''
* Writer : hankyul
* Last updated : 2019-08-21
* About what : parse options and delegate user operation to right modules
* contens : function -> main
'''
import argparse

from m_han.PoseDifference import PoseDifference

def main():
    parser = argparse.ArgumentParser(description='Pose Difference')
    parser.add_argument('--user', type=str, default='', help='Select User Type')
    parser.add_argument('--sys', type=int, default=0, help='Select System Operations')

    args = parser.parse_args()

    app = PoseDifference()
    app.choose_sys_and_option(args.user, args.sys)

if __name__=="__main__":
    main()
