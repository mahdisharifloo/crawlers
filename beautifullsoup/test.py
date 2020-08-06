import numpy as np
import requests

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
# you can also import SoftwareEngine, HardwareType, SoftwareType, Popularity from random_user_agent.params
# you can also set number of user agents required by providing `limit` as parameter
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
# Get Random User Agent String.
ua_change = True
while ua_change:
    user_agent = user_agent_rotator.get_random_user_agent()
        
    headers = {
            'user-agent': user_agent,
            }
r = requests.get('example.com',headers=headers)