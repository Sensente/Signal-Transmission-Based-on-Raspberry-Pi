# TL;DR
This repo serves as a fundamental layer for acoustic transmission and receiving, providing data for further processing, such as wireless sensing.

The most important thing is that this repo could **eliminate the possibility of channel-shifting error** cases.

# Install procedures
- First, flash the provided image to your Pi storage card;
- After flash, ```cd seeed-voicecard```, then ```run sudo ./uninstall.sh```, and ```sudo reboot```, so as to uninstall the preinstalled package;
- After reboot, ```git checkout -b rel-v5.5 remotes/origin/rel-v5.5```, then ```run sudo ./install.sh --compat-kernel``` and reboot;
- Enjoy your Raspberry Pi with Respeaker now.

For those who use Pi as the carrier for wireless sensing, I wrote a sample script myself ```local_sine_wave.py```. This script will transmit the single sine wave and collect the reflected signals locally.
Please ensure you have installed the necessary packages and:

```
sudo python3 local_sine_wave.py
```

**If you don't want to lost in the rabbit hole, you can omit the following content. :P**

# What happened to the official repo? 
We have identified the errors with the latest official repo from Respeaker, including the following scenarios:
- Shifting channels data

We noted that, when collecting data, the Raspberry Pi may collect it in the wrong channel orders, which means that the channel ID cannot match the actual data.

A typical error case is shown as the following, where the $${\color{green}Green}$$ ID number is the actual correct ID, and the black ID number is the original one extracted from the Pi.
![image](https://github.com/user-attachments/assets/b97d1514-95a6-475e-a47e-126fdc71d65b)

Clearly, it has something wrong.

# What's the reason?
The main reason may lie in the ac108 chips, but we haven't pinpointed the reasons.


# Acknowledge
Without the community's help, this repo would not have been here.
