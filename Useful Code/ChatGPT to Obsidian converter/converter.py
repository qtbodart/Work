def countSpaces(line):
    i = 0
    while line[i] == " ":
        i+=1
    return i

with open("input.txt","r") as input:
    with open("C:\\Users\\quent\\Documents\\Git\\Obsidian\\ChatGPT buffer.md","w") as output:
        space = 0

        for line in input.readlines():
            if "\[" in line:
                space = 1
                continue
            if space == 1:
                if line[-1] == "\n":
                    output.write(countSpaces(line)*" "+"$"+line.strip(" ")[:-1]+"$\n")
                else:
                    output.write(countSpaces(line)*" "+"$"+line.strip(" ")[:-1]+"$")
                space = 2
                continue
            if space == 2:
                space = 0
                continue
            else:
                output.write(line.replace("\( ", "$").replace("\(", "$").replace(" \)", "$").replace("\)", "$"))

with open("input.txt", "w"):
    pass