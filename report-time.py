#!/bin/python3

import sys
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

if len(sys.argv) < 2:
    print("usage: python report-time.py <week_data.txt>")
    exit(0)

# Read contents from the example_week.txt
with open(sys.argv[1], 'r') as f:
    week_entries = f.readlines()

# check for day option
one_day = False
if len(sys.argv) == 4:
    if sys.argv[2] == "--day":
        one_day = sys.argv[3]

    
# Read contents from the legend
with open('legend', 'r') as f:
    legend_entries = f.readlines()

# Parse the legend and create a dictionary
legend_dict = {}
for entry in legend_entries:
    if not len(entry.strip()):
        continue
    parts = entry.strip().split(':')
    key = parts[0].lower()
    name = parts[1].split(':')[0]
    r, g, b = map(int, parts[2].split(','))
    legend_dict[key] = {
        "name": name,
        "color": mcolors.to_rgba((r/255, g/255, b/255)),
        "time_spent": 0  # Initializing time spent for each task as 0
    }

# Calculate time spent for each task in the week
for entry in week_entries:
    if not len(entry.strip()):
        continue
    key, date, time_range = entry.strip().split(' ')[:3]
    day = date.split('/')[2]
    if one_day and day != one_day:
        continue
    start_time, end_time = time_range.split('-')
    time_format = "%H:%M"
    elapsed = datetime.strptime(end_time, time_format) - datetime.strptime(start_time, time_format)
    minutes_spent = elapsed.total_seconds() / 60
    legend_dict[key]["time_spent"] += minutes_spent

# Plotting
labels = [v["name"] for k, v in legend_dict.items() if v["time_spent"] > 0]
sizes = [v["time_spent"]/60 for k, v in legend_dict.items() if v["time_spent"] > 0]  # Convert to hours
colors = [v["color"] for k, v in legend_dict.items() if v["time_spent"] > 0]

fig, ax = plt.subplots()
ax.bar(labels, sizes, color=colors)
ax.set_ylabel('Minutes Spent')
ax.set_title('Time Spent on Tasks')
plt.xticks(rotation=45, ha='right')

# calculate total
total_time = sum(sizes)
#break_time = legend_dict['/']['time_spent'] / 60
#total_time -= break_time
ax.annotate(f'Total: {total_time:.2f} hours', xy=(0.75, 0.95), xycoords='axes fraction', fontsize=10, color='black')

# Reporting exact numbers to stdout
print("---")
for k, v in legend_dict.items():
    if v["time_spent"] > 0:
        # Convert minutes to hours for reporting
        hours_spent = v["time_spent"]/60
        print(f"{v['name']}: {hours_spent:.2f} hours")
print("---")
print(f"total: {total_time:.2f} hours")

# show visual report
print("...")
plt.tight_layout()
ax.set_ylabel('Hours Spent')
plt.show()

