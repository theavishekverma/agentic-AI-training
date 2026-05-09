from datetime import datetime, date, time, timedelta

# Current date and time
now = datetime.now()
print("Current datetime:", now)

# Current date only
today = date.today()
print("Today's date:", today)

# Formatting datetime
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print("Formatted datetime:", formatted)

# Creating a specific time
t = time(14, 30, 0)  # 2:30 PM
print("Specific time:", t)

# Adding 5 days to current date
future_date = today + timedelta(days=5)
print("Date after 5 days:", future_date)

# Subtracting 2 hours from current datetime
past_time = now - timedelta(hours=2)
print("2 hours ago:", past_time)
print("#" * 60)

from datetime import datetime

# Define two times
time1 = datetime.strptime("2026-04-25 10:30:00", "%Y-%m-%d %H:%M:%S")
time2 = datetime.strptime("2026-04-25 13:45:00", "%Y-%m-%d %H:%M:%S")

# Calculate difference
difference = time2 - time1

print("Difference:", difference)
print("Total seconds:", difference.total_seconds())
print("Hours:", difference.total_seconds() / 3600)
print("#" * 60)

