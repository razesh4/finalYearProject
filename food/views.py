from django.shortcuts import render
from .serializers import serializer_person_details,serializer_nutrition_details,serializer_namaste
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random

#Custsom recommedation library 
from .recommendation_model import recomm
from .ann_model import Load_data,nutrient_reccommend,drinks,food_recommend
Load_data()

#newly code here is the Functions 
def BMR(weight,age,height,gender):
  if gender == 'male':
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
  else:
    bmr = bmr=10 * weight + 6.25 * height-5 * age - 161
  return bmr

def energy_for_activity_level(bmr,activity):
  #this is the calories level for balance weight
  if activity == 'sedentary':
    CaloriesNeede = bmr * 1.2
  elif activity == 'lightly_active':
    CaloriesNeede = bmr * 1.375
  elif activity == 'moderately_active':
    CaloriesNeede = bmr * 1.55
  elif activity == 'very_active':
    CaloriesNeede = bmr*1.725
  elif activity =='extra_active':
    CaloriesNeede = bmr*1.9
  return CaloriesNeede

def weight_gain_loss(calories, weight_plan):
  if weight_plan == 'weight_gain':
      calories += round(random.uniform(500,1000),0)
  elif weight_plan == 'weight_loss':
      calories -= round(random.uniform(200,400),0)
  elif weight_plan == 'extreme_weight_loss':
      calories -= round(random.uniform(550,950),0)
  else:
      calories += 10
  # print('weightplan calories'+str(type(calories)))
  return calories



# Create your views here.
def index(request):
    # return HttpResponse('welcome ')
    try:
        if request.method == "POST":
            CaloriesNeeded = int(request.POST.get('CaloriesNeeded'))
            FatContent = int(request.POST.get('SaturatedFatContent'))
            CholesterolContent = int(request.POST.get('CholesterolContent'))
            SodiumContent = int(request.POST.get('SodiumContent'))
            CarbohydrateContent = int(request.POST.get('CarbohydrateContent'))
            FiberContent = int(request.POST.get('FiberContent'))
            ProteinContent = int(request.POST.get('ProteinContent'))
            CalciumContent = int(request.POST.get('CalciumContent'))
            PhosphorousContent = int(request.POST.get('PhosphorousContent'))
            PotassiumContent = int(request.POST.get('PotassiumContent'))
            num_recomm = int(request.POST.get('num_recomm'))

            print("calories={},Fat={},Cholestrol={},Sodium={},Carbo={},fiber={},protein={},calcium={},phosphorous={},potassium={},meals={}".format(
               CaloriesNeeded,
               FatContent,
               CholesterolContent,
               SodiumContent,
               CarbohydrateContent,
               FiberContent,
               ProteinContent,
               CalciumContent,
               PhosphorousContent,
               PotassiumContent,
               num_recomm))
            

            nuts = [
               CaloriesNeeded,
               FatContent,
               CholesterolContent,
               SodiumContent,
               CarbohydrateContent,
               FiberContent,
               ProteinContent,
               CalciumContent/10,
               PhosphorousContent/10,
               PotassiumContent/10
            ]
            foods = nutrient_reccommend(nuts,num_recomm)
            a = zip(foods[0],foods[1],foods[2])
            print(foods)
            
            datas = {
              'output' : a,
              'calorie' : CaloriesNeeded,
              'drinks':drinks()
              }

            context = {
               'datas' : [datas]
            }
        return render(request,'list.html',context)
    except:
        pass
    data = {
        'user' : 'rajesh sharma'
    }
    return render(request, "index2.html",{'data': data})


# for home directory we have index.html and list1.html for IN & OUT
def home(request):
    # return HttpResponse('welcome')
    try:
        if request.method == "POST":
            age = int(request.POST.get('age'))
            height = int(request.POST.get('height'))
            weight = int(request.POST.get('weight'))
            gender = request.POST.get('gender')
            activity = request.POST['activity']
            weight_plan = request.POST['weight_plan']
            meals = int(request.POST.get('meals'))
            # Calculating BMR value
            bmr = BMR(weight=weight,age=age,height=height,gender=gender)
            # Calculating Calories based on activity
            CaloriresNeeded = energy_for_activity_level(bmr=bmr,activity=activity)
            # Adjusting the Calories according to weight plan
            CaloriresNeeded = weight_gain_loss(CaloriresNeeded,weight_plan)
            # round off the Calories
            CaloriresNeeded = round(CaloriresNeeded)
            print(CaloriresNeeded)

            # Checking the POST values from HTML form page
            print("age={},height={},weight={},gender={},activity={},weight plan={},meals={}".format(age,height,weight,gender,activity,weight_plan,meals))

            food = food_recommend(CaloriresNeeded,meals)
            foodNamesFive = []
            calorieFive = []
            weightFive = []
            for i in range(len(food)):
                f = random.sample(list(food[i]['Food_Name'].values()),5)
                c = random.sample(list(food[i]['Calorie'].values()),5)
                w = random.sample(list(food[i]['weight(in gram)'].values()),5)
                foodNamesFive.append(f)
                calorieFive.append(c)
                weightFive.append(w)

            print(foodNamesFive,calorieFive,weightFive)
            # print(food)


            output = ['Boston Cream Pie', 'Lime Pistachio Bars', 'Almond Paste', 'Blue Jimmy Pillows', 'Low-Fat Burgundy Beef & Vegetable Stew']
            output1 = output
            output2 = output
            output3 = output
            output4 = output
            output5 = output
    
            if meals == 3:
              foodTimes = {'breakfast':0.35,'lunch':0.40,'dinner':0.25}
              newOutput = [output1,output2,output3]
            elif meals == 4:
                foodTimes = {'breakfast':0.30,'brunch':0.05,'lunch':0.40,'dinner':0.25}
                newOutput = [output1,output2,output3,output4]
            else:
                foodTimes = {'breakfast':0.30,'brunch':0.05,'lunch':0.40,'snack':0.05,'dinner':0.20}
                newOutput = [output1,output2,output3,output4,output5]
          
            newOutput = zip(foodTimes.items(),foodNamesFive,calorieFive,weightFive)
            datas = {
              'output' : newOutput,
              'CaloriresNeeded' : CaloriresNeeded,
              'calorieFive':calorieFive,
              'weightFive':weightFive,
              'drinks':drinks()
              }

            context = {
               'datas' : [datas]
            }
            # submit = True
        return render(request,'list1.html',context)
    except:
        pass
    return render(request,"index.html")

