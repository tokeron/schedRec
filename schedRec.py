# importing the required packages
import webbrowser
import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
import fileinput
import keyboard


LAST_DAY_OF_SEMESTER = datetime.datetime.strptime('Jan 25 2021 11:59PM', '%b %d %Y %I:%M%p')
scheduler = BackgroundScheduler()
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
TIME_BEFORE_LESSON_STARTS = 0
TIME_AFTER_LESSON_IS_OVER = 0


# lesson_day is a integer from 1 to 7, lesson start is an integer
def add_new_lesson(zoom_link, lesson_time, password="None"):
    lesson_start_time, lesson_end_time = lesson_time.split("-")
    lesson_start_hour, lesson_start_minute = lesson_start_time.split(":")
    lesson_end_hour, lesson_end_minute = lesson_end_time.split(":")
    start_hour = int(lesson_start_hour)
    start_minute = int(lesson_start_minute)
    end_hour = int(lesson_end_hour)
    end_minute = int(lesson_end_minute)
    if start_hour < 0 or start_hour > 23 or end_hour < 0 or end_hour > 23:
        return "Hour should be between 0 and 23"
    if start_minute < 0 or start_minute > 59 or end_minute < 0 or end_minute > 59:
        return "Minutes should be between 0 and 59"
    if (start_hour > end_hour) or \
            ((start_hour == end_hour) and start_minute > end_minute):
        return "The starting time should be before ending time"
    now = datetime.datetime.today()
    first_lesson = now.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
    if first_lesson < now:
        first_lesson = first_lesson + datetime.timedelta(7)
    next_lesson = first_lesson
    scheduler.add_job(start_recording, args=[zoom_link, password], next_run_time=next_lesson)
    next_lesson_ends = next_lesson.replace(hour=end_hour, minute=end_minute, second=0)
    scheduler.add_job(stop_recording, next_run_time=next_lesson_ends)
    return "The lesson has been scheduled from "+lesson_start_time+" to "+lesson_end_time


def start_recording(zoom_link, password):
    webbrowser.open(zoom_link, new=1)
    time.sleep(5)
    if password != "None":
        keyboard.send(password)
    time.sleep(5)
    # subprocess.call(find_prog("ShareX"))  # ("C:\\Program Files\\ShareX\\ShareX.exe")
    print("Starting recording")
    keyboard.send('windows+alt+r')


def stop_recording():
    print("Recording done")
    keyboard.send('windows+alt+r')


scheduler.start()
print("Hello! Welcome to Sched Rec!")
print("This program will record your zoom meetings for you!")
print("In order to schedule a meeting insert the details of your lessons today.")
print("Enter your course information in the following order:")
print("zoom link, time, zoom password(optional)")
print("For example: https://example.zoom.us/j/1234, 12:30-14:30")
print("With password it should look like this: https://example.zoom.us/j/1234, 12:30-14:30, 1234")


while True:
    for line in fileinput.input():
        args = line.split(",")
        zoom_link = args[0].strip()
        time = args[1].strip()
        password = "None"
        if len(args) > 2:
            password = args[2].strip()
        print(add_new_lesson(zoom_link, time, password))
