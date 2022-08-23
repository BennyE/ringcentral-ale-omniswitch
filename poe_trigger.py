#!/usr/bin/env python3

import sys
import getopt
import json
import subprocess

# Based upon work done by Patricio Martelo and Benny Eggerstedt in 2015
# Some corrections and enhancements done by Benny in 2020 & 2022

# ['/flash/python/poe_trigger.py', '-t', 'pethPsePortOnOffNotification', '-d', '{"sysUpTime":821917120,"pethMainPseGroupIndex":1,"pethPsePortIndex":8}']

# Load the data that is being sent to us
# -t holds the traptype
# -d holds the trapdata
try:
    opts, args = getopt.getopt(sys.argv[1:], "t:d:")
except getopt.GetoptError as err:
    print(err)
    print("{0}".format(sys.argv))
    sys.exit(2)
traptype = "(none)"
trapdata = "{}"

# Go through the data in opts and allocate it properly
# traptype gets the value from -t
# trapdata gets the value from -d
for o, a in opts:
    if o == "-t":
        traptype = a
    elif o == "-d":
        trapdata = a

trapdetail = json.loads(trapdata)

# Limited to port 1/1/8 on purpose for the demo
# Contact Alcatel-Lucent Enterprise Professional Service for help on the implementation or customisation wishes
if trapdetail["pethMainPseGroupIndex"] == 1 and trapdetail["pethPsePortIndex"] == 8:
    # Ringcentral / Rainbow Office
    subprocess.run(["python3", "/flash/python/ringcentral_omniswitch.py", "send_notification_card", f"PoE Device DOWN {trapdetail['pethMainPseGroupIndex']}/{trapdetail['pethPsePortIndex']}!"])
