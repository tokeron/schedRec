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
START_STOP_RECORDING = 'windows+alt+r'

# lesson_day is a integer from 1 to 7, lesson start is an integer
def add_new_lesson(zoom_link, lesson_time, password="None"):
    date_array = lesson_time.split(" ")
    if len(date_array) < 2:
        return "Please type the day and time separated with a space. For example: Monday 9:30-12:30"
    lesson_day, lesson_time = date_array[0], date_array[1]
    try:
        lesson_day_num = DAYS.index(lesson_day)
    except ValueError:
        return "Please type the day in english starting with a big letter"
    time_array = lesson_time.split("-")
    if len(time_array) < 2:
        return "Please type the time separated with a '-'. For example: 10:30-11:30 "
    lesson_start_time, lesson_end_time = time_array[0], time_array[1]
    start_array = lesson_start_time.split(":")
    if len(start_array) < 2:
        return "Please type the hour and minutes separated with a ':'. For example: 10:30 "
    start_hour, start_minute = int(start_array[0]), int(start_array[1])
    end_array = lesson_end_time.split(":")
    if len(end_array) < 2:
        return "Please type the hour and minutes separated with a ':'. For example: 10:30 "
    end_hour, end_minute = int(end_array[0]), int(end_array[1])
    if start_hour < 0 or start_hour > 23 or end_hour < 0 or end_hour > 23:
        return "Hour should be between 0 and 23"
    if start_minute < 0 or start_minute > 59 or end_minute < 0 or end_minute > 59:
        return "Minutes should be between 0 and 59"
    if (start_hour > end_hour) or \
            ((start_hour == end_hour) and start_minute > end_minute):
        return "The starting time should be before ending time"
    now = datetime.datetime.today()
    first_lesson = now.replace(day=lesson_day_num, hour=start_hour, minute=start_minute, second=0, microsecond=0)
    if first_lesson < now:
        first_lesson = first_lesson + datetime.timedelta(7)
    next_lesson = first_lesson
    while next_lesson < LAST_DAY_OF_SEMESTER:
        scheduler.add_job(start_recording, args=[zoom_link, password], next_run_time=next_lesson)
        next_lesson_ends = next_lesson.replace(hour=end_hour, minute=end_minute, second=0)
        scheduler.add_job(stop_recording, next_run_time=next_lesson_ends)
        next_lesson += datetime.timedelta(7)
    return "The lesson has been scheduled from "+lesson_start_time+" to "+lesson_end_time+\
           " for the rest of the semester"


def start_recording(zoom_link, password):
    webbrowser.open(zoom_link, new=1)
    time.sleep(5)
    if password != "None":
        keyboard.send(password)
    time.sleep(5)
    # subprocess.call(find_prog("ShareX"))  # ("C:\\Program Files\\ShareX\\ShareX.exe")
    print("Starting recording")
    keyboard.send('START_STOP_RECORDING')


def stop_recording():
    print("Recording done")
    keyboard.send('START_STOP_RECORDING')


scheduler.start()
print("Hello! Welcome to Sched Rec!")
print("This program will record your zoom meetings for you for the rest f the semester!")
print("Enter your course information in the following order:")
print("zoom link, day and time, zoom password (optional)")
print("For example: https://example.zoom.us/j/1234, 12:30-14:30")


while True:
    for line in fileinput.input():
        args = line.split(",")
        if len(args) < 2:
            print("Please Type the link and time seperated with a comma.")
            print("For example: https://example.zoom.us/j/1234, 12:30-14:30")
        else:
            zoom_link = args[0].strip()
            lesson_time = args[1].strip()
            password = "None"
            if len(args) > 2:
                password = args[2].strip()
            print(add_new_lesson(zoom_link, lesson_time, password))


print("Hello! Welcome to Sched Rec!")
print("This program will record your zoom meetings for you!")
print("Enter your course information in the following order:")
print("zoom link, time, zoom password (optional)")
print("For example: https://example.zoom.us/j/1234, 12:30-14:30")
scheduler.start()


while True:
    for line in fileinput.input():
        args = line.split(",")
        if len(args) < 2:
            print("Please Type the link and time separated with a comma.")
            print("For example: https://example.zoom.us/j/1234, 12:30-14:30")
        else:
            zoom_link = args[0].strip()
            lesson_time = args[1].strip()
            password = "None"
            if len(args) > 2:
                password = args[2].strip()
            print(add_new_lesson(zoom_link, lesson_time, password))
