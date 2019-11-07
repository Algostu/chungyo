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
  <a href='https://travis-ci.org/I-Love-IU/chungyo'><img src = "https://travis-ci.org/I-Love-IU/chungyo.svg?branch=dev"></a>
</p>

Chunghakdong Gyojungdang(chungyo) is a posture correction program for modern people.

- **Don't hesitate.** Exercise at anytime, anywhere you want.
- **Put your wallet in** Get personal training even if you don't have any money.
- **Get a wonderful feedback** Receive various information such as posture, amount of exercise, calories, etc.

  [**Go to our wiki!**](https://github.com/I-Love-IU/chungyo/wiki)
  
<span style="display:block;text-align:center">![main](https://user-images.githubusercontent.com/53206234/68396912-af4d2b80-01b5-11ea-85e8-94b12a7d502f.gif)
</span>


## 📌 What's In This Document

  - [📌 What's In This Document](#-whats-in-this-document)
  - [🚀 Let's Get Quick Start](#-lets-get-quick-start)
  - [👀 Look at output](#-look-at-output)
  - [📋 How To Use More Detailed](#-how-to-use-more-detailed)
  - [📝 License](#license)
  - [🧷 References(gitHub Repo)](#-referencesgithub-repo)


**Test environment**

- windows 10
- python 3.7.4
- opencv-python 4.1.0
- numpy 1.16
- matplotlib
- pyqt5
- beautifulsoup4
- googledrivedownloader

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
 From here, we introduce you how to introduce our program.
 Chungyo designed GUI to provide easy use environment for users.
 You can get a example result in a few seconds with this code: 
   ```
   python main.py
   ```

   This command will start our first page that sign in. After the sign in, follow  the steps below.
   1. Upload Video files
   2. Make Personal Trainer
   3. Analyze Guide Line
   4. Comment from Expert

<span style="display:block;text-align:center">![overall](https://user-images.githubusercontent.com/53206234/68394980-2e406500-01b2-11ea-89a9-e0b47a5059ed.gif)</span>
   


## 👀 Look at output
We shall provide for a final report.
<span style="display:block;text-align:center">![report](https://user-images.githubusercontent.com/53206234/68396918-b07e5880-01b5-11ea-87f0-eaf7181b6b9c.gif)
</span>

## 📋 How To Use More Detailed
There are 7 menu for using our program. Let's learn more about each function in detail.

**1. Upload Video Files**
    - Upload your workout video and your EssentialForce video.
    
**2. Register Trainer**
    - This menu uploads an exercise video that will be used as a trainer. Only trainers can enter this menu.

**3. Make Personal Trainer**
    - Based on the physical information of the initialized user and trainer, create a personal trainer of the same size as the user.

**4. Analyze Physically**
    - The user and trainer are analyzed physically. But, this function is still under development.

**5. Analyze Guide Line**
    - The user's motion is analyzed by considering the difference in the trainer's coordinate value and angle.

**6. Comment from Expert**
    - Generate a comprehensive report in html format based on the analyzed information.

**7. More info**
    - You can view all of the data history that you previously analyzed.

---

## 📝 License

Chunghakdong Gyojungdang is freely available for free non-commercial use, and may be redistributed under these conditions. Please, see the [license](LICENSE) for further details.

---

## 🧷 References(gitHub Repo)

1. [tf-pose-estimation](https://github.com/ildoonet/tf-pose-estimation)
2. [open-pose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
3. [pose-trainer](https://github.com/stevenzchen/pose-trainer)
