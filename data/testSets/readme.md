# Test Set Usage

## Basic Info  
Each test set video come from [some crossfit website][1]. 비디오는 운동하는 사람을 찍는 방향에따라 여러 부분으로 나눌 수 있다. 각 부분은 보통 2~3회의 반복 동작을 하고 우리는 이것을 *testSet/해당운동/해당관점/user set* 으로 사용한다. 또한, 각 부분에서 반복동작들을 하나의 *testSet/해당운동/해당관점/trainer set* 으로 생각한다. 따라서 *testSet/해당운동* 은 모두 하나의 비디오 자료를 바탕으로 만들어졌고 같은 촬영환경에서 촬영 되었다. Openpose를 사용해서 분석한 결과물들은 다음과 같다.  
      1. json file (각 프레임 속 운동하는 사람에대한 위치좌표)  
      2. image file (각 프레임을 분석해서 저장된 이미지 파일)  
      3. video file (제한 : avi or mp4가 공식적으로 지원되나, mp4는 제한적으로 작동되고 testset으로 사용한 비디오 파일에서는 작동되지 않았다)  
      4. numpy file (json file을 바탕으로 만든 파일이다. 다만, 동영상에서 사람이 사라질 경우, 프레임수와 동일하게 배열이 생성이 되지만 값은 (0,0,0)이 대입된다.)  


각각의 분석물들을 만들때 사용한 방법은 다음과 같다. 첫째, 각 *user set* 과 *trainer set* 의 시작점, 끝점 그리고 재생시간은 임의로 정했다. 다음번에는 프로그램을 만들어 자를 게획이다. 둘째, *resizing* 과 *diff* 방식. diff 방식에 있어서 사용방식은 다음과 같다. 전체적인 방식은 *user set* 하나를 여러 *trainer set* 과 비교하는 방식이다. 위에서 설명했듯이, 모두 같은 사람이기에 *resizing* 을 해줄 필요는 없다. 다만, 촬영앵글에 따라서 완전히 다른 경우라는 것을 주의해야하고 동영상이 하나가 아니라 여러개가 될 경우에 *resizing* 을 하거나 angle만을 이용해서 *diff* 해야 한다.

## File Structure

**1. squat**  
  * 1-1 : squat input # 1 (front)
    * 1-1-1 : squate front trainer # 1
    * 1-1-2 : squate front trainer # 2
  * 1-2 : squat input # 2 (side)
    * 1-2-1 : squate side trainer # 1
    * 1-2-2 : squate side trainer # 2
    * 1-2-3 : squate side trainer # 3
  * 1-3 : squat input # 3 (front)
    * 1-3-1 : squate front trainer # 3
    * 1-3-2 : squate front trainer # 4
    * 1-3-3 : squate front trainer # 5
즉, 스쿼트는 front에서 트레이너가 5명, 인풋 동영상이 2개 그리고, side에서는 3명, 1개가 된다.



[1]: https://www.crossfit.com/exercisedemos/
