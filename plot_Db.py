import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

conn = sqlite3.connect('geeks2.db')
c = conn.cursor()

end_time = datetime.now()
start_time = end_time - timedelta(hours=12)

query = """
    SELECT DangerType, DangerDate, AVG(DangerAmount) AS AvgDangerAmount
    FROM Site
    WHERE DangerDate BETWEEN ? AND ?
    GROUP BY DangerType, strftime('%Y-%m-%d %H:%M', DangerDate)
"""

c.execute(query, (start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S')))
results = c.fetchall()

danger_types = []
time_slots = []
avg_danger_amounts = []

for row in results:
    danger_type, time_slot, avg_danger_amount = row
    danger_types.append(danger_type)
    time_slots.append(datetime.strptime(time_slot, '%Y-%m-%d %H:%M'))
    avg_danger_amounts.append(avg_danger_amount)

plt.figure(figsize=(12, 6))
for danger_type in set(danger_types):
    x_values = [time_slot for time_slot, danger, avg in zip(time_slots, danger_types, avg_danger_amounts)
                if danger == danger_type]
    y_values = [avg for danger, avg in zip(danger_types, avg_danger_amounts) if danger == danger_type]
    plt.plot(x_values, y_values, label=danger_type)

plt.xlabel('Time')
plt.ylabel('Average Danger Amount')
plt.title('Average Danger Amount for Each Danger Type')

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=20))

plt.xticks(rotation=45)
plt.legend()

# Set the x-axis limits
plt.xlim(start_time, end_time)

plt.tight_layout()

# Save the plot as a PNG file
plt.savefig('graph12hours.png')
