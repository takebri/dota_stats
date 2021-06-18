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
#match_id = 5915008308

# current number of unique match_ids = 4797
# current match_id to add more matches, not every match_id played
match_id = 5915017435

# fetch 1000 matches
for i in range(1, 1000):
    get_match_by_id(match_id + i)
    time.sleep(2)
