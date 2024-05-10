import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow import keras
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.neighbors import NearestNeighbors
import random

class Load_data():
    df=pd.read_csv('static\\models\\sorted_nepali_food.csv')
    df = df.fillna('')
    model=load_model('static\\models\\food_model.h5')
    scaler=StandardScaler()
    x_train_scaled=scaler.fit(df.iloc[:,5:15])
    def __init__(self):
        pass

    #this is for scalling data before feeding into the neural network
    def scaling_data(self,food):
        data=food
        x_scaled=self.scaler.transform(data)
        return x_scaled
    
    def foods12(self,*food):
        li=[]
        food=food
        df = self.df
        scaled_food=self.scaling_data(food)
        Food_Name_number=np.argmax(self.model.predict([scaled_food]))
        food_reccomended_by_ann=df[df['Food_Name_number']==Food_Name_number]
        calorie=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['Calorie']
        FatContent=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['FatContent']
        Cholestrol=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['Cholestrol']
        SodiumContent=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['CarbohydrateContent']
        CarbohydrateContent=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['CarbohydrateContent']
        FiberContent=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['FiberContent']
        ProteinContent=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['ProteinContent']
        CalciumContent=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['CalciumContent']
        PhosphorusContent=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['PhosphorusContent']
        PotassiumContent=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['PotassiumContent']
        nutrients_needed_for_knn=[calorie,FatContent,Cholestrol,SodiumContent,CarbohydrateContent,FiberContent,ProteinContent,CalciumContent,PhosphorusContent,PotassiumContent]
        #scaled_food=scaling_data(nutrients_needed_for_knn)
        neigh = NearestNeighbors(n_neighbors=5, radius=0.4)
        neigh.fit(df.iloc[:,5:15])
        food_aray=neigh.kneighbors([nutrients_needed_for_knn],20, return_distance=False) #number_of _reccomendation in place of10 
        for i in range(0,len(food_aray[0])):
            li.append(food_aray[0][i])
        return df.iloc[li,:]

# Load_data()

calorie=550
FatContent=20
Cholestrol=150
SodiumContent=50
CarbohydrateContent=225
FiberContent=25
ProteinContent=50
CalciumContent=10
PhosphorusContent=10
PotassiumContent=20
food=[calorie,FatContent,Cholestrol,SodiumContent,CarbohydrateContent,FiberContent,ProteinContent,CalciumContent,PhosphorusContent,PotassiumContent]



def nutrient_reccommend(food,meals):
    reccomended_food=Load_data().foods12(food)
    reccomended_food = reccomended_food.sample(meals)
    foodName = reccomended_food['Food_Name'].to_list()
    calorie = reccomended_food['Calorie'].to_list()
    weight = reccomended_food['weight(in gram)'].to_list()
    return[foodName,calorie,weight]

# a = nutrient_reccommend(food,15)
# print(a)


df=pd.read_csv('static\\models\\sorted_nepali_food.csv')
df = df.fillna('')

def drinks():
    food=df[df['Calorie']<20].sample(10)['Food_Name'].to_list()
    return food

def food_reccomended_by_calorie(calorie):
    neigh = NearestNeighbors(n_neighbors=5, radius=0.4)
    neigh.fit(df.iloc[:,5:6])
    food_aray=neigh.kneighbors([[calorie]],30, return_distance=False)#number_of _reccomendation in place of10 
    li=[]
    for i in range(0,len(food_aray[0])):
        li.append(food_aray[0][i])
    return df.iloc[li,:].sample(10)

def food_recommend(total_cal,meals):
    lis=[]
    numnber_of_meals=meals
    total_calories=total_cal

    if numnber_of_meals==3:
        breakfast=0.35*total_calories
        launch=0.40*total_calories
        dinner=0.25*total_calories
        li=[breakfast,launch,dinner]
        
    elif  numnber_of_meals==4:
        breakfast=0.30*total_calories
        brunch=0.05*total_calories
        launch=0.40*total_calories
        dinner=0.25*total_calories
        li=[breakfast,brunch,launch,dinner]
    else:
        breakfast=0.30*total_calories
        brunch=0.05*total_calories
        launch=0.40*total_calories
        snack=0.05*total_calories
        dinner=0.20*total_calories
        li=[breakfast,brunch,launch,snack,dinner]

    for i in range(len(li)):
       food = food_reccomended_by_calorie(li[i]).to_dict()

       lis.append(food)
    return lis