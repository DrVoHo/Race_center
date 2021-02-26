# Race_center
A Race center for time and lap tracking. Designed for a Märklin Sprint slot car race track. Scale 1:32.
Design is on Thingiverse.

Features:
-	Training: count up time and laps
-	Qualification: count down time
-	Race: count down laps
-	Advantage (laps in advance) for weak driver or slower cars or compensation for unbalanced track
-	Start control with start light and false start detection
-	Optional buzzer for start and finish.
-	No dependency on track position – can be placed on any place, because sensor is not placed inside the lane.

Installation:
- copy all files (including pad4pi folder) to the /home/pi directory
- activate I2C bus with raspi-config
- enable boot without login
- sudo apt-get install i2c-tools
- check I2C bus with sudo i2cdetect -y 1
- pip3 install smbus2
- pip3 install RPLCD
- pip3 install adafruit-pca9685

To start script on boot modify /etc/rc.local and insert following line just before  'exit 0'
sudo -H -u pi python3 /home/pi/Race_center.py  &

Port_IO.py needs to be adjusted to the used configuration. To distinguish between 2 and 4 track configuration just define only 2 sensors. Everything else will be adjusted. 
Change language in globals.py by setting 'english = True' (False will enable German)
