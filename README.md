# PointyPy
Final Project of Data Analytics Bootcamp @IronHack Lisbon

PointyPy allows you to have control in the tip of your fingers!

It uses Machine Learning and Artificial Intelligence to detect and track the movements of your hand in your computer's camera, allowing you to control your mouse or a presentation without ever touching your computer!

OpenCV, MediaPipe and AutoPy were some of the resources used to make it work. Additionally flask, html and css were also explored to present the app through a GUI.

#### Check out the presentation @canva - https://www.canva.com/design/DAFTg7C_kUA/gcQJItoxuUYpFXyppYsANA/view?utm_content=DAFTg7C_kUA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

#### Graphical User Interface
![GUI](https://user-images.githubusercontent.com/111517561/207393936-2ab9d109-dabc-4647-b09d-94dc09dd7118.gif)

#### Mouse Controller Demo
![Mouse](https://user-images.githubusercontent.com/111517561/207393923-23e629fd-b9cd-40dc-8d78-a902d3030b2f.gif)

To control your mouse:
 - use the index finger to navigate through your screen;
 - join the index and middle finger to click (or double click, if you stay a little longer at the gesture);
 - using the index, middle and ring finger you maintain the left button on your mouse clicked, so you can use this to click and drag. 
 After the three fingers you drag using the index and release joining the index and middle finger.

#### Presentation Controller Demo
![Presentation](https://user-images.githubusercontent.com/111517561/207393932-1d3ed8eb-194b-4fc8-82d1-236d31d2f210.gif)

To control your presentation:
 - use your pinky finger to go to the next slide;
 - use your thumb to go to the previous slide; 
 - join the index and middle finger to use a "laser" pointer;
 - use the index finger to annotate(you can do as many annotations as you want, when you change slides the annotations will be cleared and not saved);
 - using the index, middle and ring finger you can erase the last annotation;
 - closing your whole hand, you will erase every annotation from the slide.
 
  
*The first two commands have to be done above the line that appears on the camera image, this allows you to move your hands freely and in a natural way when you're talking during the presentation.*
