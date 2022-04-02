from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from authentication.tokens import generate_token
from gfg import settings


# Create your views here.
def home(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if User.objects.filter(username=username):
            messages.error(request, "Username Already Exists!!! Please Try some Other Username")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "E-Mail Already Exists!!! Please Try some Other Email")
            return redirect('home')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 Characters!!!")
            return redirect('home')

        if password != cpassword:
            messages.error(request, "Passwords didn't match!!!")
            return redirect('home')

        # if not username.isalpha():
        #     messages.error(request, "Username must be Alpha-Numberic")
        #     return redirect('home')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active=False      #We first deactivate the account then after user click the link it will get activated
        myuser.save()

        messages.success(request,
                         "Your account has been created. We have sent you a confirmation email. Please confirm your "
                         "email in order to activate your account")

        # Welcome Email
        subject = " Welcome to My own Django-Login Website"
        message = "Hello " + myuser.first_name+"!! \n"+"Welcome to Site!!\nThank you for visiting the website.\n We have sent you a confirmation e-mail.\nPlease confirm your E-mail address to start your account.\n\nThank You. "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]  # To whom the email is to be sent
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # E-Mail address Confirmation Email
        current_site=get_current_site(request)
        email_subject= "Confirm your Email @gfg Django Login"
        message2=render_to_string("email_confirmation.html",{
            'name':myuser.first_name,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser)
        })
        from django.core.mail import EmailMessage
        email=EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently=True
        email.send()
        return redirect("signin")

    return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        myuser = authenticate(username=username, password=password)
        if myuser is not None:
            print(username, password)
            login(request, myuser)
            fname = myuser.first_name
            return render(request, "index.html", {'fname': fname})

        else:
            messages.error(request, "Wrong Credentials")
            return redirect("/")

    return render(request, "signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect("home")

def activate(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser=None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active=True
        myuser.save()
        login(request,myuser)
        return redirect("home")
    else:
        return render(request,'activation_failed.html')

