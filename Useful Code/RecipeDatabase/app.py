import json
from difflib import SequenceMatcher, get_close_matches

with open("recipes.json", "r") as file:
    data = json.load(file)

keys = data.keys()

def get_recipe():
    word = input("What do you want to eat? (enter Q to quit): ").title()

    while word not in data:
        if word.upper() == "Q":
            return "Quit"
        matches = get_close_matches(word, keys)
        if len(matches) > 0:
            print(f"Unknown recipe, did you mean {matches} ? Try again.")
            word = input("What do you want to eat? (enter Q to quit): ").title()
        else:
            return "UnknownRecipe"
    
    return (data[word])

def input_recipe():
    name = input("What's the name of the recipe? : ")

    dic = {}
    dic["Ingredients"] = input("Ingredients (separated by \", \") : ").split(", ")
    dic["Directions"] = input("Directions : ")
    dic["Servings"] = input("Number of servings : ")
    data[name] = dic
    keys = data.keys()

    with open("recipes.json", "w") as file:
        newData = json.dumps(data, indent=4)
        file.write(newData)
    
    print("Recipe succesfully added!")

def mainloop():
    run = True
    while run:
        user = input("Enter \"I\" to input and \"S\" to search a recipe in the database. Press \"Q\" to quit. : ").upper()

        match user:
            case "Q":
                run = False
                continue
            
            case "I":
                input_recipe()
                continue

            case "S":
                output = get_recipe()
                if type(output) != str:
                    ingredients_str = ', '.join(output["Ingredients"])
                    instructions_str = output["Directions"]
                    servings_str = output["Servings"] if output["Servings"] != "" else "Unknown"
                    print(f"\nIngredients : {ingredients_str}\n")
                    print(f"Instructions : {instructions_str}\n")
                    print(f"Number of servings : {servings_str}\n")
                elif output == "UnknownRecipe":
                    print("Recipe unknown, please try again.")
                continue

if __name__ == '__main__':
    mainloop()