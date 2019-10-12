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
  [![Build Status](https://travis-ci.org/I-Love-IU/pose-difference.svg?branch=dev)](https://travis-ci.org/I-Love-IU/pose-difference)
</p>

Chunghakdong Gyojungdang(chungyo) is a posture correction program for modern people.

- **Don't hesitate.** Exercise at anytime, anywhere you want.
- **Put your wallet in** Get personal training even if you don't have any money.
- **Get a wonderful feedback** Receive various information such as posture, amount of exercise, calories, etc.

  [**Go to our homepage**](https://www.naver.com)

--이곳에 짧막한 시연동영상 또는 결과물--

## What's In This Document

- [What's In This Document](#whats-in-this-document)
- [Get Up Install](#get-up-install)
- [🚀 Let's Get Quick Start](#%f0%9f%9a%80-lets-get-quick-start)
- [👀 Look at output](#%f0%9f%91%80-look-at-output)
- [시연사진 및 동영상](#%ec%8b%9c%ec%97%b0%ec%82%ac%ec%a7%84-%eb%b0%8f-%eb%8f%99%ec%98%81%ec%83%81)
- [📋 How To Use More Detailed](#%f0%9f%93%8b-how-to-use-more-detailed)
- [📝 License](#%f0%9f%93%9d-license)
- [🧷 References(gitHub Repo)](#%f0%9f%a7%b7-referencesgithub-repo)

## Get Up Install

---

Before use Chungyo, you are recommended to set up some frameworks and check the test environment.

**Test environment**

- windows 10
- python 3.7.4
- opencv-python 4.1.0
- numpy >= 1.14.5

**Dependencies**

- openpose(only for extracting example from video Images)

1. **Install from gitHub**
   You can simply download it from gitHub.

   ```
   git clone https://github.com/I-Love-IU/pose-difference.git
   ```

2. **Install several package**
   ```
   pip install requirements.txt
   ```

## 🚀 Let's Get Quick Start

You can get a example result in 5 minutes with these follow steps:

1. **Register user info.**

   This command will create userNameFolder/ at data/user/ or data/trainer/ directory (depends on user type)

   ```
   python main.py --user u --sys 1
   ```

2. **Register user skeleton.**

   This command will store user's basic skeleton from either video or picture, which will be used for resizing one's exercise motion. To choose input type between video and picture, use '--type [fileName]' command, which makes openpose to parse your input picture, not video file. The draw back issues are related to file name. Input file name is fixed now, not decided on user's choice. So this issues should be fixed quickly.

   ```
   python main.py --user u --sys 2 # for video whose name is 'initial_video' at '/data/type/userName/'
   ```

   ```
   python main.py --user u --sys 2 --type [anything] # for any picture stored at '/data/type/userName/'
   ```

3. **Train user skeleton.**

   This command will makes applied exercise skeleton based on user skeleton and trainer's exercise skeleton. The draw back issues are two things: size and direction problem and test unit problem. Size and direction problem is that each output's size and direction are different so that user skeleton is captured in different environment. We should regularize out's size and direction. Next, test unit problem simply means that there are no test tools to test performance of resizing function.

   ```
   python main.py --user u --sys 3 # apply exercise vector to user skeleton
   ```

4. **Analyze trainer skeleton.**

   Analyzing skeleton require two things: target person's basic skeleton and target exercise's skeleton performed by the same person. So if you want to analyze an exercise, you should enter above info.

   ```
   python main.py --user t --sys 4 # only for trainer
   ```
For more information on how to use it, please visit our guestbook's [start page](https://app.gitbook.com/@rhcsky/s/chungyo/).

## 👀 Look at output

If you follow 'Quick Start' step, the following results can be found.

## 시연사진 및 동영상

## 📋 How To Use More Detailed

---

## 📝 License

Chunghakdong Gyojungdang is freely available for free non-commercial use, and may be redistributed under these conditions. Please, see the [license](LICENSE) for further details.

---

## 🧷 References(gitHub Repo)

1. [tf-pose-estimation](https://github.com/ildoonet/tf-pose-estimation)
2. [open-pose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
3. [pose-trainer](https://github.com/stevenzchen/pose-trainer)

---
