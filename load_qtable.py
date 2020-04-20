f = open("outputs.txt","r")
q = open("qtable.txt", "w")

for line in f:
    if line[:2] == " [" or line[:2] == "[ " or line[:2] == "[[":
        q.write(line) 
