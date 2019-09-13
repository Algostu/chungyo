# **pose_diff**

## frame_filtering(user,trainer)

When comparing video attributes, the frame of the trainer and the user is usually incorrect. So *frame_filtering* is a method to match the frame of them. There are 2 methods, and we will try to realize which one is the most accurate.

1. Match many frames with fewer frames proportionally
2. Pick frames by step

> ### frame_filtering *proportionally*
> 
> - user, trainer : npy file
> 
> Comparing length of npy file to match many frames with fewer frames and Choose frames from many frames. To match the number with the fewer frame. Inform what is bigger and return npy file picked with split number.

`code`
````
if trainer_frame > user_frame:
    recom = "trainer"
    resize = np.zeros(user.shape)
    split = int(trainer_frame / user_frame)
    cnt = 0
    while cnt < trainer_frame:
        resize[cnt] = trainer[cnt]
        cnt = cnt+split

elif trainer_frame < user_frame:
    recom = "user"
    resize = np.zeros(user.shape)
    split = int(user_frame / trainer_frame)
    cnt = 0
    while cnt < trainer_frame:
        resize[cnt] = user[cnt]
        cnt = cnt + split
else:
    recom = "no"
    resize = "no:
````

-----

## angle_difference(trainer,user,exercise)

It is a method that checks the error of the trainer and the user with angle. *angle_difference* get the type of exercise and decide the body part to be calculated. It calculates the angle using *evaluate_pose* and compares their.

This is the code when exercise is pullup. The margin of error is 1. The frame beyond the margin of error is changed the color section into 0(RED)
````
if exercise == 'pullup':
    i=0
    while True:
         if i > len(user):
                break

        if (trainer_x[i]+1<user_x[i] or trainer_x[i]-1>user_x[i]):
            angle_np[i][2][2] = 0

        elif (trainer_y[i]+1<user_y[i] or trainer_y[i]-1>user_y[i]):
            angle_np[i][3][2] = 0

        elif (trainer_z[i]+1<user_z[i] or trainer_z[i]-1>user_z[i]):
            angle_np[i][4][2] = 0
        else:
            angle_np[i][4][2] = 1
        i= i+1
    return angle_np
````

----

## point_differnce(trainer, user, exercise)

This method is almost the same as above. Check the error of the trainer and the user with point. The margin of error is 0.5 and also the frame beyond the margin of error is changed the color section into 0(RED)
````
if exercise == 'pullup': 
    while True:
        if (user_x[i] == None or user_y[i] == None or trainer_x[i] == None or trainer_y[i] == None or i == 120):
            break

        if (trainer_x[i] + 0.5 < user_x[i] or trainer_x[i] - 0.5 > user_x[i]):
            point_np[i][2][2] = 0

        elif (trainer_y[i] + 0.5 < user_y[i] or trainer_y[i] - 0.5 > user_y[i]):
            point_np[i][3][2] = 0

        elif (trainer_z[i] + 0.5 < user_z[i] or trainer_z[i] - 0.5 > user_z[i]):
            point_np[i][4][2] = 0
        else:
            point_np[i][4][2] = 1
        i = i + 1
return point_np
````

----

## diffing(trainer,user,exercise)

The changer the user and trainer npy file using above methods. It consists of three stages.

1. frame_filtering
2. angle,point difference with resize npy file
3. return user and trainer changed color and frames

````
recom, resize = frame_filtering(user, trainer)

if recom == "trainer":
    trainer = resize
    anglenp = angle_difference(trainer,user,exercise)
    pointnp = point_difference(trainer,user,exercise)
    for a,b in zip(anglenp,pointnp):
        for i in range(0,18):
            if a[i][2] == 0 and b[i][2]==0:
                user[i][2] = 0
else:
    user = resize
    anglenp = angle_difference(trainer, user, exercise)
    pointnp = point_difference(trainer, user, exercise)
    for a,b in zip(anglenp,pointnp):
        for i in range(0,18):
            if a[i][2] == 0 and b[i][2]==0:
                user[i][2] = 0

return user,trainer
````

# **run**

## How to use
Run have two class.

- Video(trainer, user, exercise)
- Real_time(npyfile)

Once, import the run class as 

````
from m_seung import run
````

> ### Video class
> 
> You need two npy file to compare the various things of skeleton.
> Designate the user path of npy file, trainer path of npy file and exercise with string.
> Use as the code.

````
user = "data/user/IU/walk/trained_skeleton.npy"
trainer = "data/trainer/IU/walk/skeleton.npy"
exercise = "pullup"

run.Video(user,trainer,exercise)
````

> ### Real_time class
> 
> This is simply a class to show the user skeleton when it is real time. So you only need to specify one path of npy file.
> Use as the code.

````
user = "data/user/IU/walk/trained_skeleton.npy"

run.Real_time(user)
````

# **Screen**

## Attribute
> * point
> * accuracy
> * angle
> * fps
> * time
> * msg
----

## Define
> To show a variety of circumstance upper things.

## draw_human(point)
> draw_human can make skeleton using openCV with making circle and line
>````
>cv2.circle(self.img,center,10, Coco.CocoColors[num], thickness, lineType, shift)
>cv2.line(self.img, centers[pair[0]], centers[pair[1]], Coco.CocoColors[pair_order], 3)
>````

## Display Define
Using cv2.putText, we show to user a several things.
> * display_accuracy
> * display_fps
> * display_times
> * display_msg
> * display_angle
> ````
> cv2.putText(img, text, location, font, fontScale, color, thickness)
> ````

# Calculate_angle

The new Issue#11 in github is need to calculate the angle. So I make some new definition for claculation.

## angle_betwee_vectors_degrees(u,v)
This return angle into degree between two vectors.

## Calculate_angle(a,b,c)
The definition can calculate the angle with given point a,b,c.
Point b is inner point. It works on latitude/longitude radians space.

First, we convert the point in tuple to point in numpy.
```
a = np.radians(np.array(point_a))
b = np.radians(np.array(point_b))
c = np.radians(np.array(point_c))
```

Second, make the vector and adjust the scale into 2D space
```
adjust = b[0]
vec1[1] *= math.cos(adjust)
vec2[1] *= math.cos(adjust)
```

## get_angle(npy file, npy file)
Anglepairs in coco.py is the collection that can be measure part on Openpose in coco.
So, get_angle can return the angle that each part of body using Anglepairs and npy file.
The thing to be careful about at this time is that the point of cabinet must be always centered on.