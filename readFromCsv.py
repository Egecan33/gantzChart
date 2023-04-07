import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def create_gantt_chart(jobs, time_intervals):
    fig, ax = plt.subplots()

    # Set the format for the date axis
    date_format = mdates.DateFormatter("%Y-%m-%d %H:%M")
    ax.xaxis.set_major_formatter(date_format)

    # Set the axis labels
    ax.set_xlabel("Date & Time")
    ax.set_ylabel("Jobs")

    for idx, job in enumerate(jobs):
        start_date, end_date = time_intervals[idx]
        ax.barh(job, end_date - start_date, left=start_date, height=0.3, align="center")

    # Set the layout and show the chart
    plt.tight_layout()
    plt.grid(axis="x")
    plt.xticks(rotation=45)
    plt.show()


# Example usage:
jobs = ["Job 1", "Job 2", "Job 3"]
time_intervals = [
    ("2023-04-10 08:00", "2023-04-15 17:00"),
    ("2023-04-12 10:30", "2023-04-18 15:00"),
    ("2023-04-16 09:00", "2023-04-22 18:00"),
]

# Convert date strings to datetime objects
time_intervals = [
    (mdates.datestr2num(start), mdates.datestr2num(end))
    for start, end in time_intervals
]

create_gantt_chart(jobs, time_intervals)
