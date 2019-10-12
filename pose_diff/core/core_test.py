import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from pose_diff.core.run import Video,Real_time

if __name__ == '__main__':
    trainer_dir = 'C:/Users/Rhcsky/Desktop/SW_developer/pose-difference/data/output/1-1/numpy/result.npy'
    user_dir = 'C:/Users/Rhcsky/Desktop/SW_developer/pose-difference/data/output/1-2/numpy/result.npy'

    Video(trainer_dir,user_dir)
    # Real_time(user_dir)