from email import message
import re
from django.http import HttpResponse
from django.shortcuts import render, redirect

from Role_based_login_system import settings
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from .models import Ngo, People, Blogs, Needy, Forms, solved_cases, Leaderboard
from django.contrib.auth.models import User, auth 
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.


def index(request):
    posts = Blogs.objects.all()
    return render(request, 'index.html', {'posts' : posts})


def register(request):
    msg = None
    if request.method == 'POST':
        ngo1 = request.POST.get('is_admin')
        people1 = request.POST.get('is_customer')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            if ngo1 :
                ngo = Ngo.objects.create(username = username, email = email, password = password)
                ngo.save()
            elif people1 :
                ngo = People.objects.create(username = username, email = email, password = password)
                ngo.save()
            return redirect('login_view')
            
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('/')
            elif user is not None and user.is_customer:
                login(request, user)
                return redirect('/')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})



def logout(request):
    auth.logout(request)
    return redirect('/')


def admin(request):
    return render(request,'admin.html')


def customer(request):
    return render(request,'customer.html')

def base(request):
    return render(request, 'base.html')


def postblog(request):
    if request.method == 'POST':
        # username = request.POST.get('username')
        title = request.POST.get('title')
        body = request.POST.get('body')
        print(request.user.id-18)
        userObj=Ngo.objects.get(id=(request.user.id-18))
        # print(request.user.id)
        blog = Blogs.objects.create(title = title, body = body)
        blog.ngo_id.add(userObj)
        blog.save()
        messages.info(request, 'Blog posted')
        # Ngo.objects.filter(id = request.user).values_list('id', flat=True).first()
        # instance = blog.save(commit = False)
        # instance.ngo_id = request.user
        # blog.save()

    return render(request, 'postblog.html')


def posts(request, pk):
    post = Blogs.objects.get(blog_id = pk)
    print(post.blog_id)
    return render(request, 'posts.html', {'post' : post})

def send(request):
    needy_id=request.POST.get('id1')
    status=request.POST.get('status1')
    pre_status=status
    ngo_name = request.user.username
    print(status)
    if status=='Approach':
        status='In Progress'
    elif status=='In Progress':
        status='Solved'
    userObj=Needy.objects.filter(needy_id=needy_id)
    # print(userObj.status)
    ngo = request.user.username
    for item in userObj:
        needy = item.name
        item.status=status
        item.save()
        user=item.people_id.all()

        if status == 'Solved':
            for j in user:
                people_name = j.username
                solvedObj = solved_cases.objects.create(ngo_name = ngo_name, user_name = people_name, needy_name = needy)
                solvedObj.save()

        print(user)
        for i in user:
            sendmail(i.email, needy, i.username, ngo, pre_status)
    messages.info(request, "Mail send to related User")
    return HttpResponse("Mail Sent")   

def sendmail(email, needy, Name, ngo,status):
    print("sending mail")
    needy = needy
    Name = Name 
    ngo = ngo
    # print(needy)
    # print(Name)
    # print(ngo)
    mail_content=""
    mail_subject=""
    if status=='Approach':
        mail_subject=f'Your Submitted form about {needy} is Taken under {ngo} NGO'
        mail_content=f"Hey {Name}\n  \nThanks for helping needy out there , keep doing good work.\n\n\nRegrads N&P Connector Team.\n\n This is system generated e-mail please don't reply"
    elif status=='In Progress':
        mail_subject=f'Congratulations, Your Submitted Case about {needy} has been solved by {ngo} NGO'
        mail_content=f"Hey {Name}\n  \nThanks for helping needy out there , keep doing good work.\n\n\nRegrads N&P Connector Team.\n\nThis is system generated e-mail please don't reply"
    subject=mail_subject
    message=mail_content
    email_from=settings.EMAIL_HOST_USER 
    recipient_list=[email]
    send_mail(subject, message,email_from,recipient_list)

def needyform(request):
    if request.method == "POST":
        # prod = Needy
        name = request.POST.get('name')
        location = request.POST.get('location')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin = request.POST.get('pin')
        photo = request.POST.get('img')
        # if len(request.FILES) != 0:
        #     photo = request.FILES('img') 

        print(request.user.id-14)
        userobj = People.objects.get(id = (request.user.id-16))
        form = Needy.objects.create(name = name, location = location, city = city, state = state, pin = pin, photo = photo)
        form.people_id.add(userobj)
        form.save()
        # prod.save()
        messages.info(request, 'Form Submitted Successfully')
        
    return render(request, 'needyform.html')


def needy(request):
    x = Needy.objects.all()
    return render(request, 'needy.html', {'x' : x})

def leaderboard(request):
    return render(request, 'leaderboard.htnl')

def contact(request):
    if request.method == 'POST':
        message_name = request.POST.get('name')
        message_email = request.POST.get('email')
        message_subject = request.POST.get('subject')
        message = request.POST.get('message')
        to_email = ['amanpalsinghrana27@gmail.com']

        send_mail(
            message_name,
            message,
            message_email,
            to_email,
        )

        return render(request, 'contact.html', {'message_name' : message_name})
    else:
        return render(request, 'contact.html')


def feed(request):
    name = request.POST.get('name1')
    email = request.POST.get('email1')
    subject = request.POST.get('subject1')
    message = request.POST.get('message1')
    print(name, email, subject, message)
    return HttpResponse('done')




