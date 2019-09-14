class UserInfo():
    def __init__(self, user_type):
        self.user_type = user_type
        self.preferred_trainer = 0
        self.preferred_exercise_type = 0
        self.rate = 0
        self.reps_per_set = 0
        self.user_id = ""

    def set_preferred_exercise_type(self, str):
        print("--------------Exercise List-----------")
        for s in str[0]:
            print(s)
        print("--------------------------------------")
        print(str[1], end="")
        self.preferred_exercise_type = int(input())-1

    def set_user_id(self, str):
        print(str, end="")
        self.user_id = input()

    def set_preferred_trainer(self, str):
        print("--------------Trainer List-----------")
        for i, s in enumerate(str[0]):
            print("%d. %s" % (i+1, s))
        print("--------------------------------------")
        print(str[1], end="")
        self.preferred_trainer = int(input())-1
