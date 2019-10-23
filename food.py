"""
Recipes from Open Data - Command Line Version
Authors: Anthony Russell, Dillon Furey, Wesley Chang, Bryan Beach
Dataset Used: Shuyang Li's Food.com Recipes and Interactions
Required external libaries: kaggle for python 3
"""
#import kaggle
import zipfile
import os
import csv

""" Downloads the dataset from kaggle if not present
:returns: Ordereddict of all recipes
"""
def download_from_kaggle():
#    kaggle.api.authenticate()
    if not(os.path.exists(os.getcwd()+'/RAW_recipes.csv')):
#        kaggle.api.dataset_download_file('shuyangli94/food-com-recipes-and-user-interactions', "RAW_recipes.csv", force=True, quiet=True)
        with zipfile.ZipFile(os.getcwd()+'/RAW_recipes.csv.zip', 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())
    recipes = csv.DictReader(open(os.getcwd()+'/RAW_recipes.csv'))
    return recipes


def get_ingredients():
    print("Enter in a list of ingredients to search for. \n"+
    "Separate ingredients with a comma without spaces. "+
    "\nFor example: chicken,rice,peppers")
    list_of_ingredients = input().split(',')
    return list_of_ingredients


"""Parses through the dataset for any recipe that contains the list of ingredients 
and prints each recipe name (limited to print only 10 currently)

:param recipes: dataset of recipes
:type recipes: Ordereddict
:param list_of_ingredients: ingredients to search for
:type list_of_ingredients: list
"""
def parse_ingredients(recipes, list_of_ingredients):
    returned_recipes = []
    number_of_recipes = 10
    try:
        for recipe in recipes:
            if (number_of_recipes != 0):
                if (all(ingredients in recipe['ingredients'] for ingredients in list_of_ingredients )):
                    returned_recipes.append(recipe['name'])
                    number_of_recipes = number_of_recipes - 1
            else:
                break
    except TypeError as e:
        print(e)
    return returned_recipes if returned_recipes else ['No Recipes Found']


"""Main method, calls all necessary methods

"""
def main():
    recipes = download_from_kaggle()
    ingredients = get_ingredients()
    print(parse_ingredients(recipes, ingredients))

def run(list_of_ingredients):
    recipes = download_from_kaggle()
    return parse_ingredients(recipes, list_of_ingredients)


main()