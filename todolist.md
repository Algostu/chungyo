# ToDo List
1. 각 UC별로 필요한 그래프 추출 (moreinfo에서 `graph.npy` 파일 불러오기 위해서 넣은 `load_skeleton`제거)
  + MoreInfo 각 UC 마다 그래프 이름 변경
2. 각 UC별로 Analyze할때 들어갈 이벤트
3. CURRENT_TIMESTAMP를 localtime으로 변경

4. core function 수정 - 최종 발표용
5. 기능 테스트 준비

# 승민's TodoList


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
9. UC2, 3-Scene 3 표본으로 트레이너의 스켈레톤을 훈련시키는 영상과 원본 영상을 비교한다.
  + 리사이즈된 영상 저장될때 거꾸로 저장되는것 해결 + 디버그용으로 만든 imshow제거...Done
  + UC3-Scene 3 UI 적용 (`original_label` : Trainer의 운동, `copy_label` : Resized된 Trainer)
10. UC2, 3-Scene 1 파일 정보 출력하는곳의 UI 수정
11. UC4-Scene 2 디버그용으로 imshow하는 부분 제거
12. MoreInfo UI 적용
  + 각 Tab마다 보여줘야 할 Graph
  + Load Data하는 부분 변경
13. UC 5 UI 적용

# Requirement
1. numpy==1.16.1 (pick problem)
2. python-docx
