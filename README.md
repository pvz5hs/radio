Change receipient_email variable in the python file. After that, type the following into terminal:
crontab -e

PASTE the folowing into the bottom:
EMAIL_PASSWORD = 'Password'
*/5 * * * * '/usr/bin/python3' '/home/sdr-user/Desktop/radio/ipchecker.py'

replace password, path to python and the file, as well as the */5 * * * * ' to change the interval as necessary. 
If you want to test locally you need to set the environment variable in the folder with export EMAIL_PASSWORD=”password”
