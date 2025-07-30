from celery.schedules import crontab
from flask import current_app as app
from backend.celery.tasks import email_reminder, expire_stale_reservations, send_daily_reminders, send_monthly_reports
from backend.models import User
from backend.utils.email_templates import render_daily_reminder_html

celery_app = app.extensions['celery']

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Expire stale reservations every 5 minutes
    sender.add_periodic_task(
        crontab(minute='*/5'),
        expire_stale_reservations.s(),
        name='expire stale reservations',
    )

    #  Daily reminders at 6:30 PM IST
    sender.add_periodic_task(
        crontab(hour=18, minute=30),
        send_daily_reminders.s(),
        name='daily reminders (evening IST)',
    )

    # Monthly reports on the 1st of every month at 9:00 AM IST
    sender.add_periodic_task(
        crontab(minute=0, hour=9, day_of_month=1),
        send_monthly_reports.s(),
        name='monthly activity reports (1st day 9AM IST)',
    )