@api_view(['POST'])
def nutrition(request):
  try:
    nutrition_serializer = serializer_nutrition_details(data=request.data)
    if nutrition_serializer.is_valid():
       print(nutrition_serializer.data)
       pass
    else:
       return Response({'message':'some values are missing at nutrition'})
    return Response({'message':'your data is processing now on nutrition.'})
  except:
     return Response({'message':'your at the response page from nutrition'})



@api_view(['POST'])
def person(request):
  try:
    person_serializer = serializer_person_details(data=request.data)
    # print(type(person_serializer.data))
    if person_serializer.is_valid():
        # print(person_serializer.data)
        age = person_serializer.data['age']
        height = person_serializer.data['height']
        weight = person_serializer.data['weight']
        gender = person_serializer.data['gender']
        activity = person_serializer.data['activity']
        weight_plan = person_serializer.data['weight_plan']
        meals = person_serializer.data['meals']
        print(age,height,weight,gender,activity,weight_plan,meals)
        # print(type(age),type(height),type(weight),type(gender),type(activity),type(weight_plan),type(meals))
        # print(type(person_serializer.data))
        bmr = BMR(weight=weight,age=age,height=height,gender=gender)
        CaloriresNeeded = energy_for_activity_level(bmr=bmr,activity=activity)
        CaloriresNeeded = weight_gain_loss(CaloriresNeeded,weight_plan)
        # recommended_lists = recomm(CaloriresNeeded,meals)

        
        food = food_recommend(2200,meals)
        foodNamesFive = []
        calorieFive = []
        weightFive = []
        vegNonVeg = []
        for i in range(len(food)):
            f = list(food[i]['Food_Name'].values())
            c = list(food[i]['Calorie'].values())
            w = list(food[i]['weight(in gram)'].values())
            v = list(food[i]['Veg _Non_Veg'].values())
            foodNamesFive.append(f)
            calorieFive.append(c)
            weightFive.append(w)
            vegNonVeg.append(v)
        foodDetails = [foodNamesFive,calorieFive,weightFive,drinks(),vegNonVeg]
        print(foodNamesFive,calorieFive,weightFive,vegNonVeg)

        # print(recommended_lists)
        # print(CaloriresNeeded)

        # output = ['Boston Cream Pie', 'Lime Pistachio Bars', 'Almond Paste', 'Blue Jimmy Pillows', 'Low-Fat Burgundy Beef & Vegetable Stew']
        # output1 = output
        # output2 = output
        # output3 = output
        # output4 = output
        # output5 = output

        # if meals == 3:
        #   foodTimes = {'breakfast':0.35,'lunch':0.40,'dinner':0.25}
        #   newOutput = [output1,output2,output3]
        # elif meals == 4:
        #     foodTimes = {'breakfast':0.30,'brunch':0.05,'lunch':0.40,'dinner':0.25}
        #     newOutput = [output1,output2,output3,output4]
        # else:
        #     foodTimes = {'breakfast':0.30,'brunch':0.05,'lunch':0.40,'snack':0.05,'dinner':0.20}
        #     newOutput = [output1,output2,output3,output4,output5]
        
        # print(foodTimes,len(newOutput))

    else:
       return Response({'message':'some values are missing at person'})
    return Response({'message':'your data is processing from person','data':foodDetails})
  except:
    return Response({'message':'I am at the response page from person'})
  
@api_view(['POST'])
def namaste(request):
  try:
    namaste_serializer = serializer_namaste(data=request.data)
    if namaste_serializer.is_valid():
       print(namaste_serializer.data)
    else:
       return Response({'message':'some values are missing at namaste'})
    return Response({'message':'your data is processing from namaste'})
  except:
    return Response({'message':'I am at the response page from namaste'})