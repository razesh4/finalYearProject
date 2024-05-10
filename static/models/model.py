import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow import keras
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.neighbors import NearestNeighbors

df=pd.read_csv('static\\models\\sorted_nepali_food.csv')
model=load_model('static\\models\\food_model.h5')
scaler=StandardScaler()
x_train_scaled=scaler.fit(df.iloc[:,5:15])

def scaling_data(food):
    data=food
    x_scaled=scaler.transform(data)
    return x_scaled

calory=100
FatContent=10
Cholestrol=15
SodiumContent=10
CarbohydrateContent=10
FiberContent=10
ProteinContent=10
CalciumContent=10
PhosphorusContent=10
PotassiumContent=10
food=[calory,FatContent,Cholestrol,SodiumContent,CarbohydrateContent,FiberContent,ProteinContent,CalciumContent,PhosphorusContent,PotassiumContent]

def foods12(dataframe=df,*food):
    li=[]
    food=food
    df=dataframe
    scaled_food=scaling_data(food)
    Food_Name_number=np.argmax(model.predict([scaled_food]))
    food_reccomended_by_ann=df[df['Food_Name_number']==Food_Name_number]
    calory=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['Calorie']
    FatContent=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['FatContent']
    Cholestrol=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['Cholestrol']
    SodiumContent=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['CarbohydrateContent']
    CarbohydrateContent=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['CarbohydrateContent']
    FiberContent=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['FiberContent']
    ProteinContent=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['ProteinContent']
    CalciumContent=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['CalciumContent']
    PhosphorusContent=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['PhosphorusContent']
    PotassiumContent=food_reccomended_by_ann.loc[food_reccomended_by_ann.index[0]]['PotassiumContent']
    nutrients_needed_for_knn=[calory,FatContent,Cholestrol,SodiumContent,CarbohydrateContent,FiberContent,ProteinContent,CalciumContent,PhosphorusContent,PotassiumContent]
    #scaled_food=scaling_data(nutrients_needed_for_knn)
    neigh = NearestNeighbors(n_neighbors=5, radius=0.4)
    neigh.fit(df.iloc[:,5:15])
    food_aray=neigh.kneighbors([nutrients_needed_for_knn],15, return_distance=False)#number_of _reccomendation in place of10 
    for i in range(0,len(food_aray[0])):
        li.append(food_aray[0][i])
    return df.iloc[li,:]   

reccomended_food=foods12(df,food)
print(reccomended_food)
reccomended_food['Food_Name'].sample(5).to_list()

def drinks():
    food=df[df['Calorie']<20].sample(10)
    return food


#py calories only upto 700 times for this function
def reccomended_food(calorie):
    calorie_sorted=df[(df['Calorie']>calorie-30) & (df['Calorie']<calorie+30)].index.to_list()
    index=round(len(calorie_sorted)/2)
    index_number=calorie_sorted[index]
    food=df.iloc[index_number-10:index_number+10].sample(10)
    return food

# for bmi values the out put
calorie=500
reccomended_food(calorie)
# print(drinks())



