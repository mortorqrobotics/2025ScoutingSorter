import pandas as pd
import numpy as np
import requests

df = pd.read_csv("testData.csv")
r = requests.get('https://www.thebluealliance.com/api/v3', auth=('user', 'pass'))

print(df)