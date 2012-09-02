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

            return authenticate(request, username, password)
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

"""
def determineNumber(inputDay):
    if inputDay == 'Monday':
        return 1
    if inputDay == 'Tuesday':
        return 2
    if inputDay == 'Wednesday':
        return 3
    if inputDay == 'Thursday':
        return 4
    if inputDay == 'Friday':
        return 5
    return 1
"""

#Disgusting, but guaranteed to be production ready. Next time I'll use South so I don't feel the need to shoot myself.

def week(request, weeknumber):
    readingM = PatelActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Monday')
    readingT = PatelActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Tuesday')
    readingW = PatelActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Wednesday')
    readingU = PatelActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Thursday')
    readingF = PatelActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Friday')

    assignM = PatelActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Monday')
    assignT = PatelActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Tuesday')
    assignW = PatelActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Wednesday')
    assignU = PatelActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Thursday')
    assignF = PatelActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Friday')

    readingactivities = PatelActivity.objects.filter(week=weeknumber, typeofact='R').order_by('-duedate')
    assignactivities = PatelActivity.objects.filter(week=weeknumber, typeofact='A').order_by('-duedate')
    displaycollege = 'Patel'
    if request.user.is_anonymous():
        print "user was anonymous"
        readingM = PatelActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Monday')
        readingT = PatelActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Tuesday')
        readingW = PatelActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Wednesday')
        readingU = PatelActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Thursday')
        readingF = PatelActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Friday')

        assignM = PatelActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Monday')
        assignT = PatelActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Tuesday')
        assignW = PatelActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Wednesday')
        assignU = PatelActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Thursday')
        assignF = PatelActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Friday')
        
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
                readingM = PatelActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Monday')
                readingT = PatelActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Tuesday')
                readingW = PatelActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Wednesday')
                readingU = PatelActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Thursday')
                readingF = PatelActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Friday')

                assignM = PatelActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Monday')
                assignT = PatelActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Tuesday')
                assignW = PatelActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Wednesday')
                assignU = PatelActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Thursday')
                assignF = PatelActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Friday')
            if college == 'St':
                displaycollege = 'Strople'

                readingM = StropleActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Monday')
                readingT = StropleActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Tuesday')
                readingW = StropleActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Wednesday')
                readingU = StropleActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Thursday')
                readingF = StropleActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Friday')

                assignM = StropleActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Monday')
                assignT = StropleActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Tuesday')
                assignW = StropleActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Wednesday')
                assignU = StropleActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Thursday')
                assignF = StropleActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Friday')
            if college == 'Le':
                displaycollege = 'Leung'

                readingM = LeungActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Monday')
                readingT = LeungActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Tuesday')
                readingW = LeungActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Wednesday')
                readingU = LeungActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Thursday')
                readingF = LeungActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Friday')

                assignM = LeungActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Monday')
                assignT = LeungActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Tuesday')
                assignW = LeungActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Wednesday')
                assignU = LeungActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Thursday')
                assignF = LeungActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Friday')
            if college == 'Sc':
                displaycollege = 'Schaefer'
                readingM = SchaeferActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Monday')
                readingT = SchaeferActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Tuesday')
                readingW = SchaeferActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Wednesday')
                readingU = SchaeferActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Thursday')
                readingF = SchaeferActivity.objects.filter(week=weeknumber, typeofact='R').filter(duedate='Friday')

                assignM = SchaeferActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Monday')
                assignT = SchaeferActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Tuesday')
                assignW = SchaeferActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Wednesday')
                assignU = SchaeferActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Thursday')
                assignF = SchaeferActivity.objects.filter(week=weeknumber, typeofact='A').filter(duedate='Friday')
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

            #npatel = determineNumber(fpatel)
            #nstrople = determineNumber(fstrople)
            #nleung = determineNumber(fleung)
            #nschaefer = determineNumber(fschaefer)

            print "due dates:"
            print fpatel
            print fstrople
            print fleung
            print fschaefer
            newpatel = PatelActivity(author=request.user, title=ftitle, text=ftext, typeofact=ftypeofact, week=weeknumber, duedate=fpatel, slug=123)
            newstrople = StropleActivity(author=request.user, title=ftitle, text=ftext, typeofact=ftypeofact, week=weeknumber, duedate=fstrople, slug=123)
            newleung = LeungActivity(author=request.user, title=ftitle, text=ftext, typeofact=ftypeofact, week=weeknumber, duedate=fleung, slug=123)
            newschaefer = SchaeferActivity(author=request.user, title=ftitle, text=ftext, typeofact=ftypeofact, week=weeknumber, duedate=fschaefer, slug=123)
            
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
            'readingM': readingM,
            'readingT': readingT,
            'readingW': readingW,
            'readingU': readingU,
            'readingF': readingF,
            'assignM': assignM,
            'assignT': assignT,
            'assignW': assignW,
            'assignU': assignU,
            'assignF': assignF,
            'displaycollege': displaycollege,
        },
        context_instance = RequestContext(request)
    )

# Create your views here.
