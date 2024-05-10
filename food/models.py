from django.db import models

# Create your models here.
class person_details(models.Model):
    age = models.IntegerField(default = 18)
    height = models.FloatField(default = 150.0)
    weight = models.FloatField(default = 50.0)
    gender = models.CharField(max_length = 50,default='male',choices=(('male','Male'),('female','Female')))
    activity = models.CharField(max_length=50,default = 'sedentary',choices=(
        ('sedentary','Sedentary'),
        ('lightly_active','Lightly Active'),
        ('moderately_active','Moderately Active'),
        ('very_active','Very Active'),
        ('extra_active','Extra Active')
    ))
    # weight_plan = models.CharField(max_length=50,default='maintain_weight',choices=(
    #     ('maintain_weight','Maintain Weight'),
    #     ('weight_loss','Weight Loss'),
    #     ('weight_gain','Weight Gain'),
    #     ('extreme_weight_loss','Extreme Weight Loss')
    # ))
    weight_plan = models.CharField(max_length = 100)
    meals = models.IntegerField(default=3,choices=(
        (3,3),
        (4,4),
        (5,5)
    ))

class nutrition_details(models.Model):
    CaloriesNeeded = models.CharField(max_length = 50)
    SaturatedFatContent = models.IntegerField(default=25)
    CholesterolContent = models.IntegerField(default=130)
    SodiumContent = models.IntegerField(default=50)
    CarbohydrateContent = models.IntegerField(default=250)
    FiberContent = models.IntegerField(default=20)
    SugarContent = models.IntegerField(default=100)
    ProteinContent = models.IntegerField(default=50)
    num_recomm = models.IntegerField(default=5)

class namaste(models.Model):
    name = models.CharField(max_length = 50)