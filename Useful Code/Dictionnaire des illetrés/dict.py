import json
import random as rd

with open("dict.json", "r") as file:
    data = json.load(file)

keys = data.keys()

def get_random_word():
    word = rd.choice(list(keys))
    wordData = data[word]
    print(f"{wordData["date"]}  {wordData["person"]} : {wordData["cword"]} - {wordData["word"]}\n")

def input_word():
    global data
    date = input("Date (NA if none found) : ")
    person = input("Illiterate : ")
    correct_word = input("Correct word : ")
    word = input("Butchered word : ")

    dic = {}
    dic["date"] = date
    dic["person"] = person
    dic["cword"] = correct_word
    dic["word"] = word
    data[correct_word] = dic
    keys = data.keys()
    data = dict(sorted(data.items()))
    with open("dict.json", "w") as file:
        newData = json.dumps(data, indent=4)
        file.write(newData)
    
    print(f"Word succesfully added!\nDictionnary now contains {len(keys)} entries.\n")

def mainloop():
    run = True
    while run:
        user = input("Enter \"I\" to input and \"G\" to get a random word in the database. Press \"Q\" to quit. : ").upper()

        match user:
            case "Q":
                run = False
                continue
            
            case "I":
                input_word()
                continue

            case "G":
                get_random_word()
                continue

if __name__ == '__main__':
    mainloop()