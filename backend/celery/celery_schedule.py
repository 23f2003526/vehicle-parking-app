from celery.schedules import crontab
from flask import current_app as app
from backend.celery.tasks import email_reminder, expire_stale_reservations
from backend.models import User
from backend.utils.email_templates import render_daily_reminder_html

celery_app = app.extensions['celery']

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # from user, get the emails, and send them (in batches if possible). create a jinja template. send that to people. have to create 
    # Daily Reminders (G-Chat/SMS/Email) for users.
    # Monthly Activity Reports (HTML/PDF mails).


    # every 10 seconds
    # sender.add_periodic_task(10.0, email_reminder.s('students@gmail', 'subject', '<h1>content - fix this</h1>'))
    
    # daily message @6 30pm
    # sender.add_periodic_task(crontab(hour=18, minute=30), email_reminder.s('students@gmail', 'subject', '<h1>put something relevant here</h1>'), name='daily reminder')
    users = User.query.all()
    for user in users:
        subject = "Your Daily Parking Reminder"
        content = render_daily_reminder_html(user)
        sender.add_periodic_task(
            crontab(hour=8, minute=0),  # every day at 8:00 AM
            email_reminder.s(user.email, subject, content),
            name=f'daily_reminder_{user.id}'
        )

    # monthly messages
    sender.add_periodic_task(crontab(minute=30, hour=18, day_of_week='*', day_of_month=1, month_of_year='*', ), email_reminder.s('students@gmail.com', 'this is subject', '<h1>put something relevant here</h1>'), name='monthly reminder')

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Every 5 minutes
    sender.add_periodic_task(crontab(minute='*/5'), expire_stale_reservations.s(), name='expire stale reservations')




