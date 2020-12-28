from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *
from django.db.models import Q
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Create your views here.

##PAGE RENDERS
def index(request):
    return render(request, "index.html")

def login_reg(request):
    return render(request, "logandreg.html")

def home(request):
    if 'user_id' not in request.session:
        return redirect("/")
    context ={
        'page_name': "Home",
        'recents': Image.objects.filter(name__startswith="recent"),
        'trending': Image.objects.filter(name__startswith="trending"),
        'all_cards': Image.objects.filter(name__startswith="all")
    }
    return render(request, "home.html", context)

def recent(request):
    user = get_user(request)
    cards = Image.objects.filter(Q(uploaded_by=None, name__startswith="recent") | Q(uploaded_by=user))
    context ={
        'page_name': "Recent",
        'cards': cards,
    }
    return render(request, 'base_card.html', context)

def trending(request):
    user = get_user(request)
    cards = Image.objects.filter(Q(uploaded_by=None, name__startswith="trending" )| Q(uploaded_by=user))
    context ={
        'page_name': "Trending",
        'cards': cards,
    }
    return render(request, 'base_card.html', context)
     
def a_z(request):
    user = get_user(request)
    cards = Image.objects.filter(Q(uploaded_by=None) | Q(uploaded_by=user))
    context ={
        'page_name': "A-Z",
        'cards': cards,
    }
    return render(request, 'base_card.html', context)

def create(request):
    return render(request, 'create.html')

def image_details(request, img_id):
    context={
        'card': Image.objects.get(id=img_id),
        'specific': True,
        
    }
    return render(request, 'create.html', context)

def search(request):
    if request.method=="POST":
        # get search text
        stext = request.POST['search']
        print(f"search text: {stext}")

        # add check for no text or only whitespace, if so, return to page
 
        # search the DB using filter
        qs = Image.objects.filter(name__icontains=stext)
        print(f"query set: {qs}")
        # print(f"1st image name: {qs[0].name}")

        # return the query set, for now
        context={
            'image_objs': qs
        }
        return render(request, 'search.html', context)

    # not a POST request,  send em back home
    return redirect('/')

def test(request):
    return render (request, 'test2.html')


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

def upload_media(request):
    if request.method == 'POST':
        this_user = get_user(request)
        file = request.FILES
        media = file.get('media')
        this_media = Image()
        this_media.img = media
        this_media.name = media.name
        this_media.uploaded_by = this_user
        this_media.save()
    return redirect(f'/create/{this_media.id}') 
        
        # cloudinary.uploader.upload(f'/media/{this_user.id}/')
        
def review(request, img_id):
    if request.method == 'POST':
        gText = request.POST['greet_text']
        # Create a Card
        cName = 'temp'
        cCreator = get_user(request)
        cMessage = gText
        cCard = Card.objects.create(name=cName, creator=cCreator, message=cMessage)
        print(f"card id: {cCard.id}")
        # add the Image to the Card
        cImage = Image.objects.get(id=img_id)
        cCard.images.add(cImage)

        # even tho we have the image id here, get it from Card (NEED to in view_card!)
        cAllImages = cCard.images.all()
        cImage2 = cAllImages[0]             # cAllImages is a list, strip the curlies
        context={
            'image': cImage2,
            'card': cCard
        }
    return render(request, 'review.html', context)

def view_card(request, card_id):
    # no POST required: a guest has come to view a card.
    # get the Card, then display it (image and greeting text)
    cCard = Card.objects.get(id=card_id)
    # get the 1st image of the card
    cAllImages = cCard.images.all()
    cImage = cAllImages[0]             # cAllImages is a list, strip the curlies
    context={
        'image': cImage,
        'card': cCard
    }
    return render(request, 'view_card.html', context)

def send_email(request, card_id):
    if request.method == 'POST':
        recip = request.POST['email_addr']
        print(f"recip addr: {recip}")
        # send the email: 
        # TODO: put smtp parameters in settings.py
        # put call to send_mail in here, dont forget import (see solo/hg*)

        # go back to review: user may want to send multiple emails
        cCard = Card.objects.get(id=card_id)
        # get the 1st image of the card
        cAllImages = cCard.images.all()
        cImage = cAllImages[0]             # cAllImages is a list, strip the curlies
        context={
            'image': cImage,
            'card': cCard
        }
        return render(request, 'review.html', context)

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

def get_user(request):
    return User.objects.get(id=request.session['user_id'])

def confirm_session(request):
    if 'user_id' in request.session:
        return redirect('/')
    return
    
