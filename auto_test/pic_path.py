import os
import time


def get_pic_path():
    year = time.strftime("%Y")
    month = time.strftime("%m")
    day = time.strftime("%d")
    hour = time.strftime("%H")
    current_time = time.strftime("%H%M%S")
    media_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "media")

    year_path = os.path.join(media_path, year)
    month_path = os.path.join(year_path, month)
    day_path = os.path.join(month_path, day)
    hour_path = os.path.join(day_path, hour)

    print(year_path)
    if not os.path.exists(year_path):
        os.mkdir(year_path)

    if not os.path.exists(month_path):
        os.mkdir(month_path)

    if not os.path.exists(day_path):
        os.mkdir(day_path)

    if not os.path.exists(hour_path):
        os.mkdir(hour_path)

    file_path = os.path.join(hour_path, time.strftime("%M%S") + ".jpg")
    print("file_path: %s" % file_path)
    relative_path = file_path.split("media\\")[1]
    return file_path, relative_path


if __name__ == '__main__':
    print(get_pic_path())
