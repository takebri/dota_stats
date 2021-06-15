import json
import os
import time

import pandas as pd
import requests

# gets current statistics about game heroes
def get_hero_stats():
    data = requests.get("https://api.opendota.com/api/heroStats").json()
    # write Pd object to csv
    pd.DataFrame(data).to_csv("hero_stats.csv", sep=",")
    # write to json
    with open('hero_stats.json', 'w') as out_file:
        json.dump(data, out_file, indent="")

get_hero_stats()