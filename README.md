# IRcamSLAM
Use IR positioning camera to get transformation matrix between the object and camera.
This is a *ROS package*, developed in ROS-Kinetic

[![](http://img.youtube.com/vi/idRZSgrLW1o/0.jpg)](http://www.youtube.com/watch?v=idRZSgrLW1o)<br>

### What does it do
This IRcam ROS Package uses [IR Positioning Camera](https://www.dfrobot.com/product-1088.html)(a diversion of WII controller) on **Raspberry Pi 3** to get 4 brightest points from IR LEDs, and calculates a transformation matrix between the camera and IR-LED-plane.

>This infrared positioning camera can be controlled with Arduino, AVR via I2C interface. It is able to track mobile infrared points and to transmit the data back to host. The horizontal angle of camera is 33 degrees while the vertical angle is 23 degrees. It returns up to four points at a time when identifies an object. With advantages of high resolution, high sensitivity, high accuracy, small build and light weight, this Positioning IR Camera an be widely used in robot automatic search, robot soccer game, mobile trajectory recognition.

> **SPECIFICATION**
>* Operating voltage: 3.3-5v
>* Interface: I2C
>* Detecting distance: 0~3m
>* Horizontal detecting angle: 33 degrees
>* Vertical detecting angel: 23 degrees
>* Dimensions: 32mm x 16mm(1.26x0.63")
>* Resolution is 128x96 pixel, with hardware image processing, which can track four objects (IR emitting or reflecting objects)

### Steps
* Connect IRcamera to Raspberry Pi 3 using following wiring diagram.<br>
  <img src="https://raw.githubusercontent.com/ccc159/IRcamSLAM/master/IRCame_Wiring.png" width="400"/>
* (OPTIONAL) You can connect a Beeper or normal LED at GPIO17 to indicate whether the IR cam detects IR LED.<br>
* Activate Raspberry Pi 3 I2C protocol.
* (OPTIONAL) Test the IR Camera on I2C port. 
  * When IR Camera is connected, you can type `sudo i2cdetect -y 1` in Terminal. If the sensor is connected and working you will see:
  * ```
    0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    50: -- -- -- -- -- -- -- -- 58 -- -- -- -- -- -- -- 
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    70: -- -- -- -- -- -- -- -- 
    ```
  * The sensor address is ```0x58```
* Build this package in `ROS catkin`, and run it! *Follow [this](https://github.com/ros-industrial/industrial_training/wiki/Installing-Existing-Packages#52-download-and-build-a-package-from-source) if you don't know how to build a ros package from github.*
