# Embedded Code

This is where you can find the code for the Nucleo F446RE MCU.

You can either grab the binary (.bin) and flash the lastest firmware. Or develop further by downloading the .zip folder which contains the CubeMX project.

### Behind the scenes

In essence the Nucleo controls the functionality of the heart. It generates the natural signals you read with the pacemaker, but it also reads the pacemaker signals, sends the data over serial (UART) and accepts changes in functionality. You can read more about it in section 2.1.2 of the HeartView Document (course_dev >> documentation >> heartview_explained >> intro_to_heartview.pdf). 
