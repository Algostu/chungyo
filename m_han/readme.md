# m_han
---
## Basic Usage  

**Basic Option Explanation  
--user [user name]
--sys [1~6]
--type [anything] : optional. use only if you use sys 2 and want to parse video.

1. Register User Info  
This command will create userNameFolder/ at data/user/ or data/trainer/ directory (depend on user type)
````
python main.py --user u --sys 1
````
***Output***   
````
Enter User Name(will create folder with this name):testUser
Creating User folder...Done
````

2. Register User skeleton
This command will store user's basic skeleton from either video or picture, which will be used for resizing one's exercise motion. To choose input type between *video and picture*, use **'--type [fileName]'** command, which makes openpose to parse your input picture, not video file. The *draw back* issues are related to file name. Input file name is fixed now, not decided on user's choice. So this issues should be fixed quickly.  
````
python main.py --user u --sys 2 # for video whose name is 'initial_video' at '/data/type/userName/'
````

````
python main.py --user u --sys 2 --type [anything] # for any picture stored at '/data/type/userName/'
````

***Output***  
````
Enter User Name(wiil be stored into this user's folder):testUser
Check target folder...Done
Processing parse_picture...
Starting OpenPose demo...
Auto-detecting all available GPUs... Detected 1 GPU(s), using 1 of them starting at GPU 0.
Starting thread(s)...
OpenPose demo successfully finished. Total time: 9.418791 seconds.
Done
Successfully stored initial_skeleton.npy into /data/user/testUser/base folder
````

3. Train User skeleton
This command will makes applied exercise skeleton based on user skeleton and trainer's exercise skeleton. The *draw back* issues are two things: size and direction problem and test unit problem. Size and direction problem is that each output's size and direction are different so that user skeleton is captured in different environment. We should regularize out's size and direction. Next, test unit problem simply means that there are no test tools to test performance of resizing function.  
````
python main.py --user u --sys 3 # apply exercise vector to user skeleton
````  
***Output***  
````
Enter User Name(where output files are stored into):testUser # means '/data/user/testUser/base/initial_skeleton.npy'
--------------Exercise List-----------
1. shoulder_press
2. pull_up
3. dead_lift
4. walk
--------------------------------------
Enter which exercise you want to train your skeleton:4
--------------Trainer List-----------
1. good
2. han
3. IU
4. jhon
5. testSuccess
6. TestUser
--------------------------------------
Enter which trainer you want to train your skeleton from:3
Check target folder exist... Done
Check if user skeletons are analized... Done
Check sample vector exist... Done
Done
Successfully stored trainded_skeleton.npy into /data/u/testUser/walk folder
````

4. Analyze trainer skeleton  
Analyzing skeleton require two things: target person's basic skeleton and target exercise's skeleton performed by the same person. So if you want to analyze an exercise, you should enter above info.  
````
python main.py --user t --sys 4 # only for user
````  
***Output***
````
Enter Trainer Name(where output file will be stored into):IU
--------------Exercise List-----------
1. shoulder_press
2. pull_up
3. dead_lift
4. walk
--------------------------------------
Enter which exercise you want to anaysis:4
Check target folder exist... Done
Check if trainer skeletons are analized... Done
Target exercise are analized before..? Yes!
Processing analyze_exercise...
This frames accuracy is 0.931361
Done
Successfully stored vector.npy into /data/t/IU/walk folder
````
