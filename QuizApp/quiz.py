# Example file for LinkedIn Learning Course "Python: Build a Quiz App" by Joe Marini
# The Quiz and Question classes define a particular quiz
# Some changes were made to original code to allow GUI with TKinter.
import datetime
import sys
import random
from tkinter import *
from tkinter import ttk

class Quiz:

    loopBlock = True
    retake = ""

    def __init__(self):
        self.name = ""
        self.description = ""
        self.questions = []
        self.score = 0
        self.correct_count = 0
        self.total_points = 0
        self.completion_time = 0

    def updateLoop(self, ans, master, GUI):
        self.retake = ans
        self.loopBlock = False
        GUI.buttonClick(master)

    def show_results(self, master, GUI, manager):
        dateLabel = ttk.Label(GUI.top, text=f"Taken today, {datetime.datetime.today()} in {self.completion_time} seconds,", style = "Selection.TLabel")
        dateLabel.grid(row=2, column=0, columnspan=2)
        scoreLabel = ttk.Label(GUI.top, text= f"{self.correct_count} out of {len(self.questions)} questions correct, scoring {self.score} out of {self.total_points} points!", style="Selection.TLabel")
        scoreLabel.grid(row=3, column=0, columnspan=2)
        saveAsk = ttk.Label(GUI.top, text = "Would you like to save your results?", style = "Selection.TLabel")
        saveAsk.grid(row=4, column=0, columnspan=2)
        yesButton = ttk.Button(GUI.top, text = "Yes", style="Selection.TButton", command=lambda:manager.save_results(master, GUI))
        yesButton.grid(row=5, column=0)
        noButton = ttk.Button(GUI.top, text = "No", style = "Selection.TButton", command=lambda:GUI.quizDone(master))
        noButton.grid(row=5, column=1)
            
    def print_results(self, quiztaker, thefile=sys.stdout):
        print("*******************************************",
              file=thefile, flush=True)
        print(f"RESULTS for {quiztaker}", file=thefile, flush=True)
        print(f"Date: {datetime.datetime.today()}", file=thefile, flush=True)
        print(f"ELAPSED TIME: {self.completion_time}", file=thefile, flush=True)
        print(
            f"QUESTIONS: {self.correct_count} out of {len(self.questions)} correct", file=thefile, flush=True)
        print(f"SCORE: {self.score} points of possible {self.total_points}",
              file=thefile, flush=True)
        print("*******************************************\n",
              file=thefile, flush=True)

    def take_quiz(self, master, quizID, user, GUI):
        # initialize the quiz state
        self.score = 0
        self.correct_count = 0
        self.completion_time = 0
        for q in self.questions:
            q.is_correct = False
        # randomize the questions TODO add an option in quizoptions to turn this off
        random.shuffle(self.questions)
        # record the start time of the quiz
        starttime = datetime.datetime.now()
        # execute each question and record the result
        for q in self.questions:
            q.ask(master, GUI, self)
        # record the end time of the quiz
        endtime = datetime.datetime.now()
        #print("quiz done!")
        if self.correct_count != len(self.questions): #TODO fix this for TKinter
            response = GUI.retakeQuiz(master, self)
            print(response, self.retake)
            self.loopBlock = True
            while response == "done":
                if self.loopBlock == True:
                    master.update()
                    continue   
                else:
                    break
            print (self.retake)
            if self.retake == "y":
                print("Got to self.retake!")
                wrong_qs = [q for q in self.questions if q.is_correct == False]
                for q in wrong_qs:
                    print("got to asking again!")
                    q.ask(master, GUI, self)
                endtime = datetime.datetime.now()
        self.completion_time = endtime - starttime #TODO this needs changed to allow for pause time
        self.completion_time = datetime.timedelta(seconds=round(self.completion_time.total_seconds()))
        # return the results
        return (self.score, self.correct_count, self.total_points)

class Question:
    loopBlock = True

    def __init__(self):
        self.points = 0
        self.correct_answer = ""
        self.text = ""
        self.is_correct = False
    
    def checkAnswer(self, master, ans, gui, quiz):
        response = ans
        if response[0] == self.correct_answer:
            self.is_correct = True
            quiz.correct_count += 1
            print(quiz.correct_count)
            quiz.score += self.points 
        self.loopBlock = False
        gui.buttonClick(master)
        
class QuestionTF(Question):
    def __init__(self):
        super().__init__()

    def ask(self, master, GUI, quiz):
        if (True): 
            tf = GUI.TFAsk(master, self, quiz)
            self.loopBlock = True
            while tf == "done":
                if self.loopBlock == True:
                    master.update()
                    continue   
                else:
                    break
            return

class QuestioncMC(Question):
    def __init__(self):
        super().__init__()
        self.answers = []

    def ask(self, master, GUI, quiz):
        if (True):
            mc = GUI.MCAsk(master, self, quiz)
            self.loopBlock = True
            while mc == "done":
                if self.loopBlock == True:
                    master.update()
                    continue   
                else:
                    break   
            return

class Answer:
    def __init__(self):
        self.text = ""
        self.name = ""
