# pose-difference
---
## Build Status
[![Build Status](https://travis-ci.org/I-Love-IU/pose-difference.svg?branch=dev)](https://travis-ci.org/I-Love-IU/pose-difference)

## Installation
**Test environment**
* windows 10
* please add if you have ideas :)

**Dependencies**
+ tf-pose-estimation
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
you(seung-min, da-ani, byung-hun) can start this project with below sample codes. This code is for checking dependencies needed in your computer. **So before you started, make sure that these sample codes are working properly in your computer.**
````
# 1
# for check tf-pose are installed for your computer in packages
python main.py --mode check

# 2
# for check your modules
python main.py --mode [m_da | m_seung | m_byung]
````
***Result***
````
# 1
Hello Pose Difference

# 2
hello byunghun-world
hello daan-world
hello seungmin-world
````

---
## Development Rules
1) **How to Commit to Main Repository**
    * **push to repo**  
        *This section should be updated in the future.*
    * **pull from repo**  
        *This section should be updated in the future.*
    * **how to write commit message**  
        Commit message is important when you want to corporate with others. There are two tips: write better commit message, how to read others commit message. This is not a tutorial for commit message, but just give you important note that should be followed in our projects. First, you should check how other well-known repository's commit message works. These are examples: [linux][9], [spring][10]. If you check these site, please read below guide lines.
        + Separate subject from body with a blank line
        + Limit the subject line to 50 characters
        + Capitalize the subject line
        + Do not end the subject line with a period
        + Use the imperative mood in the subject line(imperative means sentence start with Verb)
        + Wrap the body at 72 characters
        + Use the body to explain what and why vs how

        Among these guide lines, we only follow rules related to subject, cause we write document about body. So you can write your commit message body as you want to. Second, you should check others commit message. There are many other ways to learn about it. So Google it or please check [This site][8].

    * **Bugs and Issues**  
        You just ask to any person via kakao message, but there are more better way to ask your questions. If you want to ask via message, we are gonna be very happy if you upload your question link instead of pictures.

        If you want to ask your question only for us, just use github issue form.
        ![github issue][6]
        But you can ask your question in wellknown question-site such as [stack overflow][7]. Both cases are require to specify your problem code and working environment in details. After upload your question, leave your question-link in either kakao chat room or trello. Or just keep it until meeting and ask in person(Maybe Best Way, lol!!)

2) **Comments and Coding Rules**
    * **Coding Rules**
        1. **Naming Convention**  
            There are numerous ways in naming convetions. But we only follow these : *it should be Meaningful and if you choose to change your variable name, please update it to your document.* Below list are type of name convention python usually follow. (search for details)
            * Function Name : Underscore
            * Class Name : Camel case
            * Variable Name : Underscore
            * Parameter Name : Underscore
        2. **Test Unit**  
            *This section should be updated in the future.*  
            Before using any tools, I recommend you test your code like below sample code.(I mean testing your program by unit of modules)
            ````
            # any_modules_you_made.py
            def increase(v1, v2):
                v1 += 1
                v2 += 1
                return v1, v2
            if __name__="__main__":
                test_var_1, test_var_2 = 1, 2
                print(increase(test_var_1, test_var_2))
       
    * **Comments Rules**  
    There are two type of comments you must write. Others are optional, but these two types must be written in order to make source file read easily by not only other people, but mainly yourself.
    First, write comments per files(moduel). This comments has form to follow, So just copy, paste and modify it.
        ````
        '''
        * Writer : your name
        * Last updated : 2019-08-18
        * About what : explain about this files
        * contens : list functions and classes that are inside of this files
        '''
        ````
        Second, add comments just above class or method, which explain what is these things for. You dont need to follow any rules, so any types are acceptable.
        ````
        # this function is for analyzing 'shoulder press motion'
        def _shoulder_press(pose_sequence):
            # define your function here
        ````
        Last, you should not feel any anxiety for writing english comments.(best parts, isnt it?) we are damm korean. **I LOVE KING SEJONG!!!**
3) **Writing Document**  
    *This section should be updated in the future.*  
    There are two types of document you should write. First, classes diagram and flow char diagram.(not exact words) Second, Readme.md of your modules. Readme.md of your modules includes explanation of functions and classes. Each Explanation has follwing fortmats.

    > moduleName.functionName(param1, param2, param3):
    > 1. explanation for params
    > 2. explanation for functions (including return value)
    > 3. bugs and limits


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
