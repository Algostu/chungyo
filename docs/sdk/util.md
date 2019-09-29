# Common

## Check_accuracy(frames, ex_type)

**Params**  
frames: numpy array, ex_type: integer

* frames: parsed video file that will be analyzed to check whether it contain several human body parts required for certain exercise.
* ex_type: specify which human body parts are required, according to this option

**How it works**  
This function determine whether input *frames* are proper to be used for analyzing *target exercise*.

**return Values**  
* Return Type: Tuple
* Return Value Type: (boolean, float)
* Return Value List: (relevance, accuracy)
