from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from django.shortcuts import render
from django.http import HttpResponse
from templated_mail.mail import BaseEmailMessage
# Create your views here.


def say_hello(request):
    try:
        message = BaseEmailMessage(
            template_name='emails/hey.html',
            context={'name': 'Nasim'}
        )
        message.send(['john@nasimbuy.com'])
        # message = EmailMessage('my subject', 'my message', 'info@nasimbuy.com', ['bob@nasimbuy.com'])
        # message.attach_file('play/static/images/men.jpg')
        
        # message.send() 
        # mail_admins('subject', 'message', html_message='my message')
        # send_mail('subject', 'message', 'info@nasimbuy.com', ['bob@nasimbuy.com'])
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'nasim'})
 