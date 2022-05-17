from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from authentication.tokens import generate_token
from Dlog import settings

#For to-do list

from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def home(request):
    return render(request, "signin.html", )


def contact(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    number=request.POST.get('number')
    query=request.POST.get('query')
    subject=f"D-Log query of {name}"
    message=f"{subject}\n{query}"
    from_email = email
    to_list = [settings.EMAIL_HOST_USER]            #To must be a list
    send_mail(subject, message, from_email, to_list, fail_silently=True)
    # messages.success("Thank You your response is noted.")
    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")


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
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, "E-Mail Already Exists!!! Please Try some Other Email")
            return redirect('signup')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 Characters!!!")
            return redirect('signup')

        if password != cpassword:
            messages.error(request, "Passwords didn't match!!!")
            return redirect('signup')

        # if not username.isalpha():
        #     messages.error(request, "Username must be Alpha-Numberic")
        #     return redirect('home')

        # Saving image in the database
        # userimage = Image()
        # userimage.image = image
        # userimage.username = username
        # userimage.save()

        # saving credentials in the user database
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False  # We first deactivate the account then after user click the link it will get activated
        myuser.save()

        # messages.success(request,
        #                  '''Your account has been created. We have sent you a confirmation email. Please confirm your
        #                  email in order to activate your account''')

        # Welcome Email
        subject = " Welcome to our own Dlog.in Website"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Site!!\nThank you for visiting the website and registering yourself on it.\n We have sent you a confirmation e-mail.\nPlease confirm your E-mail address to start your account.\n\nThank You. "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]  # To whom the email is to be sent
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # E-Mail address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @D-Log.in"
        message2 = render_to_string("email_confirmation.html", {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        from django.core.mail import EmailMessage
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
        # pass a whole dictionary
        return render(request, "linkactivate.html", {'fname': fname})

    return render(request, "signup.html")


def linkactivate(request):
    return render(request, "linkactivate.html")


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        myuser = authenticate(username=username, password=password)
        if myuser is not None:
            print(username, password)
            login(request, myuser)
            fname = myuser.first_name
            # img = Image.objects.get(username=myuser.username)
            # print(img)
            # return render(request, "signedin.html", {'fname': fname})
            return redirect('tasks')

        else:
            messages.error(request, "Wrong Credentials")
            return redirect("signin")

    return render(request, "signin.html")


def signedin(request):
    # return render(request, "signedin.html")
    return redirect('tasks')


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    # return redirect("home")
    return redirect("signin")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        username = myuser.username
        password = myuser.password
        myuser.is_active = True
        fname = myuser.first_name
        myuser.save()
        # img = Image.objects.get(username=myuser.username)
        # print(img)
        login(request, myuser, backend='django.contrib.auth.backends.ModelBackend')
        # return render(request, "signedin.html", {'fname': fname})
        return redirect('tasks')
    else:
        return render(request, 'activation_failed.html')

#To-do list

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['tasks']= context['tasks'].filter(user=self.request.user)
        context['count']= context['tasks'].filter(complete=False).count()

        search_input= self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__startswith=search_input)

        context['search_input']=search_input
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name = 'task'
    template_name = 'authentication/task_list.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name= 'task'
    success_url = reverse_lazy('tasks')
