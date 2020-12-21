from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

# Create your views here.

##PAGE RENDERS
def index(request):
    return render(request, "index.html")

def login_reg(request):
    return render(request, "logandreg.html")

def home(request):
    if 'user_id' not in request.session:
        return redirect("/")
    return render(request, "home.html")

def recent(request):
    return render(request, 'recent.html')

def trending(request):
    return render(request, 'trending.html')
     
def a_z(request):
    return render(request, 'a_z.html')

def create(request):
    return render(request, 'create.html')


##CREATE DATA    
def register(request):
    if request.method=="POST":
        errors = User.objects.validate(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/login_reg')

        # password encrypt
        user_pw = request.POST['pw']
        hash_pw = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()

        # create the new user
        new_user = User.objects.create(first_name=request.POST['f_n'], last_name=request.POST['l_n'], email=request.POST['email'], password=hash_pw)
        print(f"first_name:{request.POST['f_n']}, last_name:{request.POST['l_n']}, email:{request.POST['email']}, password:{request.POST['pw']}, (hash: {hash_pw}).")

        # store user info in session
        request.session['user_id'] = new_user.id
        request.session['user_name'] = f"{new_user.first_name} {new_user.last_name}"

        return redirect('/home')

    # was not a post request, send user back to home page
    return redirect('/')


##ACTIONS
def login(request):
    if request.method == 'POST':
        # see if email is in the DB
        logged_user = User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user = logged_user[0]    # strip the curlies 
            # compare the passwords
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                request.session['user_name'] = f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/home')
            else:
                # bad password
                messages.error(request, "Incorrect password")
                return redirect('/login_reg')
        else: 
            # didn't find user in the database
            messages.error(request, "Email address is not registered")
            return redirect('/login_reg')

    # was not a post request, send user back to home page
    return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')

