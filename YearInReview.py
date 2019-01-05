#!/usr/local/bin/python3
#/Users/Ryan/anaconda/bin/python

import csv
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd
import numpy as np
import datetime
import calendar
from collections.abc import Mapping

# Constants
YEAR = 2018
#FIRST_DAY_OF_EACH_MONTH = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
FIRST_DAY_OF_EACH_MONTH = [datetime.date(YEAR, m, 1).timetuple().tm_yday - 1 for m in np.arange(1,13)]
EPSILON = 0.0000001

csvfile = './DataYearDates.csv'
#csvfile = './test.csv'

# Column names for DataYearDates file
header_hours = ['date','12am','12:30am','1am','1:30am','2am','2:30am','3am','3:30am','4am','4:30am','5am','5:30am','6am','6:30am','7am','7:30am','8am','8:30am','9am','9:30am','10am','10:30am','11am','11:30am','12pm','12:30pm','1pm','1:30pm','2pm','2:30pm','3pm','3:30pm','4pm','4:30pm','5pm','5:30pm','6pm','6:30pm','7pm','7:30pm','8pm','8:30pm','9pm','9:30pm','10pm','10:30pm','11pm','11:30pm']

# Activity object associates a name of an activity and a color
class Activity:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __str__(self):
        return 'Activity: {0}, Color: {1}'.format(self.name, self.color)

# Activities object maps activity ids (keys) with the associated Activity object
class Activities(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        else:
            raise AttributeError("No such attribute: " + key)

    def __setattr__(self, key, activity):
        self[key] = {'name': activity.name, 'color': activity.color}

    def __delattr__(self, key):
        if key in self:
            del self[key]
        else:
            raise AttributeError("No such attribute: " + key)

# activities is an iterable mapping of each activity id with its name and color
activities = Activities({
    1: Activity('sleep', '#d9d9d9'),
    2: Activity('prep', '#999999'),
    3: Activity('work','#a61c00'),
    4: Activity('food', '#0000ff'),
    5: Activity('transit', '#e69138'),
    6: Activity('health', '#6aa84f'),
    7: Activity('social', '#674ea7'),
    8: Activity('teresa', '#a64d79'),
    9: Activity('productive', '#434343'),
    10: Activity('read', '#b6d7a8'),
    11: Activity('downtime', '#4a86e8'),
    50: Activity('transit+read', '#93c47d'),
    51: Activity('transit+sleep', '#b7b7b7'),
    53: Activity('transit+work', '#85200c'),
    57: Activity('transit+social', '#351c75'),
    58: Activity('transit+teresa', '#741b47'),
    93: Activity('work productive', '#990000')
})

# Specify exact colors for each possible value DataYearDates
act_colors = [activities[a_id].color for a_id in sorted(activities)]
cmap = colors.ListedColormap(act_colors)

# bounds array must be one longer than the color list
bounds = [1,2,3,4,5,6,7,8,9,10,11,50,51,53,57,58,93,99]
#bounds = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
norm = colors.BoundaryNorm(bounds, cmap.N)
#print('cmap: {0}'.format(cmap.N))
#print('bounds: {0}'.format(len(bounds)))

# Read DataYearDates file into a dataframe using named columns
df_year = pd.read_csv(csvfile, header=None, names=header_hours)
# Convert 'date' field into datetime objects and set as index of the dataframe
df_year['date'] = pd.to_datetime(df_year['date'], infer_datetime_format=True)
df_year.set_index('date', inplace=True)
# Add a small value to each entry to ensure the correct coloring
df_year_graph = df_year.applymap(lambda x: x+EPSILON)

# Create a canvas and axes
fig, axes = plt.subplots(ncols=3, nrows=3, figsize=(14, 10))
fig.suptitle('Year in Review', fontsize=24)
# Get the GridSpec of the first axis in the first column
gs = axes[0,0].get_gridspec()
# Remove all but the first axis in the first column
for ax in axes[:, 0]:
    ax.remove()
# Extend the first axis in the first column to fill the whole column
ax_year = fig.add_subplot(gs[:, 0])
ax_year.set_title('Hourly Activity', fontsize=12)
ax_year.set_xlabel('Time')
ax_year.set_ylabel('Date')
xtickinterval = 8 # Every 4 hours
ax_year.set_xticks(np.arange(len(header_hours)/xtickinterval)*xtickinterval)
ax_year.set_xticklabels(header_hours[1::xtickinterval], fontsize=6, rotation=60, ha='right', rotation_mode='default')
# Rotate the tick labels and set their alignment.
#plt.setp(ax_year.get_xticklabels(), rotation=60, ha='right', rotation_mode='default')
#ytickinterval = 30 # Every 30 days
#ax_year.set_yticks(np.arange(len(df_year_graph.index)/ytickinterval)*ytickinterval)
#ax_year.set_yticklabels(df_year_graph.index.date[::ytickinterval], fontsize=6)

monthslabels = [p for pair in [['', m] for m in calendar.month_name[1:]] for p in pair]
monthsticks = [p for pair in [[day, day+15] for day in FIRST_DAY_OF_EACH_MONTH] for p in pair]
#ax_year.set_yticks([day+15 for day in FIRST_DAY_OF_EACH_MONTH])
ax_year.set_yticks(monthsticks)
ax_year.set_yticklabels(
    #df_year_graph.index.date[FIRST_DAY_OF_EACH_MONTH],
    #MONTHS_ABBREV,
    #MONTHS,
    monthslabels,
    fontsize=6,
    va='center',
    rotation=90, rotation_mode='default'
)
ax_year.imshow(df_year_graph, cmap=cmap, norm=norm)
#ax_year.matshow(df_year_graph, cmap=cmap, norm=norm)

axl = fig.add_axes([0.7, 0.2, 0.2, 0.5])
colorbar = mpl.colorbar.ColorbarBase(axl, cmap=cmap, norm=norm, ticks=bounds)

df_work = df_year[df_year == 3]
df_work_hours = df_work.count(axis=1).apply(lambda x: x/2).iloc[300:]
ax_work = axes[0,1]
ax_work.set_title('Hours Working')
ax_work.set_xlabel('Date')
ax_work.set_ylabel('Hours')
ax_work.plot(df_work_hours, color=activities[3].color)

df_sleep = df_year[df_year == 1]
df_sleep_hours = df_sleep.count(axis=1).apply(lambda x: x/2)
ax_sleep = axes[1,1]
ax_sleep.set_title('Hours Sleeping')
ax_sleep.set_xlabel('Date')
ax_sleep.set_ylabel('Hours')
ax_sleep.plot(df_sleep_hours)

#plt.tight_layout()
plt.show()
plt.close()
