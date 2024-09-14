from tkinter import *
from tkinter import messagebox
from intro import show_intro_window
from constants import *


# STATE VARIABLES
timer = ""
paused_time = 0
session_count = 0
saved_session = 0
pomo_start = False
is_running = False
is_long_break = False
is_short_break = False
is_work_session = False
number_sessions = 8


# ---------------------------- APP SESSIONS ------------------------------- #
def start_resume_work():
    """Starts or resumes the work session timer."""
    global is_work_session, is_short_break, is_long_break, pomo_start
    is_work_session = True
    is_short_break = False
    is_long_break = False
    pomo_start = True

    if saved_session:
        reset_toggle()
        root.after_cancel(timer)
        count_down(saved_session)
    else:
        reset_toggle()
        work_sec = WORK_MIN * 60
        count_down(work_sec)

    update_buttons()
    set_background_color(WINDOW_BG)
    session_label.config(text="Work", fg=SESSION_LABEL)


def start_short_break():
    """Starts a short break session."""
    global is_short_break, is_long_break, is_work_session, saved_session
    if pomo_start:
        if is_work_session:
            saved_session = save_session_time()
            is_work_session = False
        is_short_break = True
        is_long_break = False
        reset_toggle()
        root.after_cancel(timer)
        short_break_sec = SHORT_BREAK_MIN * 60
        count_down(short_break_sec)
        set_background_color(SHORT_BREAK_BG)
        session_label.config(text="Short Break", fg=SESSION_LABEL)
        update_buttons()


def start_long_break():
    """Starts a long break session."""
    global is_long_break, is_short_break, is_work_session, saved_session
    if pomo_start:
        if is_work_session:
            saved_session = save_session_time()
            is_work_session = False
        is_long_break = True
        is_short_break = False
        reset_toggle()
        root.after_cancel(timer)
        long_break_sec = LONG_BREAK_MIN * 60
        count_down(long_break_sec)
        set_background_color(LONG_BREAK_BG)
        session_label.config(text="Long Break", fg=SESSION_LABEL)
        update_buttons()


def save_session_time():
    """Saves the remaining time of the current session."""
    timer_value = canvas.itemcget(timer_text, "text")
    minutes, seconds = map(int, timer_value.split(":"))
    saved_time = minutes * 60 + seconds - 1
    return saved_time if saved_time > 0 else 0


def session_complete():
    """Handle the completion of a work session."""
    global session_count
    session_count += 1
    update_session_counter()

    if session_count % number_sessions == 0:
        end_day()
    elif session_count % 3 == 0:
        start_long_break()
    else:
        start_short_break()


def end_day():
    """Ends the Pomodoro sessions after 8 work sessions."""
    global saved_session
    set_background_color(WINDOW_BG)
    session_label.config(text="Sessions Complete", font=("Verdana", 21, "bold"))
    start_button.config(state="normal", text="Continue Work", width=9)
    short_break_button.config(state="disabled")
    long_break_button.config(state="disabled")
    play_pause_button.config(state="disabled")
    reset_button.config(state="normal", text="Reset")
    root.update()
    messagebox.showinfo(
        f"{session_count} Sessions Complete",
        f"Great work! \n\nYou’ve completed today’s sessions. Time to relax!",
    )
    play_pause_button.config(state="normal", text="▶")
    root.after_cancel(timer)
    saved_session = 0


def update_session_counter():
    """Update the session counter label."""
    global session_count
    session_counter_label.config(text=f"SESSIONS COMPLETED: {session_count}")


def update_buttons():
    """Update the state of the buttons based on the current session."""
    if is_work_session:
        start_button.config(state="disabled", text="Resume Work")
        short_break_button.config(state="normal")
        long_break_button.config(state="normal")
    elif is_short_break:
        short_break_button.config(state="disabled")
        long_break_button.config(state="normal")
        start_button.config(state="normal", text="Resume Work")
    elif is_long_break:
        long_break_button.config(state="disabled")
        short_break_button.config(state="normal")
        start_button.config(state="normal", text="Resume Work")


def set_background_color(color):
    root.config(bg=color)
    task_label.config(bg=color)
    add_button.config(highlightbackground=color)
    start_button.config(highlightbackground=color)
    short_break_button.config(highlightbackground=color)
    long_break_button.config(highlightbackground=color)
    play_pause_button.config(highlightbackground=color)
    reset_button.config(highlightbackground=color)
    session_label.config(bg=color)
    session_counter_label.config(bg=color)
    canvas.config(bg=color)


# ---------------------------- TIMER CONTROLS ------------------------------- #
def count_down(duration):
    """Countdown mechanism for the timer."""
    global timer, is_running
    is_running = True
    count_min = duration // 60
    count_sec = duration % 60

    if count_min < 10:
        count_min = f"0{count_min}"
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if duration > 0:
        timer = root.after(1000, count_down, duration - 1)
    else:
        if is_work_session:
            session_complete()
        elif is_short_break or is_long_break:
            start_resume_work()


def toggle_timer():
    """Toggles between play and pause states for the timer."""
    global is_running, paused_time
    if is_running:
        # Pause the timer
        timer_value = canvas.itemcget(timer_text, "text")
        minutes, seconds = map(int, timer_value.split(":"))
        paused_time = minutes * 60 + seconds
        root.after_cancel(timer)
        canvas.itemconfig(timer_text, text=f"{minutes:02d}:{seconds:02d}")
        is_running = False
    else:
        # Resume the timer
        if paused_time > 0:
            count_down(paused_time - 1)
    play_pause_button.config(text="⏸" if is_running else "▶")


def reset_toggle():
    """Resets the play/pause button to the play state."""
    global is_running
    is_running = True
    play_pause_button.config(text="⏸")


