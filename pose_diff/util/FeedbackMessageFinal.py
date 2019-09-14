class FeedbackMessage:
    shoulder=[0,0,1,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0]
    elbow=[0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,0,0,0]
    neck=[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    def feedback_massage_tool(self, choice_number):
        self.feedback_down = self.feedback_up = self.feedback_little_down = self.feedback_little_up = 'None'  # 없는경우
        if choice_number == 1:
            self.feedback_up = '팔꿈치를 올리세요'                   # up 기준값 - 실제값 >0 , down 기준값 - 실제값 <0
            self.feedback_little_up = '팔꿈치을 조금만 올리세요'
            self.feedback_down = '팔꿈치를 내리세요'
            self.feedback_little_down = '팔꿈치을 조금만 내리세요'
        elif choice_number == 2:
            self.feedback_up = '팔을 펴세요'
            self.feedback_little_up = '팔을 조금만 펴세요'
            self.feedback_down = '팔을 접으세요'
            self.feedback_little_down = '팔을 조금만 접으세요'
        elif choice_number == 3:
            self.feedback_up = '어께를 올리세요'
            self.feedback_little_up = '어께를 조금만 올리세요'
            self.feedback_down = '어께를 내리세요'

            self.feedback_little_down = '어께를 조금만 내리세요'

    def feedback_message(self):
        if self.angle < -15:
            print(f'문제부분 : {self.probelm_parts}')
            print(f'해결방안 : {self.feedback_down}({self.abs_angle}도 정도 오류)')
        elif self.angle < 0 and self.angle >= -15:
            print(f'문제부분 : {self.probelm_parts}')
            print(f'해결방안 : {self.feedback_little_up}')
        elif self.angle == 0:
            print('잘하고 있어요')
        elif self.angle > 0 and self.angle <= 15:
            print(f'문제부분 : {self.probelm_parts}')
            print(f'해결방안 : {self.feedback_little_down}')
        elif self.angle > 15:
            print(f'문제부분: {self.probelm_parts}')
            print(f'해결방안 : {self.feedback_down}({self.abs_angle}도 정도 오류)')


    def give_feedback_about_difference(self,exercise,different_angle_lists):
        if exercise=='pull up':
            for different_angle_list in different_angle_lists:
                for i in range(len(self.shoulder)):
                    self.angle=different_angle_list[i]
                    self.abs_angle=abs(different_angle_list[i])
                    if self.shoulder[i]==1:
                        self.probelm_parts='right shoulder'
                        self.feedback_massage_tool(1)
                        self.feedback_message()
                    elif self.shoulder[i]==2:
                        self.probelm_parts = 'left shoulder'
                        self.feedback_massage_tool(1)
                        self.feedback_message()
                    if self.elbow[i]==1:
                        self.probelm_parts = 'left elbow'
                        self.feedback_massage_tool(2)
                        self.feedback_message()
                    elif self.elbow[i]==2:
                        self.probelm_parts = 'right elbow'
                        self.feedback_massage_tool(2)
                        self.feedback_message()
                    if self.neck[i]==1:
                        self.probelm_parts = 'neck'
                        self.feedback_massage_tool(3)
                        self.feedback_message()
        else:
            print('do pull up')




if __name__ == "__main__":
    test_class = FeedbackMessage()
    list = [[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18],[-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18]]
    result = test_class.give_feedback_about_difference('pull up',list)
