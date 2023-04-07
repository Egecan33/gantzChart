import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv


def create_gantt_chart(file_path):
    # Read the job names and time intervals from the CSV file
    jobs = []
    time_intervals = []
    with open(file_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            jobs.append(row[0])
            time_intervals.append((row[1], row[2]))

    fig, ax = plt.subplots()

    # Set the format for the date axis
    date_format = mdates.DateFormatter("%Y-%m-%d %H:%M:%S")
    ax.xaxis.set_major_formatter(date_format)

    # Set the axis labels
    ax.set_xlabel("Date & Time")
    ax.set_ylabel("Jobs")

    # Compute the minimum and maximum time values from the input time intervals
    start_times, end_times = zip(*time_intervals)
    min_time = min(start_times)
    max_time = max(end_times)

    for idx, job in enumerate(jobs):
        start_time, end_time = time_intervals[idx]
        start_num = mdates.datestr2num(start_time)
        end_num = mdates.datestr2num(end_time)
        ax.barh(job, end_num - start_num, left=start_num, height=0.3, align="center")

    # Set the x-axis limits to the minimum and maximum time values, with a buffer of 5% on either side
    time_range = mdates.datestr2num(max_time) - mdates.datestr2num(min_time)
    buffer = 0.05 * time_range
    ax.set_xlim(
        mdates.datestr2num(min_time) - buffer, mdates.datestr2num(max_time) + buffer
    )

    # Set the layout and show the chart
    plt.tight_layout()
    plt.grid(axis="x")
    plt.xticks(rotation=45)
    plt.show()


# Example usage:
file_path = "jobs.csv"
create_gantt_chart(file_path)
