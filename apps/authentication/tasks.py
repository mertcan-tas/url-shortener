from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from decouple import config

DEFAULT_FROM_EMAIL = config("EMAIL_HOST_USER", default="noreply@app.com", cast=str)

@shared_task
def send_password_reset_email(email, reset_url, full_name):    
    subject = 'Password Reset Request'
    context = {'email': email, 'reset_url': reset_url, 'full_name': full_name}
    
    text_content = f'Click the following link to reset your password: {reset_url}'
    html_content = render_to_string('password_reset.html', context)
    
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=DEFAULT_FROM_EMAIL,
        to=[email]
    )
    msg.attach_alternative(html_content, "text/html")
    return msg.send()




