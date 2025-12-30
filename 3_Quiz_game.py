from datetime import datetime
import win32com.client
import random
import time

TIME_LIMIT = 15
class Questions:
    def __init__(self, que, opt, ans, money):
        self.que = que
        self.opt = opt
        self.ans = ans          
        self.money = money

class Lifeline:
    def __init__(self):
        self.fifty_fifty = True
        self.skip = True
        self.hint = True

    def available(self):
        avail = []
        if self.fifty_fifty:
            avail.append("fifty-fifty")
        if self.skip:
            avail.append("skip")
        if self.hint:
            avail.append("hint")
        return avail

    def use(self, choice, question):
        if choice == "fifty-fifty" and self.fifty_fifty:
            self.fifty_fifty = False
            correct = question.opt[question.ans - 1]
            wrong = random.choice([o for o in question.opt if o != correct])
            return "50-50", [correct, wrong]

        elif choice == "skip" and self.skip:
            self.skip = False
            return "skip", None

        elif choice == "hint" and self.hint:
            self.hint = False
            return "hint", f"Correct option number is near {question.ans}"

        return "invalid", None

class Levels:
    def __init__(self):
        self.level = {"EASY": [], "MEDIUM": [], "HARD": []}
        self.total_prize = 0
        self.lifeline = Lifeline()   

    def load_questions(self):
        curr_level = None
        with open("Questions.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line in self.level:
                    curr_level = line
                    continue
                if line and curr_level:
                    parts = line.split("|")
                    q = Questions(parts[0], parts[1:5], int(parts[5]), parts[6])
                    self.level[curr_level].append(q)

    def start_quiz(self, level):
        speaker.Speak(f"Starting {level} level")
        print(f"\n🔥 Starting {level} Level 🔥....Be ready..!!!")
        for q in self.level[level]:
            print("\n" + q.que)
            for i, opt in enumerate(q.opt, 1):
                print(f"{i}. {opt}")

            print(f"⏱ You have {TIME_LIMIT} seconds")
            start_time = datetime.now()
            used_5050 = False
            new_options = q.opt
            choice = input("Want to use lifeline or ans the que ?(lifeline/ans): ").lower()
            if choice == "lifeline":
                avail = self.lifeline.available()
                if not avail:
                    print("❌ No lifelines left")
                else:
                    print("Available lifelines:", avail)
                    ll = input("Choose lifeline: ").lower()
                    result, data = self.lifeline.use(ll, q)
                    if result == "50-50":
                        used_5050 = True
                        new_options = data
                        print("50-50 Options:")
                        for i, opt in enumerate(new_options, 1):
                            print(f"{i}. {opt}")
                    elif result == "skip":
                        print("⏭ Question skipped")
                        continue
                    elif result == "hint":
                        print("💡 Hint:", data)
            ans = int(input("Your answer: "))
            end_time = datetime.now()
            time_taken = (end_time - start_time).seconds
            if time_taken > TIME_LIMIT:
                speaker.Speak("Time up! Game over")
                print("⏱ Time exceeded")
                break
            if used_5050:
                chosen = new_options[ans - 1]
                correct = q.opt[q.ans - 1]
                is_correct = chosen == correct
            else:
                is_correct = ans == q.ans
            if is_correct:
                speaker.Speak("Correct answer..!!")
                print("✅ Correct..!! You won", q.money)
                self.total_prize += int(q.money.replace("/-", ""))
            else:
                speaker.Speak("Wrong answer. Game over")
                print("❌ Wrong answer..!!")
                break


speaker = win32com.client.Dispatch("SAPI.SpVoice")
game = Levels()
game.load_questions()
while True:
    name = input("Enter player name: ")
    game.total_prize=0
    game.lifeline = Lifeline()
    current_time = datetime.now()
    print("Date & Time:", current_time)
    level = input("Choose level (EASY/MEDIUM/HARD): ").upper()
    if level in game.level:
        game.start_quiz(level)
        print("\n🏆 Total Prize Won:", game.total_prize)
        speaker.Speak(f"Total prize won is {game.total_prize}")
    else:
        print("Invalid level")
    
    with open('score.txt','a') as file:
            file.write( f"{name} | {level} | {game.total_prize} | {current_time}\n")
    again = input("Another player? (yes/no): ").lower()
    if again != 'yes':
        break
    