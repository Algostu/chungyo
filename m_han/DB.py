import os

class DB():
    def __init__(self):
        pass
    def create_user(self, folder_name):
        print('Creating User folder...', end='')
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            return True
        else:
            return False

    def read_dir_list(self, folder_name):
        return os.listdir(folder_name)

    def read_exercise_list(self, loc):
        if loc != None:
            fileloc = loc
        else:
            fileloc = os.path.join('data', 'exercise.txt')
        with open(fileloc, 'r') as f:
            return [line.rstrip('\n') for line in f]


if __name__ == '__main__':
    loc = os.path.join('..','data','exercise.txt')
    db = DB()
    db.read_exercise_list(loc)
