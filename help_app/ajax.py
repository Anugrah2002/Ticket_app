from django.core.mail import send_mail
from django.http import HttpResponse
from django.template import loader

from help_desk import settings
from .views import password_generator


def send_OTP(request):
    otp = password_generator()
    email = request.POST.get('email')
    html_message = loader.render_to_string('emails/otp_email.html', {'otp': otp})
    mail = send_mail('Otp Verification', '', settings.EMAIL_HOST_USER, [email], html_message=html_message, fail_silently=False)
    request.session['otp'] = otp
    request.session['emailAddress'] = email
    if mail:
        return HttpResponse("send")
    else:
        return HttpResponse("un_send")


def verify_OTP(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        email = request.POST.get('email')
        if otp == request.session['otp'] and email == request.session['emailAddress']:
            return HttpResponse("verified")
        else:
            return HttpResponse("not verified")
