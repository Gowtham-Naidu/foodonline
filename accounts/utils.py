from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
#helper functions
def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        
#helper function to send email    
def send_verification_email(request,user,mail_subject,email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    #print('inside the send verification function')
    current_site = get_current_site(request)
    #print(current_site)
    #mail_subject = 'Please activate your account'
    message = render_to_string(email_template,{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),
        
    })
    to_email = user.email
    #print(to_email)
    mail = EmailMessage(mail_subject,message,from_email,[to_email])
    #print(mail)
    mail.send()
    
# def send_password_reset_email(request,user):
#     from_email = settings.DEFAULT_FROM_EMAIL
#     #print('inside the send verification function')
#     current_site = get_current_site(request)
#     #print(current_site)
#     mail_subject = 'Reset Your Password '
#     message = render_to_string('accounts/emails/reset_password.html',{
#             'user':user,
#             'domain':current_site,
#             'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#             'token':default_token_generator.make_token(user),
            
#     })
#     to_email = user.email
#     #print(to_email)
#     mail = EmailMessage(mail_subject,message,from_email,[to_email])
#     #print(mail)
#     mail.send()


#helper function to send vendor notification that he is approved or not
def send_notification(mail_subject,mail_template,context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template,context)
    to_email = context['user'].email
    mail = EmailMessage(mail_subject,message,from_email,[to_email])
    mail.send()
    