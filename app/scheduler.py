from apscheduler.schedulers.background import BackgroundScheduler
from ocso import main as run_ocso_scraper

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(run_ocso_scraper, "interval", minutes=1)
    scheduler.start()
