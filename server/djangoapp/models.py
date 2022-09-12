from django.db import models
from django.utils.timezone import now
import datetime

def year_choices():
    return [(r,r) for r in range(1800, datetime.date.today().year+1)]

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
    carmake = models.ForeignKey(CarMake,on_delete=models.CASCADE,)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    dealer_id = models.IntegerField()
    TYPE_CHOICES = [('sd','Sedan'), ('sv', 'SUV'), ( 'wg', 'WAGON')]
    model_type = models.CharField(max_length=200, choices=TYPE_CHOICES)
    year = models.IntegerField('year', choices=year_choices(), default=current_year)


    def __str__(self):
        return self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
