Power Inventor
===
### Background and Goals
The Power Inventor is relay controller with the goal of being a consistent means of controlling AC Powered Devices. The goal is to seperate the power control aspects of a Maker's project, with the sensing part of the project. In this way, the Power Inventor can be a UL Listed device that Maker's can use in their AC powered projects.

### Big Picture
This project is meant to run on a Rasperry Pi, and the code creates a webserver for users to interact with the relay device. The Webserver is the CherryPy webserver, which is an easy way to create Python web applications. Also, this project was built with ResinOS. ResinOS is open-source container OS that allows using Docker containers on the Raspberry Pi.

### Operation
1. Go to Resin.io, create an account, and create a new image for the Raspberry Pi with your device and network settings.
2. Burn memory card with image, and power-up the Raspberry Pi, after ~10mins the device will show up on Resin.io's dashboard.
3. Clone this repository on your own computer. 
4. Install Resin.io's command line tools, and log into your Resin.io account.
5. Run BASH command: git push resin master
6. This will create a container with this repo's code, install all dependancies, and run it on your Raspberry Pi.
7. Locate IP address of your Raspberry Pi from dashboard or other means.
8. Browse to ip address in your browser, and start controlling AC Outlets!
9. Sign up for a service like no-ip, and you can access your outlets from anywhere with a convenient web address.


