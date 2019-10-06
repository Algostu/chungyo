from pose_diff.interface import PoseDifference
import os

base_root_project_location = 'pose-difference'
def main():
    change_cwd()
    PoseDifference.main_ui()
def change_cwd():
    path = os.path.abspath(__file__)
    dirname = os.path.dirname(path)
    while os.path.split(dirname)[1] != base_root_project_location:
        dirname = os.path.dirname(dirname)
    os.chdir(dirname)
if __name__=="__main__":
    main()
