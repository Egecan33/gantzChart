import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv


def create_gantt_chart(jobs, time_intervals):
    fig, ax = plt.subplots()

    # Convert date strings to datetime objects
    time_intervals = [
        (mdates.datestr2num(start), mdates.datestr2num(end))
        for start, end in time_intervals
    ]

    # Find the earliest start time and latest end time
    earliest_start_time = min([start for start, end in time_intervals])
    latest_end_time = max([end for start, end in time_intervals])

    # Set the format for the date axis
    date_format = mdates.DateFormatter("%Y-%m-%d %H:%M:%S")
    ax.xaxis.set_major_formatter(date_format)

    # Set the axis labels and limits
    ax.set_xlabel("Date & Time")
    ax.set_ylabel("Jobs")
    ax.set_xlim(earliest_start_time, latest_end_time)

    # Add a vertical line at the earliest start time
    ax.axvline(x=earliest_start_time, color="black", linestyle="--", alpha=0.5)

    unique_jobs = sorted(list(set(jobs)))
    y_pos_mapping = {job: idx for idx, job in enumerate(unique_jobs)}

    for idx, job in enumerate(jobs):
        start_date, end_date = time_intervals[idx]
        ax.barh(
            y_pos_mapping[job] + idx * 0.1,
            end_date - start_date,
            left=start_date,
            height=0.1,
            align="center",
        )

    ax.set_yticks(range(len(unique_jobs)))
    ax.set_yticklabels(unique_jobs)

    # Set the layout and show the chart
    plt.tight_layout()
    plt.grid(axis="x")
    plt.xticks(rotation=45)
    plt.show()


# Read jobs and time intervals from the CSV file
jobs = []
time_intervals = []

with open("jobs.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        jobs.append(row[0])
        time_intervals.append((row[1], row[2]))

create_gantt_chart(jobs, time_intervals)
