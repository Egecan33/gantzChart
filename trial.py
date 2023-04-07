import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
from collections import defaultdict
import mplcursors


def create_gantt_chart(file_path):
    # Read the machine names, job names, and time intervals from the CSV file
    machines = []
    jobs = defaultdict(list)
    time_intervals = defaultdict(list)
    with open(file_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            machine, job, start_time, end_time = row
            if machine not in machines:
                machines.append(machine)
            jobs[machine].append(job)
            time_intervals[machine].append((start_time, end_time))

    # Create a larger figure and adjust the size of the chart area
    fig, ax = plt.subplots(figsize=(13, 8))
    plt.subplots_adjust(left=0.25, right=0.95, top=0.95, bottom=0.2)

    # Set the format for the date axis
    date_format = mdates.DateFormatter("%Y-%m-%d %H:%M:%S")
    ax.xaxis.set_major_formatter(date_format)

    # Set the axis labels
    ax.set_xlabel("Date & Time")
    ax.set_ylabel("Machines")

    # Compute the minimum and maximum time values from the input time intervals
    all_start_times = [
        start_time
        for machine_intervals in time_intervals.values()
        for start_time, _ in machine_intervals
    ]
    all_end_times = [
        end_time
        for machine_intervals in time_intervals.values()
        for _, end_time in machine_intervals
    ]
    min_time = min(all_start_times)
    max_time = max(all_end_times)

    # Assign a color to each unique job
    all_jobs = set(job for job_list in jobs.values() for job in job_list)
    colors = plt.cm.get_cmap("tab20", len(all_jobs))
    job_colors = {job: colors(i) for i, job in enumerate(all_jobs)}

    for idx, machine in enumerate(machines):
        for job, (start_time, end_time) in zip(jobs[machine], time_intervals[machine]):
            start_num = mdates.datestr2num(start_time)
            end_num = mdates.datestr2num(end_time)
            ax.barh(
                machine,
                end_num - start_num,
                left=start_num,
                height=0.95,
                align="center",
                color=job_colors[job],
                label=job,
                alpha=0.81,  # Set the transparency of the bars
            )

    # Set the x-axis limits to the minimum and maximum time values, with a buffer of 5% on either side
    time_range = mdates.datestr2num(max_time) - mdates.datestr2num(min_time)
    buffer = 0.05 * time_range
    ax.set_xlim(mdates.datestr2num(min_time), mdates.datestr2num(max_time) + buffer)

    # Set the x-axis label to include the minimum time value
    ax.set_xlabel(f"Start Time: {min_time}   Date & Time")

    # Create a legend for the job colors outside the chart area
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    legend = ax.legend(by_label.values(), by_label.keys(), draggable=True)

    # Set the layout and show the chart
    plt.grid(axis="x")
    plt.xticks(rotation=45)

    # Add interactivity with mplcursors
    cursor = mplcursors.cursor(ax, hover=False)
    cursor.connect(
        "add",
        lambda sel: sel.annotation.set_text(
            f"{jobs[sel.target.get_y()][0]}: {mdates.num2date(sel.target.get_x()):%Y-%m-%d %H:%M:%S}"
        ),
    )

    plt.show()


file_path = "jobs.csv"
create_gantt_chart(file_path)
