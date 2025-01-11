#!/bin/python3

import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from datetime import datetime, timedelta


bg = '#ffffff'
fg = '#000000'
# Set default figure and axes background color to black
plt.rcParams['figure.facecolor'] = bg
plt.rcParams['axes.facecolor'] = bg

# Set default text color to white
plt.rcParams['text.color'] = fg

# Set default axes label, title, and tick color to white
plt.rcParams['axes.labelcolor'] = fg
plt.rcParams['axes.titlecolor'] = fg
plt.rcParams['xtick.color'] = fg
plt.rcParams['ytick.color'] = fg

class TimeEntry():
    def __init__(self, char, date, start_time, end_time):
        self.char = char
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
    

def parse_legend():
    # Read the legend file
    legend = {}
    with open('legend', 'r') as f:
        for line in f:
            if len(line.strip()) == 0:
                continue
            parts = line.strip().split(':')
            legend[parts[0].lower()] = (parts[1], tuple(map(lambda x: pow(float(x)/255, 1.2), parts[2].split(','))))
    return legend


def parse_entries(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    entries = []
    for line in lines:
        if not len(line.strip()):
            continue
        parts = line.split()
        char = parts[0]
        # date
        the_date = datetime.strptime(parts[1], '%Y/%m/%d')
        # times
        time_parts = parts[2].split('-')
        start_time = datetime.strptime(time_parts[0], '%H:%M')
        end_time = datetime.strptime(time_parts[1], '%H:%M')
        if start_time == end_time:
            continue
        entries.append(TimeEntry(char, the_date, start_time, end_time))
    return entries


def plot_weekly_time(entries):
    # Data processing
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    data = {day: [] for day in days}
    earliest_time = 23 * 60 + 59  # latest possible time in minutes (23:59)
    latest_time = 0  # earliest possible time in minutes (00:00)

    legend = parse_legend()
    
    for entry in entries:
        start_minutes = entry.start_time.hour * 60 + entry.start_time.minute
        end_minutes = entry.end_time.hour * 60 + entry.end_time.minute
        # Updating earliest and latest times
        earliest_time = min(earliest_time, start_minutes)
        latest_time = max(latest_time, end_minutes)
        #
        the_day = entry.date.strftime('%A')
        data[the_day].append((entry.char, start_minutes, end_minutes))

    fig, ax = plt.subplots(figsize=(8, 5))  # 700x500 pixels
    colors = dict()

    for idx, day in enumerate(days):
        y_bottom = earliest_time
        for entry in sorted(data[day], key=lambda x: x[1]):
            char, start, end = entry
            if char not in colors:
                colors[char] = legend[char][1]
            ax.add_patch(Rectangle((idx, start), 1, end - start, color=colors[char],
                                   label=f"{legend[char][0]}" if f"{legend[char][0]}" not
                                   in [rec.get_label() for rec in ax.patches] else ""))

    ax.set_xlim(0, len(days))
    times_range = range(earliest_time//60*60, ((latest_time-1)//60+2)*60, 60)
    ax.set_ylim(times_range[0], times_range[-1])
    ax.set_xticks([i + 0.5 for i in range(len(days))])
    ax.set_xticklabels(days)
    ax.set_yticks(times_range)
    ax.set_yticklabels([f"{i:02d}:00" for i in range(earliest_time//60, (latest_time-1)//60 + 2)])
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)
    plt.tight_layout()
    #
    plt.show()

if __name__ == "__main__":
    filename = sys.argv[1]
    entries = parse_entries(filename)
    plot_weekly_time(entries)
