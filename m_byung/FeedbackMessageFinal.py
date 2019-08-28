class FeedBackMassage:

    def feedback_massage_tool(self, choice_number):
        self.feedback_down = self.feedback_up = self.feedback_little_down = self.feedback_little_up = 'None'  # 없는경우
        if choice_number == 1:
            self.feedback_up = '팔꿈치를 올리세요'                  # up 기준값 - 실제값 >0 , down 기준값 - 실제값 <0
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

    def give_feedback_about_difference(self, part, different_angle_lists):

        parts = ['코', '목', '오른쪽 어께', '오른쪽 팔꿈치', '오른쪽 손목', '왼쪽 어께', '왼쪽 팔꿈치', '왼쪽 손목', '오른쪽 엉덩이',
                 '오른쪽 무릎', '오른쪽 발목', '왼쪽 엉덩이', '왼쪽 무릎', '왼쪽 발목', '오른쪽 눈', '왼쪽 눈', '오른쪽 귀', '왼쪽 귀']

        probelm_parts = parts[part]

        list=[]
        for different_angle_list in different_angle_lists:

            if type(different_angle_list)== type([1]):
                pass
            else:
                different_angle_list=[different_angle_list]


            if probelm_parts == '오른쪽 어께' or probelm_parts == '왼쪽 어께':
                self.feedback_massage_tool(1)
            elif probelm_parts == '오른쪽 팔꿈치' or probelm_parts == '왼쪽 팔꿈치':
                self.feedback_massage_tool(2)
            elif probelm_parts == '목':
                self.feedback_massage_tool(3)
            else:
                self.feedback_massage_tool('None')      #해결방안이 없는경우


            for i in different_angle_list:
                abs_angle = abs(i)
                if i < -15:
                    print(f'문제부분 : {probelm_parts}')
                    print(f'해결방안 : {self.feedback_down}({abs_angle}도 정도 오류)')
                elif i < 0 and i >= -15:
                    print(f'문제부분 : {probelm_parts}')
                    print(f'해결방안 : {self.feedback_little_up}')
                elif i == 0:
                    print('잘하고 있어요')
                elif i > 0 and i <= 15:
                    print(f'문제부분 : {probelm_parts}')
                    print(f'해결방안 : {self.feedback_little_down}')
                elif i > 15:
                    print(f'문제부분: {probelm_parts}')
                    print(f'해결방안 : {self.feedback_down}({abs_angle}도 정도 오류)')

    # 어께 2 5 팔꿈치 3 6 목 1
if __name__ == "__main__":
    test_class = FeedBackMassage()
    list = [[-8,-19],[5,19],[-1,-16,0,1,16],0]  # test list
    result = test_class.give_feedback_about_difference(15, list) # input값을 제한해서 받는 방법(?)
