import schedule
import time
import threading

def job():
    print("I'm working...")


def thread_function(name):
    schedule.every().day.at("19:05").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    x = threading.Thread(target=thread_function, args=(1,))
    print("hello world!")
    x.join()