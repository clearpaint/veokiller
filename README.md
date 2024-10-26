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



Week 3:
Received NVIDA Jetson Xavier NX Dev kit.
Loading image https://developer.nvidia.com/embedded/jetpack-sdk-514 
Will try and get a simple project going and feed it some video . 

Had a little trouble, the BSP on the device was for a really old image, had to download and install an ancient version on the sd card and load Ubuntu. I have the developer kit booting up and the serial connection working. 

Next is to start a small project and learn the compilers for this stuff. 

https://www.nvidia.com/en-us/on-demand/session/gtcspring21-s31351/

Week 4: Worked through all kinds of issues with the NVIDIA SDK Manager clunky and not really a great first experience with their tool chain. Did get to run some code on the device, but the dependcies hell is real, mis match on packages and the board being a little older means i can just get latest and have to cherry pick changes, which is just about impossible.
was able to process some vide using YOLO , it works the further segmentation and following , i cant really do without heavier duty pc. 

Week 5: Pivoted to developing the front end of the interface, have a Lite Flask Web server (Flask Video Viewer) up and mostly feature complete. this will get intigrated into the video AI portion later.

Week 6: Ordered a NVIDIA T4 , going to put in an older server I have , setup tool chain and try running the code there , seeing as how the depends hell of doing it on the older Jetson just was not going to work out. Still plan to come back to the embeded HW to try and do the video capture at a minimum. 

Week 7: Get the existing code running on the server.. Both the front end and early detection. 

