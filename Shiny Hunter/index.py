import random

count = 0

while True:
    chance = random.randint(1, 8192)    

    if chance == 1:
        print("Shiny Snivy Found!")
        break
    else:
        count += 1

print("Number of tries until Shiny Snivy is Found: " + str(count))