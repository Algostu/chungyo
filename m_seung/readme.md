# Screen

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
