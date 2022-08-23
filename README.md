# Alcatel-Lucent Enterprise Digital Age Network / OmniSwitch integration with RingCentral / Rainbow Office
In this respository I'll share findings/developments that shall serve as an inspiration on how to leverage the integration of [Alcatel-Lucent Enterprise Digital Age Network](https://www.al-enterprise.com/en/solutions/digital-age-networking) / [OmniSwitch](https://www.al-enterprise.com/en/products/switches) with [RingCentral](https://www.ringcentral.com/) / [Rainbow Office](https://www.al-enterprise.com/rainbow-office).

## Overview
<img width="960" alt="API-UseCases-ALE-OmniSwitch_Ringcentral" src="https://user-images.githubusercontent.com/5174414/186093853-9959e90d-b4b8-40ea-96ad-240ada4771bb.png">

## Setup for ALE Digital Age Network Notifications Add-In

1. Download `ringcentral_omniswitch.py`, `poe_trigger.py` & `ringcentral_webhook_secrets-template.py`
2. Deploy [requests](https://pypi.org/project/requests/) to your ALE OmniSwitch with AOS R8 (You can contact Alcatel-Lucent Enterprise Professional Service if you need help with that)
3. Add the ALE Digital Age Network Notifications Add-In from the RingCentral / Rainbow Office app store to the desired personal/team conversation and copy the webhook URL <br> ![dan-add-in](https://user-images.githubusercontent.com/5174414/186110716-3c3856af-1c68-4bb5-ab97-b0eea07ff52f.png)
4. Rename `ringcentral_webhook_secrets-template.py` to `ringcentral_webhook_secrets.py` and add the webhook URL from the previous step
5. Upload the three Python files to the OmniSwitch in `/flash/python`
6. Associate the type of notification you'd like to deliver to the RingCentral/Rainbow Office personal/team conversation and adapt the contents of `poe_trigger.py` according to your needs
```
 ________  ________  ________           ________  ________     
|\   __  \|\   __  \|\   ____\         |\   __  \|\   __  \    
\ \  \|\  \ \  \|\  \ \  \___|_        \ \  \|\  \ \  \|\  \   
 \ \   __  \ \  \\\  \ \_____  \        \ \   _  _\ \   __  \  
  \ \  \ \  \ \  \\\  \|____|\  \        \ \  \\  \\ \  \|\  \ 
   \ \__\ \__\ \_______\____\_\  \        \ \__\\ _\\ \_______\
    \|__|\|__|\|_______|\_________\        \|__|\|__|\|_______|
                       \|_________|                            
					       OmniSwitch 6465T

Router-> event-action trap pethPsePortOnOffNotification script /flash/python/poe_trigger.py

Router-> show event-action 
Script Time Limit (seconds): 60

 Type                   Name                      Script (/flash/python/...)    
------+---------------------------------------+----------------------------------
trap   pethPsePortOnOffNotification             poe_trigger.py
```
7. Save the configuration on your OmniSwitch
```
Router-> write memory flash-synchro
```
8. You'll now receive beautiful notifications like the following for the associated network events<br>
![ringcentral-notification](https://user-images.githubusercontent.com/5174414/186112895-aef90053-7e32-4942-a73a-1bd6d9adbfce.png)
