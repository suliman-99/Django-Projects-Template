from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, register_job


def start():
    scheduler = BackgroundScheduler()

    # @register_job(scheduler, "interval", seconds=5)
    # def test_job():
    #     print('here is called the test job.')

    register_events(scheduler)
    scheduler.start()
