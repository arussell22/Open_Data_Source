"""
Recipes from Open Data - Gui Version
Authors: Anthony Russell, Dillon Furey, Wesley Chang, Bryan Beach
Dataset Used: Shuyang Li's Food.com Recipes and Interactions
Required external libaries: kaggle for python 3, tkinter for python 3
"""
import tkinter as tk
import tkinter.scrolledtext as tkst
import kaggle
import zipfile
import os
import csv

"""Gui using tkinter
"""
class recipe_gui(tk.Tk):
    """Initializes and runs the GUI and necessary graphical components
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Find A Recipe!')
        tk.Label(self, text='Add Ingredients to Search for a Recipe').pack()
        tk.Label(self, text='Note: Not adding any ingredients will return all recipes').pack()
        self.e1 = tk.Entry(self)
        self.e1.pack()
        self.ingredients = []

        self.all_ingredients = tk.Label(self)
        self.all_ingredients.pack()

        tk.Button(self, text='Add Ingredient', width=15, command=self.add_ingredient).pack()
        tk.Button(self, text='Find Recipes', width=15, command=self.run).pack()
        tk.Button(self, text='Reset Ingredients', width=15, command=self.reset_ingredients).pack()

        self.frame1 = tk.Frame(
            self,
            bg = '#002C76'
        )
        self.frame1.pack(fill='both', expand='yes')
        self.found_recipes = tkst.ScrolledText(
            master = self.frame1,
            wrap   = tk.WORD,
            width  = 65,
            height = 15
        )
       # self.found_recipes = tk.Label(self, anchor='w', width="65")
        self.found_recipes.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.mainloop()

    """Adds an ingredient to the list of ingredients
    Updates list of ingredients on GUI
    """
    def add_ingredient(self):
        ingredient = self.e1.get()
        if ingredient not in self.ingredients:
         self.ingredients.append(ingredient.lower())
         ingredient_string = ""
         count = 1
         for text in self.ingredients:
            ingredient_string = ingredient_string+str(count)+": "+text+"\n"
            count = count + 1
         self.all_ingredients.configure(text=ingredient_string)
        self.e1.delete(0, 'end')

    """Resets the list of ingredients
    Resets the list of ingredients on GUI
    """
    def reset_ingredients(self):
        self.ingredients = []
        self.all_ingredients.configure(text="")
        self.e1.delete(0, 'end')


    """ Downloads the dataset from kaggle if not present
    :returns: Ordereddict of all recipes
    """
    def download_from_kaggle(self):
        kaggle.api.authenticate()
        if not(os.path.exists(os.getcwd()+'/RAW_recipes.csv')):
            kaggle.api.dataset_download_file('shuyangli94/food-com-recipes-and-user-interactions', "RAW_recipes.csv", force=True, quiet=True)
            with zipfile.ZipFile(os.getcwd()+'/RAW_recipes.csv.zip', 'r') as zip_ref:
                zip_ref.extractall(os.getcwd())
        recipes = csv.DictReader(open(os.getcwd()+'/RAW_recipes.csv'))
        return recipes


    """Parses through the dataset for any recipe that contains the list of ingredients 
    and prints each recipe name (limited to print only 10 currently)

    :param recipes: dataset of recipes
    :type recipes: Ordereddict
    :param list_of_ingredients: ingredients to search for
    :type list_of_ingredients: list
    :return lists of recipes that contain the ingredients, or else 'No Recipes Found'
    """
    def parse_ingredients(self,recipes, list_of_ingredients):
        returned_recipes = []
        #number_of_recipes = 10
        try:
            for recipe in recipes:
                #if (number_of_recipes != 0):
                    if (all(ingredients in recipe['ingredients'] for ingredients in list_of_ingredients )):
                        returned_recipes.append(recipe['name'])
                        #number_of_recipes = number_of_recipes - 1
                #else:
                #    break
        except TypeError as e:
            print(e)
        return returned_recipes if returned_recipes else ['No Recipes Found']

    def run(self):
        recipes = self.download_from_kaggle()
        found_recipes = self.parse_ingredients(recipes, self.ingredients)
        recipe_string = ""
        count = 1
        for text in found_recipes:
            recipe_string = recipe_string+str(count)+": "+text+"\n"
            count = count + 1
        self.found_recipes.delete('1.0', 'end')
        self.found_recipes.update()
        self.found_recipes.insert('insert', recipe_string)

app = recipe_gui()


