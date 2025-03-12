import pandas as pd
import numpy as np


import requests
import dotenv
import os
import json

# get api keys
dotenv.load_dotenv()   
api_key = os.getenv("API_KEY")


#make the api request 
matches = requests.get("http://www.thebluealliance.com/api/v3/event/2025caph/matches", headers={"X-TBA-Auth-Key": api_key})
teams = requests.get("http://www.thebluealliance.com/api/v3/event/2025caph/teams", headers={"X-TBA-Auth-Key": api_key})

teamarr = []
for team in teams.json():
    teamarr.append(team["team_number"])    
    teamarr.sort()

scoutData = pd.read_csv("testData.csv")

def averageNumericalCategory(category):
    # make a temp frame to calculate tghe total values
    tempFrame = pd.DataFrame(data=np.zeros((len(teamarr), 2)), index = teamarr, columns=["catTotal", "numMatches"])

    # iterate through the data csv to append to tempframe
    for i in scoutData.index:
        row = scoutData.loc[i]
        catNum = row[category]
        # add value to category total
        tempFrame.loc[row["teamNumber"], "catTotal"] = tempFrame["catTotal"][row["teamNumber"]]+catNum
        # increase number of matches
        tempFrame.loc[row["teamNumber"], "numMatches"] = tempFrame["numMatches"][row["teamNumber"]]+1

    # construct a return data frame by dividing the categorical total by the number of matches to find categorical average
    returndf = pd.DataFrame(data = tempFrame["catTotal"]/tempFrame["numMatches"], index=tempFrame.index, columns=["averages"])
    returndf = returndf.fillna(0)
    return returndf
    

def normalizeAverages(df):
    #define max min and range to normalize
    max = df["averages"].max()
    min = df["averages"].min()
    range = max-min

    #return the normalized array
    returndf = pd.DataFrame(data = ((df["averages"]-min)/range).to_numpy(), index=df.index, columns=["normalized average"])

    return returndf

# tests
print(normalizeAverages(averageNumericalCategory("autoL1Scores")))