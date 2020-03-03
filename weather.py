import datetime

def getTime():
    ISOTIMEFORMAT = '%H:%M'
    time = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    return time

def start():
    time = getTime()
    print(time)

start()