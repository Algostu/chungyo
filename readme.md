# pose-difference

<h1 align="center">
  Chunghakdong Gyojungdang
</h1>

<h3 align="center">
  ⌚ 💪 📊
</h3>
<h3 align="center">
  Check your posture anytime, anywhere.
</h3>
<p align="center">
  Chunghakdong Gyojungdang is a free and open source project based on Openpose that can make your body more  balanced.
</p>
<p align="center">
  <a href='https://travis-ci.org/I-Love-IU/pose-difference'><img src = "https://travis-ci.org/I-Love-IU/pose-difference.svg?branch=dev"></a>
</p>

Chunghakdong Gyojungdang(chungyo) is a posture correction program for modern people.

- **Don't hesitate.** Exercise at anytime, anywhere you want.
- **Put your wallet in** Get personal training even if you don't have any money.
- **Get a wonderful feedback** Receive various information such as posture, amount of exercise, calories, etc.

  [**Go to our homepage**](https://rhcsky.gitbook.io/chungyo/)

--이곳에 짧막한 시연동영상 또는 결과물--

## What's In This Document

- [pose-difference](#pose-difference)
  - [What's In This Document](#whats-in-this-document)
  - [🚀 Let's Get Quick Start](#%f0%9f%9a%80-lets-get-quick-start)
  - [👀 Look at output](#%f0%9f%91%80-look-at-output)
  - [📋 How To Use More Detailed](#%f0%9f%93%8b-how-to-use-more-detailed)
  - [📝 License](#%f0%9f%93%9d-license)
  - [🧷 References(gitHub Repo)](#%f0%9f%a7%b7-referencesgithub-repo)



**Test environment**

- windows 10
- python 3.7.4
- opencv-python 4.1.0
- numpy >= 1.14.5
- matplotlib
- pyqt
- 
**Dependencies**
+ openpose(only for extracting example from video Images)

**Install**

1. **Install from gitHub**
   You can simply download it from gitHub.

   ```
   git clone https://github.com/I-Love-IU/pose-difference.git
   ```

2. **Install several package**
   ```
   pip install requirements.txt
   ```
3. **Install OpenPose Demo version and other pre-requisite for OpenPose**
   
   You can check download list from [this link](2). 

## 🚀 Let's Get Quick Start
 From here, we introduce hello usage of our project, such as register your video file as trainer used for bases of certain exercises.
 You can get a example result in 5 minutes with these follow steps: (Register Trainer) If you are new to our project, use --sys 10 options, 
 which is made for getting result fast.

   ```
   python main.py --sys 10
   ```

   This command will store trainer's basic skeleton from either video or picture, which will be used for resizing one's exercise motion. We only support video file as input which we pass to openpose for getting info about your body parts. 

   ![Register](https://github.com/I-Love-IU/pose-difference/blob/master/docs/AC_%5B20191011-035747%5D.gif?raw=true)


## 👀 Look at output

You can see details of our output info from [here](https://naver.com)

## 📋 How To Use More Detailed

For more information on how to use it, please visit our guestbook's [start page](https://rhcsky.gitbook.io/chungyo/use/how-to-use).

---

## 📝 License

Chunghakdong Gyojungdang is freely available for free non-commercial use, and may be redistributed under these conditions. Please, see the [license](LICENSE) for further details.

---

## 🧷 References(gitHub Repo)

1. [tf-pose-estimation](https://github.com/ildoonet/tf-pose-estimation)
2. [open-pose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
3. [pose-trainer](https://github.com/stevenzchen/pose-trainer)
