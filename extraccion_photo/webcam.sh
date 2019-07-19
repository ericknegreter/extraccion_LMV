#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

fswebcam -S 20 --no-banner /home/pi/Documents/extraccion_photo/$DATE.jpg
