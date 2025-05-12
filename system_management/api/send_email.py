from django.core.mail import EmailMessage
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from system_management.models import User
from django.template.loader import get_template

def email_send(context, email, html_tpl_path):
    html_tpl_path = html_tpl_path
    recipient = email
    subject = 'Deep OCR Team NoReply'
    sender = settings.DEFAULT_FROM_EMAIL
    email_html_template = get_template(html_tpl_path).render(context)
    email_msg = EmailMessage(
        subject, 
        email_html_template, 
        sender, 
        [recipient],
        reply_to=[sender]
        )
    email_msg.content_subtype = "html"
    email_msg.send(fail_silently=False)



   


