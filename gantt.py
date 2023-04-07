import os

os.environ["TK_SILENCE_DEPRECATION"] = "1"

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def create_gantt_chart(jobs, time_intervals):
    # Clear the existing chart
    ax.clear()

    # Set the format for the date axis
    date_format = mdates.DateFormatter("%Y-%m-%d %H:%M")
    ax.xaxis.set_major_formatter(date_format)

    # Set the axis labels
    ax.set_xlabel("Date & Time")
    ax.set_ylabel("Jobs")

    if jobs and time_intervals:
        for idx, job in enumerate(jobs):
            start_date, end_date = time_intervals[idx]
            ax.barh(
                job, end_date - start_date, left=start_date, height=0.3, align="center"
            )

    # Set the layout and redraw the chart
    plt.tight_layout()
    plt.grid(axis="x")
    plt.xticks(rotation=45)
    canvas.draw_idle()


def add_job():
    job = job_entry.get()
    start_time = start_entry.get()
    end_time = end_entry.get()

    if job and start_time and end_time:
        jobs.append(job)
        time_intervals.append(
            (mdates.datestr2num(start_time), mdates.datestr2num(end_time))
        )
        create_gantt_chart(jobs, time_intervals)

        # Clear the input fields
        job_entry.delete(0, tk.END)
        start_entry.delete(0, tk.END)
        end_entry.delete(0, tk.END)


# Create the main window
root = tk.Tk()
root.title("Gantt Chart Generator")
root.geometry("800x600")

# Configure the main window grid
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Create a frame for input fields and buttons
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create input fields and labels
job_label = ttk.Label(frame, text="Job:")
job_entry = ttk.Entry(frame, width=20)
start_label = ttk.Label(frame, text="Start Time (YYYY-MM-DD HH:MM):")
start_entry = ttk.Entry(frame, width=20)
end_label = ttk.Label(frame, text="End Time (YYYY-MM-DD HH:MM):")
end_entry = ttk.Entry(frame, width=20)

# Create the "Add Job" button
add_button = ttk.Button(frame, text="Add Job", command=add_job)

# Grid input fields and labels
job_label.grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
job_entry.grid(row=0, column=1, sticky=tk.W)
start_label.grid(row=1, column=0, padx=(0, 10), sticky=tk.W)
start_entry.grid(row=1, column=1, sticky=tk.W)
end_label.grid(row=2, column=0, padx=(0, 10), sticky=tk.W)
end_entry.grid(row=2, column=1, sticky=tk.W)
add_button.grid(row=3, column=1, pady=(10, 0), sticky=tk.W)

# Create a frame for the Gantt chart
chart_frame = ttk.Frame(root, padding="10")
chart_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create the Gantt chart
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.draw_idle()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Initialize jobs and time_intervals lists
jobs = []
time_intervals = []

# Call create_gantt_chart to initialize the empty chart
create_gantt_chart(jobs, time_intervals)

# Run the main event loop
root.mainloop()
