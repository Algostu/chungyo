# ToDo List
1. UC2, 3-Scene 3 표본으로 트레이너의 스켈레톤을 훈련시키는 영상과 원본 영상을 비교한다.
  + 리사이즈된 영상 저장될때 거꾸로 저장되는것 해결 + 디버그용으로 만든 imshow제거
  + math_info를 찾는 과정에서 필요한 그래프 추출
3. UC2, 3-Scene 1 파일 정보 출력하는곳의 UI 수정
4. UC3-Scene 3 UI 적용
5. UC4-Scene 2 디버그용으로 imshow하는 부분 제거
6. MoreInfo UI 적용
  + 각 Tab마다 보여줘야 할 Graph
  + Load Data하는 부분 변경
7. CURRENT_TIMESTAMP를 localtime으로 변경

# 승민's TodoList
***꼭 메인.py의 복사본을 만들어서 사용할것***
1. diff 할때 graph로 출력할 용도의 numpy를 만들기
2. 그외 잡다한 것

# Done List
1. UC2-Scene 2 영상을 출력할때 skeleton을 찾을 경우 copy 영상이 멈춘다.
2. UC2-Scene 2 영상을 출력할때 skeleton을 못 찾을 경우 경고창을 띄워주고 종료
3. UC2-Scene 2 skeleton_list를 저장할때 Frame_num과 skeleton을 같이 저장하기.
4. UC2-Scene 2 스켈레톤을 찾을 경우 skeleton 이미지를 띄워주기
  + 이미지로 변환하는 방법을 알면 할 수 있다. (승민)
5. UC2-Scene 3 close 버튼, listWidget 옆으로 보기
6. UC2-Scene 2,3 그래프 사이에 구분선 넣기 - 취소
7. 동영상 저장될때 gif 라벨을 통해서 출력 - 취소
8. UC4-Scene 2 DB에 동영상 저장


# Requirement
1. numpy==1.16.1 (pick problem)
