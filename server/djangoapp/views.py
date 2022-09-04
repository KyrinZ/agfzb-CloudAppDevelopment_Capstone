from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.http import require_http_methods

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
@require_http_methods(["GET"])
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
@require_http_methods(["GET"])
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
@require_http_methods(["POST"])
def login_request(request):
    context = {}
    # Get username and password from request.POST dictionary
    username = request.POST['username']
    password = request.POST['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        return redirect('djangoapp:index')
    return redirect('djangoapp:index')   

# Create a `logout_request` view to handle sign out request
@require_http_methods(["GET"])
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')  


# Create a `registration_request` view to handle sign up request
@require_http_methods(["GET", "POST"])
def registration_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))

        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username,password=password,first_name=first_name, last_name=last_name)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)
    return render(request, 'djangoapp/registration.html', context)
 

# Update the `get_dealerships` view to render the index page with a list of dealerships
@require_http_methods(["GET"])
def get_dealerships(request):
    context = {}
    return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

