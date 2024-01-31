# Example file for LinkedIn Learning Course "Python: Build a Quiz App" by Joe Marini
# QuizManager manages the quiz content
# Minor changes to original code were made to allow for a GUI.
import os.path
import os
import quizparser
import datetime


class QuizManager:
    def __init__(self, quizfolder):
        self.quizfolder = quizfolder
        self.the_quiz = None    
        self.quizzes = dict()
        self.results = None
        self.quiztaker = ""

        if (os.path.exists(quizfolder) == False):
            raise FileNotFoundError("The quiz folder doesn't seem to exist!")
        self._build_quiz_list()

    def _build_quiz_list(self):
        dircontents = os.scandir(self.quizfolder)
        # parse the XML files in the directory
        for i, f in enumerate(dircontents):
            if f.is_file():
                parser = quizparser.QuizParser()
                self.quizzes[i+1] = parser.parse_quiz(f)

    # start the given quiz for the user and return the results
    def take_quiz(self, master, quizID, username, GUI):
        self.quiztaker = username
        self.the_quiz = self.quizzes[quizID]
        self.results = self.the_quiz.take_quiz(master, quizID, username, GUI)
        return(self.results)

    def show_results(self, master, GUI):
        self.the_quiz.show_results(master, GUI, self)

    # save the results of the most recent quiz to a file
    # the file is named using the current date as
    # QuizResults_YYYY_MM_DD_N (N is incremented until unique)
    def save_results(self, master, GUI):
        today = datetime.datetime.now()
        filename = f"QuizResults_{today.year}_{today.month}_{today.day}.txt"
        n = 1
        # if the file name already exists, then add a digit to the end until it's unique
        while(os.path.exists(filename)):
            filename = f"QuizResults_{today.year}_{today.month}_{today.day}_{n}.txt"
            n = n + 1

        with open(filename, "w") as f:
            self.the_quiz.print_results(self.quiztaker, f)

        GUI.saveSuccess(master)        
