from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
from django.views.decorators.http import require_http_methods
from djangoapp.models import CarModel

from djangoapp.restapis import (
    get_dealer_reviews_from_cf,
    get_dealers_from_cf,
    post_request,
)


DEALERSHIPS_URL = "https://us-south.functions.appdomain.cloud/api/v1/web/bayajitmohammed_djangoserver-space/dealership-package/get-dealership"

REVIEWS_URL = "https://us-south.functions.appdomain.cloud/api/v1/web/bayajitmohammed_djangoserver-space/dealership-package/get-review"

ADD_REVIEW_URL = "https://us-south.functions.appdomain.cloud/api/v1/web/bayajitmohammed_djangoserver-space/dealership-package/post-review"

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
@require_http_methods(["GET"])
def about(request):
    context = {}
    return render(request, "djangoapp/about.html", context)


# Create a `contact` view to return a static contact page
@require_http_methods(["GET"])
def contact(request):
    context = {}
    return render(request, "djangoapp/contact.html", context)


# Create a `login_request` view to handle sign in request
@require_http_methods(["POST"])
def login_request(request):
    context = {}
    # Get username and password from request.POST dictionary
    username = request.POST["username"]
    password = request.POST["password"]
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        return redirect("djangoapp:index")
    return redirect("djangoapp:index")


# Create a `logout_request` view to handle sign out request
@require_http_methods(["GET"])
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect("djangoapp:index")


# Create a `registration_request` view to handle sign up request
@require_http_methods(["GET", "POST"])
def registration_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
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
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, "djangoapp/registration.html", context)
    return render(request, "djangoapp/registration.html", context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
@require_http_methods(["GET"])
def get_dealerships(request):
    context = {}
    # Get dealers from the URL
    dealership_list = get_dealers_from_cf(DEALERSHIPS_URL)
    context["dealership_list"] = dealership_list

    return render(request, "djangoapp/index.html", context)


# Create a `get_dealer_details` view to render the reviews of a dealer
@require_http_methods(["GET"])
def get_dealer_details(request, dealer_id):
    context = {}

    reviews = get_dealer_reviews_from_cf(REVIEWS_URL, dealer_id)
    context["reviews"] = reviews
    context["dealer_id"] = dealer_id
    context["dealership"] = get_dealers_from_cf(DEALERSHIPS_URL, dealerId=dealer_id)[0]
    return render(request, "djangoapp/dealer_details.html", context)


def validate_review(data: dict):
    if not data.get("review"):
        return False
    if data.get("purchase") == "on" and (
        not data.get("purchase_date") or not data.get("car")
    ):
        return False
    return True


# Create a `add_review` view to submit a review
@require_http_methods(["GET", "POST"])
def add_review(request, dealer_id):
    context = {}

    if request.user.is_authenticated:
        context["dealer_id"] = dealer_id
        context["cars"] = CarModel.objects.filter(dealer_id=dealer_id)
        context["dealership"] = get_dealers_from_cf(
            DEALERSHIPS_URL, dealerId=dealer_id
        )[0]
        if request.method == "POST":
            if validate_review(request.POST):
                data = request.POST
                user = request.user
                cleaned_data = {
                    "review": data.get("review"),
                    "dealership": dealer_id,
                    "name": f"{user.first_name} {user.last_name}",
                    "purchase": data.get("purchase") == "on",
                }
                if data.get("purchase") == "on":
                    car = CarModel.objects.filter(id=data.get("car")).first()
                    cleaned_data = {
                        **cleaned_data,
                        **{
                            "purchase": data.get("purchase") == "on",
                            "car_make": car.carmake.name,
                            "car_model": car.name,
                            "car_year": car.year,
                            "purchase_date": datetime.strptime(
                                data.get("purchase_date"), "%Y-%m-%d"
                            ).strftime("%d/%m/%Y"),
                        },
                    }
                    print(cleaned_data)
                res = post_request(ADD_REVIEW_URL, {"review": cleaned_data})
                if res.get("ok"):
                    messages.success(request, "Review added.")
                    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
                messages.error(request, "Something went wrong.")
                return redirect("djangoapp:add_review", dealer_id=dealer_id)
            messages.error(request, "Fields are empty.")
            return redirect("djangoapp:add_review", dealer_id=dealer_id)
        else:
            return render(request, "djangoapp/add_review.html", context)
    return redirect("djangoapp:login")
