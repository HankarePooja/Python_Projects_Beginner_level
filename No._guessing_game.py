import random

a= input("Enter a level (easy,medium,difficult) : ")
if a=='easy':
    r= random.randint(1, 10)
elif(a=='medium'):
    r = random.randint(1,50)
elif(a=='difficult'):
    r = random.randint(1,100)
else:
    print("Invalid level")
    exit()

attempts=1  
while r: 
    user = int(input("Guess the no. 🤔 : "))
    attempts+=1
    if(user>r):
        print("So sorry...!! It's too high...😳")
    elif(user<r):
        print("So sorry...!! It's too low...😔")
    else:
        print("Congratulations....🥳 !! You guessed it right..👏")
        print(f"No. of attempts taken for {a} level: {attempts}")

        play=input("Do u want to play again..? : ")
        if(play=="yes"):
           attempts=0
           r=random.randint(1,10 if a=="easy" else 50 if a=="medium" else 100)
           continue
        else:
            break
    
