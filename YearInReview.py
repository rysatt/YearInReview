#!/Users/Ryan/anaconda/bin/python
#/usr/local/bin/python3

import csv
import sys
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib as mpl
import pandas as pd
import numpy as np
from datetime import datetime

csvfile = './DataYearDates.csv'
#csvfile = './test.csv'


"""
dataYear = []
with open(csvfile, 'rU') as csvdict:
    csvreader = csv.reader(csvdict)
    for row in csvreader:
        dataYear.append(row)

print(len(dataYear))
"""

header_hours = ['date','12am','12:30am','1am','1:30am','2am','2:30am','3am','3:30am','4am','4:30am','5am','5:30am','6am','6:30am','7am','7:30am','8am','8:30am','9am','9:30am','10am','10:30am','11am','11:30am','12pm','12:30pm','1pm','1:30pm','2pm','2:30pm','3pm','3:30pm','4pm','4:30pm','5pm','5:30pm','6pm','6:30pm','7pm','7:30pm','8pm','8:30pm','9pm','9:30pm','10pm','10:30pm','11pm','11:30pm']

cmap = colors.ListedColormap([
    '#d9d9d9', #1
    '#999999', #2
    '#a61c00', #3
    '#0000ff', #4
    '#e69138', #5
    '#6aa84f', #6
    '#674ea7', #7
    '#a64d79', #8
    '#434343', #9
    '#b6d7a8', #10
    '#4a86e8', #11
    '#93c47d', #50
    '#85200c', #51
    '#351c75', #57
    '#741b47', #58
    '#990000'  #93
])
bounds = [1,2,3,4,5,6,7,8,9,10,11,50,51,53,57,58,93]
norm = colors.BoundaryNorm(bounds, cmap.N)

df_year = pd.read_csv(csvfile, header=None, names=header_hours)
df_year['date'] = pd.to_datetime(df_year['date'], infer_datetime_format=True)
df_year.set_index('date', inplace=True)
print(df_year)

print(type(df_year.index[0]))

fig, ax = plt.subplots()
ax.set_title('Year in Review')
ax.set_xlabel('Time')
ax.set_ylabel('Date')
ax.set_xticks(np.arange(len(header_hours)/2)*2)
ax.set_xticklabels(header_hours[1::2])
# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=60, ha='right', rotation_mode='default')
ax.set_yticks(np.arange(len(df_year.index)))
ax.set_yticklabels(df_year.index.date)
ax.imshow(df_year, cmap=cmap, norm=norm)

plt.show()
plt.close()
