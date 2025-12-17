from datetime import datetime, timedelta
import win32com.client
import threading
import time
import pythoncom

print("~~~~~~~~~~~~~~~~~~~~~~~ TO DO LIST ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ")
task=[]
try:
    with open('myfile.txt' , "r")as file:
        for line in file :
            task.append(line.strip())
except FileNotFoundError:
    pass
def menu():
    while True : 
        user =  input("Enter a choice (Add,View,delete,clear,exit)🤔 : ").lower()
        # if(user=='add'):
        #     add=input("Enter task to add in list : ")
        #     user_input = input("Enter date & time (YYYY-MM-DD HH:MM:SS): ")
        #     task.append(add+"  "+"|"+"  "+user_input+"  "+"|"+"  "+"Pending")
        #     with open("myfile.txt" , "w",encoding='utf-8') as file :
        #         for t in task:
        #             file.write(t + "\n")
        #     print(f"{add}  Task added successfully...!!👏 ")
        #     print("***********************************************************")
        if user == "add":
            add = input("Enter task to add in list : ")
            user_input = input("Enter date & time (YYYY-MM-DD HH:MM:SS): ")

            try:
                task_time = datetime.strptime(user_input, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print("❌ Invalid date format")
                continue

            if task_time < datetime.now() + timedelta(seconds=5):
                print("❌ Time must be in the future")
                continue

            task.append(f"{add} | {user_input} | Pending")

            with open("myfile.txt", "w", encoding="utf-8") as file:
                for t in task:
                    file.write(t + "\n")

            schedule_reminder(add, task_time)
            print(f"{add} task added successfully 👏")

        elif(user=='view'):
            if(len(task)==0):
                print("Tasks are not available.....😔")
            else:
                print(f"List of Tasks are given below : ")
                for i, t in enumerate(task,start=1):
                    print(f"{i}: {t}")
            print("**************************************************************")

        elif(user == 'delete'):
            if len(task) == 0:
                print("Tasks are not available to delete.....😔")
            else:
                for i, t in enumerate(task, start=1):
                    print(f"{i}: {t}")
                num = int(input("Enter task number to delete: "))
                if num < 1 or num > len(task):
                    print("Invalid task number....😔")
                else:
                    removed = task.pop(num - 1)
                    with open('myfile.txt',"w") as file :
                        for t in task:
                            file.write(t +"\n")
                    print(f"The task '{removed}' is deleted successfully...👏")
            print("**************************************************************")   

        elif(user=='clear'):
            if len(task) == 0:
                print("Tasks are not available to clear.....😔")
            else:
                clr = input(("Do u want to clear all tasks ?(Yes/No)🤔:  "))
                if(clr=='Yes'):
                    task.clear()
                    with open('myfile.txt', 'w') as file:
                        pass
                    print("Cleared all tasks successfully...!!!👏")
                else:
                    continue
            print("******************************************************************")
        
        elif(user=='exit'):
            print("Goodbye..👋!! Have a nice day....😊")         
            break

# def reminder():
#     pythoncom.CoInitialize() 
#     speaker  =  win32com.client.Dispatch("SAPI.SpVoice")
#     while True:
#         try:
#             with open ('myfile.txt','r',encoding='utf-8') as file:
#                 lines = file.readlines()
#         except FileNotFoundError:
#             time.sleep(10)
#             continue
#         updated_lines=[]
#         for line in lines:
#             parts= line.strip().split("|")
#             if(len(parts)!=3):
#                updated_lines.append(line)
#                continue
#             task_name,dt_str,status=[p.strip() for p in parts]
#             try:
#                 task_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
#             except ValueError:
#                 task_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
#             now = datetime.now()
#             if now >= task_time and status == "Pending":
#                 speaker.Speak(f"It's time to {task_name}")
#                 updated_lines.append(f"{task_name} | {dt_str} | Notified\n")
#             else:
#                 updated_lines.append(line)

#         with open("myfile.txt", "w", encoding="utf-8") as file:
#             file.writelines(updated_lines)

#         time.sleep(5)

# t1 = threading.Thread(target=reminder, daemon=True)
# t1.start()
def schedule_reminder(task_name, task_time):
    def remind():
        pythoncom.CoInitialize()
        speaker = win32com.client.Dispatch("SAPI.SpVoice")

        wait_seconds = (task_time - datetime.now()).total_seconds()
        if wait_seconds <= 0:
            return  # never remind past tasks

        time.sleep(wait_seconds)
        speaker.Speak(f"It's time to {task_name}")

        # update file after notification
        with open("myfile.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        updated = []
        for line in lines:
            if line.startswith(task_name) and "Pending" in line:
                updated.append(line.replace("Pending", "Notified"))
            else:
                updated.append(line)

        with open("myfile.txt", "w", encoding="utf-8") as f:
            f.writelines(updated)

    threading.Thread(target=remind, daemon=True).start()

menu()

            