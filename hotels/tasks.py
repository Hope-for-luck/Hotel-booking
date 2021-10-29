from django.core.mail import send_mail
from CRM_system._celery import app

@app.task
def notify_user_func(email):
    send_mail(
        'вы создали новый запрос',
        'Спасибо за испоьзование нашего сайта',
        'test@gmail.com',
        [email, ]
    )
    return 'Success'
