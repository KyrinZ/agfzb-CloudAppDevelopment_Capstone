from django.db import models
from django.utils.timezone import now
import datetime


def year_choices():
    return [(r, r) for r in range(1800, datetime.date.today().year + 1)]


def current_year():
    return datetime.date.today().year


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    carmake = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    dealer_id = models.IntegerField()
    TYPE_CHOICES = [("sd", "Sedan"), ("sv", "SUV"), ("wg", "WAGON")]
    model_type = models.CharField(max_length=200, choices=TYPE_CHOICES)
    year = models.IntegerField("year", choices=year_choices(), default=current_year)

    def __str__(self):
        return self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(
        self,
        dealership,
        name,
        purchase,
        review,
        purchase_date,
        car_make,
        car_model,
        car_year,
        sentiment,
        id,
    ):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "Dealer name: " + self.full_name
