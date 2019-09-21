#How to use core

You just use class in run.py

First, you import the class

`
from pose_diff.core import run
`

Second, you choose applying only angle_diff. So if you want applying it, write this.

`
run.Video(trainer, user, exercise, diffing, way, average,'angle')
`

If you don't want to apply only angle_diff. Just remove 'angle'

`
run.Video(trainer, user, exercise, diffing, way, average,'angle')
`

The parameter are as follows


* exercise = 1  # 'pullup'
* way = 'round'  # round_up, round_down.
* average = 1  # 1은 apply 2는 non
* diffing = 'increase'  # decrease