def reset_timer():
    """Resets the entire timer and session states."""
    global paused_time, session_count, saved_session, is_work_session, is_running, is_short_break, is_long_break, pomo_start
    pomo_start = False
    is_work_session = False
    is_short_break = False
    is_long_break = False
    is_running = False
    session_count = 0
    saved_session = 0
    paused_time = 0
    canvas.itemconfig(timer_text, text="00:00")
    session_label.config(text="Click 'Start' to begin", font=("Verdana", 23, "bold"))
    play_pause_button.config(text="▶")
    start_button.config(state="normal", text="Start Work")
    short_break_button.config(state="normal")
    long_break_button.config(state="normal")
    set_background_color(WINDOW_BG)
    task_entry.delete("1.0", "end")
    for widget in task_frame.winfo_children():
        widget.destroy()
    if timer:
        root.after_cancel(timer)


# ---------------------------- TASK MANAGEMENT ------------------------------- #
def add_task():
    """Adds a new task to the task list."""
    task = task_entry.get("1.0", "end-1c")
    if task:
        var = IntVar()
        checkbox = Checkbutton(
            task_frame,
            text=task.strip(),
            variable=var,
            font=("Verdana", 14),
            anchor="w",
            fg=SESSION_LABEL,
            bg=FRAME_COLOR,
            command=lambda: complete_task(checkbox),
        )
        checkbox.var = var
        checkbox.pack(fill="x", padx=5, pady=2)
        task_entry.delete("1.0", END)

        # Increase frame height if tasks exceed the current height
        current_height = task_frame.winfo_height()
        if len(task_frame.winfo_children()) * 30 > current_height:
            new_height = current_height + 10
            task_frame.config(height=new_height)


def complete_task(checkbox):
    """Mark a task as complete or incomplete."""
    if checkbox.var.get():
        checkbox.config(fg="grey", font=("Verdana", 14, "overstrike"))
    else:
        checkbox.config(fg=SESSION_LABEL, font=("Verdana", 14))


# ---------------------------- UI SETUP ------------------------------- #
root = Tk()
root.title("Deep Focus ⏰")
root.config(padx=50, pady=30, bg=WINDOW_BG)
root.geometry("700x870")
root.resizable(False, False)
root.withdraw()

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)

canvas = Canvas(width=200, height=295, bg=WINDOW_BG, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(125, 200, image=tomato_img)
timer_text = canvas.create_text(
    125, 200, text="00:00", fill="white", font=("Verdana", 28, "bold")
)
canvas.grid(column=2, row=2, rowspan=1, sticky="ew")

session_label = Label(
    text="Click 'Start' to begin",
    font=("Verdana", 23, "bold"),
    bg=WINDOW_BG,
    fg=SESSION_LABEL,
)
session_label.grid(row=2, column=1, columnspan=3, pady=(0, 180), sticky="ew")
session_counter_label = Label(
    root,
    text=f"SESSIONS COMPLETED: {session_count}",
    font=("Verdana", 12, "bold"),
    fg=SESSION_LABEL,
    bg=WINDOW_BG,
)
session_counter_label.grid(column=1, columnspan=3, row=0, padx=(350, 0), pady=(0, 35))

start_button = Button(
    text="Start Work",
    font=("Verdana", 12),
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    highlightbackground=WINDOW_BG,
    command=start_resume_work,
)
start_button.grid(column=1, row=1, pady=(30, 0))

short_break_button = Button(
    text="Short Break",
    font=("Verdana", 12),
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    highlightbackground=WINDOW_BG,
    command=start_short_break,
)
short_break_button.grid(column=2, row=1, pady=(30, 0))

long_break_button = Button(
    text="Long Break",
    font=("Verdana", 12),
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    highlightbackground=WINDOW_BG,
    command=start_long_break,
)
long_break_button.grid(column=3, row=1, pady=(30, 0))

play_pause_button = Button(
    text="▶",
    width=1,
    height=2,
    borderwidth=0,
    highlightbackground=WINDOW_BG,
    command=toggle_timer,
)
play_pause_button.grid(column=2, row=3, pady=(0, 10))

reset_button = Button(
    text="Reset",
    font=("Verdana", 12),
    height=1,
    highlightbackground=WINDOW_BG,
    command=reset_timer,
)
reset_button.grid(column=1, row=0, padx=(0, 30), pady=(0, 35))


def on_focus_in(event):
    """Highlights the task entry box on focus."""
    task_entry.config(
        highlightbackground=FRAME_COLOR,
        highlightcolor=BORDER_COLOR,
        highlightthickness=3,
    )


task_label = Label(
    root,
    text="Add a new task:",
    font=("Verdana", 15, "bold"),
    fg=SESSION_LABEL,
    bg=WINDOW_BG,
)
task_label.grid(column=2, row=6, pady=(40, 0))

task_entry = Text(
    root,
    height=1,
    width=40,
    font=("Verdana", 14),
    highlightbackground="#d9d9d9",
    bg=FRAME_COLOR,
    fg=SESSION_LABEL,
)
task_entry.grid(row=7, column=1, columnspan=3, padx=(0, 0), pady=0)
task_entry.bind("<FocusIn>", on_focus_in)

add_button = Button(
    text="add",
    font=("Verdana", 12),
    height=2,
    width=2,
    borderwidth=1,
    highlightbackground=WINDOW_BG,
    command=add_task,
)
add_button.grid(row=7, column=3, padx=(20, 0))

task_frame = Frame(root, height=200, width=500, bg=FRAME_COLOR)
task_frame.grid(row=8, column=1, columnspan=3, padx=(0, 0), pady=(5, 15))
task_frame.grid_propagate(False)
task_frame.pack_propagate(False)


if __name__ == "__main__":
    show_intro_window(root)
    root.mainloop()
