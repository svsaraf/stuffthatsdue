from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect


from app.forms import RegistrationForm
from app.forms import ActivityForm

from django.contrib.auth.models import User
from app.models import UserProfile, PatelActivity, LeungActivity, StropleActivity, SchaeferActivity

def index(request):
    # If not logged in, then go to register page
	return redirect('/week/3')

def about(request):
    return render_to_response("about.html", {

        },
        context_instance = RequestContext(request)
    )

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            location = email.find("@")
            username = email[:location]

            user = User.objects.create_user(username, #email is username
                                            email, #email
                                            password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            up = UserProfile(user=user, college=form.cleaned_data['college'])
            up.save()

            #request.session['next'] = '/'

            return authenticate(request, email, password)
    else:
        form = RegistrationForm()
    
    return render_to_response("login.html", {
            'form': form,
        },
        context_instance = RequestContext(request)
    )

def authenticate(request, email, password):
    user = auth.authenticate(username=email, password=password)
    if user is not None:
        if not user.is_active:
            auth.logout(request)
            return redirect('/') 

        auth.login(request, user)

        if 'next' in request.session:
            next = request.session['next']
            del request.session['next']
            return redirect(next)

        return redirect('/') 
    else:
        form = RegistrationForm()
        return render_to_response("login.html", {
                'login_error': True, # indicates username / pword did not match
                'form': form,
            },
            context_instance = RequestContext(request)
        )
        
@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

@csrf_protect
def login(request):
    if request.method == "POST":
        activeemail = request.POST['email']
        location = activeemail.find("@")
        username = activeemail[:location]
        return authenticate(request, username, request.POST['password'])
    return redirect('/')

def week(request, weeknumber):
    readingactivities = PatelActivity.objects.filter(week=weeknumber, typeofact='R').order_by('-duedate')
    assignactivities = PatelActivity.objects.filter(week=weeknumber, typeofact='A').order_by('-duedate')
    displaycollege = 'Patel'
    if request.user.is_anonymous():
        print "user was anonymous"
        readingactivities = PatelActivity.objects.filter(week=weeknumber, typeofact='R').order_by('-duedate')
        assignactivities = PatelActivity.objects.filter(week=weeknumber, typeofact='A').order_by('-duedate')
    else:
        print "user was logged in."
        try:
            profile = request.user.get_profile()
            print "getting the profile!"
            college = profile.college
            if college == 'Pa':
                displaycollege = 'Patel'
                readingactivities = PatelActivity.objects.filter(week=weeknumber, typeofact='R').order_by('-duedate')
                assignactivities = PatelActivity.objects.filter(week=weeknumber, typeofact='A').order_by('-duedate')
            if college == 'St':
                displaycollege = 'Strople'
                readingactivities = StropleActivity.objects.filter(week=weeknumber, typeofact='R').order_by('-duedate')
                assignactivities = StropleActivity.objects.filter(week=weeknumber, typeofact='A').order_by('-duedate')
            if college == 'Le':
                displaycollege = 'Leung'
                readingactivities = LeungActivity.objects.filter(week=weeknumber, typeofact='R').order_by('-duedate')
                assignactivities = LeungActivity.objects.filter(week=weeknumber, typeofact='A').order_by('-duedate')
            if college == 'Sc':
                displaycollege = 'Schaefer'
                readingactivities = SchaeferActivity.objects.filter(week=weeknumber, typeofact='R').order_by('-duedate')
                assignactivities = SchaeferActivity.objects.filter(week=weeknumber, typeofact='A').order_by('-duedate')
        except:
            print "hit exception"
            pass

    if request.method == 'POST':
        if request.user.is_anonymous():
            return redirect('/register')
        form = ActivityForm(request.POST)
        if form.is_valid():
            ftitle = form.cleaned_data['title']
            ftext = form.cleaned_data['text']
            ftypeofact = form.cleaned_data['typeofact']
            fpatel = form.cleaned_data['patelduedate']
            fstrople = form.cleaned_data['stropleduedate']
            fleung = form.cleaned_data['leungduedate']
            fschaefer = form.cleaned_data['schaeferduedate']
            print "due dates:"
            print fpatel
            print fstrople
            print fleung
            print fschaefer
            newpatel = PatelActivity(author=request.user, title=ftitle, text=ftext, typeofact=ftypeofact, week=weeknumber, duedate=fpatel)
            newstrople = StropleActivity(author=request.user, title=ftitle, text=ftext, typeofact=ftypeofact, week=weeknumber, duedate=fstrople)
            newleung = LeungActivity(author=request.user, title=ftitle, text=ftext, typeofact=ftypeofact, week=weeknumber, duedate=fleung)
            newschaefer = SchaeferActivity(author=request.user, title=ftitle, text=ftext, typeofact=ftypeofact, week=weeknumber, duedate=fschaefer)
            
            #print user.college

            newpatel.save()
            newstrople.save()
            newleung.save()
            newschaefer.save()

#            print "Starting post request here"
#            print "User:" + request.user.first_name + request.user.last_name
#            print "Title:" + title
#            print "Text:" + text
#            print "Type of activity:" + typeofact
#            print "Patel:" + patel
#            print "Strople:" + strople
#            print "Leung:" + leung
#            print "Schaefer:" + schaefer

        return redirect('/week/'+ weeknumber)
    else:
        form = ActivityForm()
    return render_to_response("home.html", {
            'form': form,
            'weeknumber': weeknumber,
            'readingactivities': readingactivities,
            'assignactivities': assignactivities,
            'displaycollege': displaycollege,
        },
        context_instance = RequestContext(request)
    )

# Create your views here.
