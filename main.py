'''
* Writer : hankyul
* Last updated : 2019-08-21
* About what : parse options and delegate user operation to right modules
* contens : function -> main
'''
import argparse

from m_han.PoseDifference import PoseDifference
from m_seung import run

def main():
    # parser = argparse.ArgumentParser(description='Pose Difference')
    # parser.add_argument('--user', type=str, default='', help='Select User Type')
    # parser.add_argument('--sys', type=int, default=0, help='Select System Operations')
    # parser.add_argument('--type', type=str, default=None, help='Select Input Type')
    #
    # args = parser.parse_args()
    #
    # app = PoseDifference()
    # app.choose_sys_and_option(args.user, args.sys, args.type)
<<<<<<< HEAD

    trainer = "data/trainer/IU/walk/skeleton.npy"
    user = "data/user/IU/walk/trained_skeleton.npy"
    
    run.Video(trainer,user,'pullup')



=======
    user = 'data/user/IU/walk/trained_skeleton.npy'
    trainer = 'data/trainer/IU/walk/skeleton.npy'
    exercise = 'pullup'
    way = 'round' #round_up, round_down.
    average = 1 # 1은 apply 2는 non
    diffing = 'increase' # decrease
    run.Video(trainer,user,exercise,diffing,way,average)
>>>>>>> c01d02a617729775c27a444d7e3312f45b9ab768

if __name__=="__main__":
    main()
