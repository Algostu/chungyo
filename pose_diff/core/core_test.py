from pose_diff.core import run

if __name__ == '__main__':
    user = 'C:/Users/Rhcsky/Desktop/SW_developer/pose-difference/data/user/IU/walk/trained_skeleton.npy'
    trainer = 'C:/Users/Rhcsky/Desktop/SW_developer/pose-difference/data/trainer/IU/walk/skeleton.npy'
    exercise = 1 # 'pullup'
    way = 'round'  # round_up, round_down.
    average = 1  # 1은 apply 2는 non
    diffing = 'increase'  # decrease
    run.Video(trainer, user, exercise, diffing, way, average)
