# pose-difference
---
## Build Status
[![Build Status](https://travis-ci.org/I-Love-IU/pose-difference.svg?branch=dev)](https://travis-ci.org/I-Love-IU/pose-difference)

## Installation
**Test environment**
* windows 10
* python 3.6.4
* opencv-python 4.1.0
* numpy >= 1.14.5

**Dependencies**
+ openpose(only for extracting example from video Images)

**Install from gitHub**  
You can simply download it from gitHub. Type this in your git command(or bash)
````
git clone https://github.com/I-Love-IU/pose-difference.git
cd pose-difference
python main.py
````

---
## Hello World  
This command will create userNameFolder/ at data/user/ or data/trainer/ directory (depend on user type)
````
python main.py --user u --sys 1
````
***Output***   
````
Enter User Name(will create folder with this name):testUser
Creating User folder...Done
````
For more information, please follow this [link][11]




## References(gitHub Repo)
1. [tf-pose-estimation][2]
2. [open-pose][3]
3. [pose-trainer][4]

[1]: https://i-love-iu.github.io/
[2]: https://github.com/ildoonet/tf-pose-estimation
[3]: https://github.com/CMU-Perceptual-Computing-Lab/openpose
[4]: https://github.com/stevenzchen/pose-trainer
[5]: https://trello.com/b/Jn1NikPt/sw-opensource-2019
[6]: /docs/issues.png
[7]: https://stackoverflow.com/
[8]: https://chris.beams.io/posts/git-commit/
[9]: https://github.com/torvalds/linux/commits/master
[10]: https://github.com/spring-projects/spring-boot/commits/master
