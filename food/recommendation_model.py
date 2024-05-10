import pandas as pd
import numpy as np
import numpy as np
import re
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

df=pd.read_csv('static\\csv\\recipes.csv')

def scaling(dataframe):
    scaler=StandardScaler()
    prep_data=scaler.fit_transform(dataframe.iloc[:,16:17].to_numpy())
    return prep_data,scaler

def nn_predictor(prep_data):
    neigh = NearestNeighbors(metric='cosine',algorithm='brute')
    neigh.fit(prep_data)
    return neigh

def build_pipeline(neigh,scaler,params):
    transformer = FunctionTransformer(neigh.kneighbors,kw_args=params)
    pipeline=Pipeline([('std_scaler',scaler),('NN',transformer)])
    return pipeline

def extract_data(dataframe,ingredients):
    extracted_data=dataframe.copy()
    extracted_data=extract_ingredient_filtered_data(extracted_data,ingredients)
    return extracted_data
    
def extract_ingredient_filtered_data(dataframe,ingredients):
    extracted_data=dataframe.copy()
    regex_string=''.join(map(lambda x:f'(?=.*{x})',ingredients))
    extracted_data=extracted_data[extracted_data['RecipeIngredientParts'].str.contains(regex_string,regex=True,flags=re.IGNORECASE)]
    return extracted_data

def apply_pipeline(pipeline,_input,extracted_data):
    _input=np.array(_input).reshape(1,-1)
    return extracted_data.iloc[pipeline.transform(_input)[0]]

def recommend(dataframe,_input,ingredients=[],params={'n_neighbors':15,'return_distance':False}):
        extracted_data=extract_data(dataframe,ingredients)
        if extracted_data.shape[0]>=params['n_neighbors']:
            prep_data,scaler=scaling(extracted_data)
            neigh=nn_predictor(prep_data)
            pipeline=build_pipeline(neigh,scaler,params)
            return apply_pipeline(pipeline,_input,extracted_data)
        else:
            return None

def extract_quoted_strings(s):
    # Find all the strings inside double quotes
    strings = re.findall(r'"([^"]*)"', s)
    # Join the strings with 'and'
    return strings

def output_recommended_recipes(dataframe):
    if dataframe is not None:
        output=dataframe.copy()
        output=output.to_dict("records")
        for recipe in output:
            recipe['RecipeIngredientParts']=extract_quoted_strings(recipe['RecipeIngredientParts'])
            recipe['RecipeInstructions']=extract_quoted_strings(recipe['RecipeInstructions'])
    else:
        output=None
    return output

import json

class Generator:
    def __init__(self,nutrition_input:list,ingredients:list=[],params:dict={'n_neighbors':5,'return_distance':False}):
        self.nutrition_input=nutrition_input
        self.ingredients=ingredients
        self.params=params

    def set_request(self,nutrition_input:list,ingredients:list,params:dict):
        self.nutrition_input=nutrition_input
        self.ingredients=ingredients
        self.params=params

    def generate(self,):
        request={
            'nutrition_input':self.nutrition_input,
            'ingredients':self.ingredients,
            'params':self.params
        }
        #print(request)
        return request
    

class Recommendation:
    def __init__(self,nutrition_list,nb_recommendations,ingredient_txt):
        self.nutrition_list=nutrition_list
        self.nb_recommendations=nb_recommendations
        self.ingredient_txt=ingredient_txt
        pass
    def generate(self,):
        params={'n_neighbors':self.nb_recommendations,'return_distance':False}
        ingredients=self.ingredient_txt.split(';')
        generator=Generator(self.nutrition_list,ingredients,params)
        recommendations=generator.generate()
        return recommendations




# nutritions_values_list=2000

# nb_recommendations=5
# recommendation=Recommendation(nutritions_values_list,nb_recommendations,'')
# ab=recommendation.generate()
# ab['nutrition_input']

# nutritions_values_list=[2000,60,10,250,500,500,20,20,20]
#nutritions_values_list=2000


def recomm(total_cal=2000,meals=3):
    lis=[]
    nb_recommendations=5
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
        nutritions_values_list=li[i]
        nb_recommendations=5
        # print(li[i])
        recommendation=Recommendation(nutritions_values_list,nb_recommendations,'')
        ab=recommendation.generate()
        recommendation_dataframe=list(recommend(df,ab['nutrition_input'],[''],ab['params'])['Name'])
        lis.append(recommendation_dataframe)
    return lis

# print(recomm(2200,3))
