import requests, json, time, os
import pandas as pd
from matplotlib import pyplot as plt

#  fill with [match_id, hero_id, win]
db = []

for f in os.listdir('download'):
    file = open('download' + os.sep + f)
    data = json.load(file)
    file.close()

    # skip errors
    if "error" in data.keys():
        continue

    # skip matches with bots
    if data["human_players"] != 10:
        continue

    # skip matches with no pick data
    if not data['picks_bans']:
        continue

    # radiant = team 0
    win_team = 0
    if data["radiant_win"] == False:
        win_team = 1

    # get pick info
    picks = pd.DataFrame(data['picks_bans'])
    picks = picks[picks.is_pick] # drop bans
    picks = picks.sort_values("order") # sort by order

    # add last two picks to database
    db.append(
                [data['match_id'],
                picks.iloc[-1].hero_id,
                picks.iloc[-1].team == win_team]
                )

    db.append(
                [data['match_id'],
                picks.iloc[-2].hero_id,
                picks.iloc[-2].team == win_team]
                )

db = pd.DataFrame(db, columns = ['match_id', 'hero_id', 'win'])

# keep heroes with at least 50 samples
count = db.hero_id.value_counts()
keep = count[count > 50].index
db = db[db.hero_id.isin(keep)]


# calculate winrate
winrate = db.groupby('hero_id')['win'].mean()
winrate = winrate.sort_values()


# hero_id to hero_name
heroes = pd.read_csv('hero_stats.csv')[['name', 'hero_id']]
lookup = {k: v[14:] for k, v in zip(heroes.hero_id, heroes.name)}
#print(heroes.hero_id, heroes.name)
def id2name(ids):
    return [lookup[i] for i in ids]


# visuals
N = 10
bot10 = winrate.iloc[:N]
top10 = winrate.iloc[-N:]

fig, ax1 = plt.subplots()

ax2 = ax1.twiny()

ax1.bar(range(N), 100 * top10.values)
ax1.bar(range(N), 100 * bot10.values)

ax1.set_xticks(range(N))
ax1.set_xticklabels(id2name(bot10.index))
ax2.set_xlim(ax1.get_xlim())
ax2.set_xticks(range(N) )
ax2.set_xticklabels(id2name(top10.index))
ax1.tick_params(axis = 'x', rotation = 30)
ax2.tick_params(axis = 'x', rotation = 30)
ax1.set_ylabel('winrate')

ax1.set_title('Top/Bottom 10 winrate for last picks - ')
ax1.axhline(y = 50, linestyle = '--', color='red')

# plt.bar(id2name(top10.index), top10)

plt.show()