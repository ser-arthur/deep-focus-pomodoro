from tkinter import font, Tk, Toplevel, Label, Button as TkButton
from tkmacosx import Button as MacButton
from constants import *
import platform


def show_intro_window(root):
    """Displays the introductory window with the Pomodoro Technique explanation."""
    intro_window = Toplevel(root)
    intro_window.title("Welcome to Deep Focus!")
    intro_window.config(padx=50, pady=50, bg=WINDOW_BG)

    # Labels
    default_font = get_default_font()
    app_title_label = Label(
        intro_window,
        text="DeepFocus with Pomodoro⏰",
        font=(default_font, 24, "bold"),
        bg=WINDOW_BG,
        fg=LABEL_COLOR,
    )
    app_title_label.pack(pady=(0, 25))

    pomodoro_label = Label(
        intro_window,
        text="What is the Pomodoro Technique?",
        font=(default_font, 17, "bold"),
        bg=WINDOW_BG,
        fg=LABEL_COLOR,
    )
    pomodoro_label.pack(padx=10, pady=(15, 5))

    pomodoro_text = Label(
        intro_window,
        font=(default_font, 17),
        bg=WINDOW_BG,
        fg="#5A5753",
        wraplength=460,
        justify="left",
        text="The Pomodoro Technique, created by Francesco Cirillo, is a productivity method "
        "designed for work and study. It involves using a timer to break work into intervals, "
        "traditionally 25 minutes long, with short and long breaks in between. Each interval "
        "is called a 'pomodoro,' named after the Italian word for 'tomato,' inspired by the "
        "tomato-shaped kitchen timer that Cirillo used as a university student. This technique "
        "helps you stay focused and manage your time efficiently, improving overall "
        "productivity.",
    )
    pomodoro_text.pack(padx=10, pady=(0, 20))

    how_to_use_label = Label(
        intro_window,
        text="How to Use Deep Focus",
        font=(default_font, 17, "bold"),
        bg=WINDOW_BG,
        fg=LABEL_COLOR,
    )
    how_to_use_label.pack(padx=10, pady=(10, 5))

    how_to_use_text = Label(
        intro_window,
        font=(default_font, 17),
        bg=WINDOW_BG,
        fg="#5A5753",
        wraplength=460,
        justify="left",
        text="Deep Focus automates the Pomodoro sequence for you, with a total of 8 work sessions "
        "(intervals) each day. Short breaks follow each session, and a longer break comes "
        "after every 3 sessions. You can also control your own workflow by using the "
        "available buttons to pause the timer, take breaks, or add tasks to track your "
        "progress.",
    )
    how_to_use_text.pack(padx=10, pady=(0, 20))

    def create_get_started_btn():
        """Customizes the Get-Started button based on the OS."""
        current_os = platform.system()
        if current_os == "Darwin":  # macOS
            get_started_btn = MacButton(
                intro_window,
                text="Get Started",
                fg=WINDOW_BG,
                bg="#15171a",
                borderless=1,
                font=(default_font, 18),
                activebackground="#15171a",
                activeforeground=WINDOW_BG,
                command=lambda: (intro_window.destroy(), root.deiconify()),
            )
            get_started_btn.pack(padx=20, pady=25, ipadx=10, ipady=15)
        else:  # Windows or other OS
            get_started_btn = TkButton(
                intro_window,
                text="Get Started",
                fg=WINDOW_BG,
                bg="#15171a",
                borderwidth=0,
                activebackground="#15171a",
                activeforeground=WINDOW_BG,
                highlightthickness=0,
                font=(default_font, 18),
                highlightbackground=WINDOW_BG,
                command=lambda: (intro_window.destroy(), root.deiconify()),
            )
            get_started_btn.pack(padx=20, pady=25, ipadx=10, ipady=10)

    create_get_started_btn()

    intro_window.mainloop()


def get_default_font():
    """Returns 'Gill Sans' if available, otherwise 'Georgia'."""
    temp_root = Tk()
    temp_root.withdraw()
    available_fonts = font.families()
    temp_root.destroy()
    return "Gill Sans" if "Gill Sans" in available_fonts else "Georgia"
