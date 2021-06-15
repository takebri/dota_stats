import json
import os
import time

import requests


# Download match data from opendota API
def get_match_by_id(match_id):
    m_id = str(match_id)
    # fetch match data
    response = requests.get("https://api.opendota.com/api/matches/" + m_id)
    # if successful
    if response.ok:
        print("GET:", m_id)
        # response.json data
        data = response.json()
        # write it to file
        file = open("download" + os.path.sep + m_id + '_data.json', 'w')
        json.dump(data, file, indent="")
        file.close()

# starting match_id
match_id = 5915008308

# match id to build 1000 matches, not all match_ids played
# match_id_end = 5915010226

# fetch 1000 matches
for i in range(1, 1000):
    get_match_by_id(match_id + i)
    time.sleep(2)
