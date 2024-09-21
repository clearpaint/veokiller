# veokiller
Capstone work on video analysis

Week 1: Reviewed a few differnt options for capstone work: 

Option 1: Write some video analysis tools that can detect players do segmentation etc. 

Option 2: Design a system that looks just like VEO's for ~$300 and do option 1 on devivce.

Option 3: Man in the middle hack the existing VEO infrastructure used to upload the video.
#3 might happen as a result of my experimentations with #2. 

Week 2: 
At anytime one of the above options might be where we end up , although the intent is to stick with 1/2.

Option 1 highlevel plan:

Use a dell poweredge server I already have add a GPU ~ NVIDIA RTX 3080 or similar, reimage it with latest ubuntu setup the tool chains try some experiments with OpenCV  ultimate goal is to find and track players based on name and jersey number, although theres a number of intermediate goals those need to be gauged as work progresses.

Option 2 highlevel plan:

Reviewed HW requirements for video collection and offline analysis.
Video Collection Stitching and close to source AI features following/segmentation:
Processor SOM: https://www.seeedstudio.com/Jetson-10-1-A0-p-5336.html
Camera Module(s): https://a.co/d/hOJH2Og  or https://a.co/d/42IJGB2

NVIDIA Jetson boards come packed with developer tools and are ment to be an out of the box video AI platform.

https://github.com/mkoshkina/jersey-number-pipeline

Option 3 highlevel plan:

Aquire a ~high end ethernet TAP , connect my VEO cam through the TAP capture rx/tx do the analysis , spoof server side and capture video packets , reasemble packets into a video. No more need for subscrition service. 


Start playing with this before hardwares in https://github.com/Seeed-Projects/jetson-examples/blob/main/reComputer/scripts/ultralytics-yolo/README.md
