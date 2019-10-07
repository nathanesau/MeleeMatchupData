# python script to scrape data from https://liquipedia.net/smash/SSBMRank

from bs4 import BeautifulSoup
import requests
import os.path
import time
from database import *


def scrapeSSBMRankData():  # output to data/ssbmrank.data
    url = "https://liquipedia.net/smash/SSBMRank"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    ssbm_rank_dict = {}
    for table in soup.find_all('table', {'class': 'sortable wikitable'}):
        tdata = []  # list of [Rank, Player]
        th_tags = table.find_all('th')
        table_name = th_tags[0].contents[0]
        tr_tags = table.find_all('tr')
        row_no = 0
        for row in tr_tags:
            rdata = []  # [Rank, Player]
            if row_no != 0 and row_no != 1:  # header 1, header 2
                td_tags = row.find_all('td')
                data_no = 0
                for data in td_tags:
                    if data_no != 1 and data_no != 3 and data_no != 4 and data_no != 5:  # country, flag, mains, pm
                        if data_no == 0:
                            rank = data.contents[0]
                            rdata.append(rank)
                        if data_no == 2:
                            pname = data.find_all('a')[0]['title']
                            rdata.append(pname)
                    data_no += 1
                tdata.append(rdata)
            row_no += 1
        ssbm_rank_dict[table_name] = tdata

    db = Database("data/ssbmrank.db")
    for tname, playerData in ssbm_rank_dict.items():
        tname = tname.replace(' ', '')
        tname = tname.replace('\n', '')
        db.SaveSSBMRankData(tname, playerData)


def scrapeSetCount(p1name, p2Name):
    # ensure 1 second delay between queries (avoid getting blocked from API access)
    time.sleep(1)
    baseurl = "https://liquipedia.net/smash/index.php?title=Special%3ARunQuery%2FMatch_history&" + \
        "pfRunQueryFormName=Match%20history&Head_to_head_query[player]=P1Name&Head_to_head_query[opponent]=" + \
        "P2Name&Head_to_head_query[game]=Melee"
    url = baseurl
    url = url.replace('P1Name', p1Name)
    url = url.replace('P2Name', p2Name)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    stats_tags = soup.find_all('span', {'class': 'stats-value'})
    try:
        set_count = stats_tags[0].contents[0]
        return set_count
    except:  # no matchup data available for (p1Name, p2Name) provided
        return None


# uncomment to download SSBM rank lists for melee
# scrapeSSBMRankData("data/ssbmrank.db")

ssbm_rank_dict = {}
db = Database("data/ssbmrank.db")
db.LoadSSBMRankData(ssbm_rank_dict)

# example:
# download matchups for MPGR2019Summer
playerData = ssbm_rank_dict["MPGR2019Summer"]
nplayers = len(playerData)
matchup_dict = {}
for i in range(nplayers):
    for j in range(nplayers):
        if i != j:
            p1Name = playerData[i][1]
            p2Name = playerData[j][1]
            mname = (p1Name, p2Name)
            if mname not in matchup_dict:
                setcount = scrapeSetCount(p1Name, p2Name)
                try: # setcount available
                    dashpos = setcount.find('-')
                    parenpos = setcount.find('(')
                    wins = int(setcount[:dashpos])
                    losses = int(setcount[dashpos+1:parenpos])
                except: # setcount not available
                    wins = -1
                    losses = -1
                matchup_dict[mname] = {'wins': wins, 'losses': losses}
        print("finished (" + str(i) + ", " + str(j) + ")")

db = Database("data/ssbmrank.db")  # reload database
db.SaveMatchupData(matchup_dict)
