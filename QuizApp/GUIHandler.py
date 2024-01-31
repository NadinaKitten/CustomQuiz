# Created based off the pyquiz module created by Joe Marini for the LinkedIn Learning Course "Python: Build a Quiz App"
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from quizmanager import QuizManager
from tkfontchooser import askfont
import os
import json
import sys

settingsToSave = {
        "Name" : "Custom Settings",
        "Style" : {
            "Titles" : {
                "Names" : {
                    "Label" : "Welcome.TLabel",
                    "Button" : "Welcome.TButton"
                },
                "fontSettings" : {
                    "family" : "Courier",
                    "size" : 24,
                    "weight" : "bold",
                    "slant" : "roman",
                    "underline" : 0,
                    "overstrike" : 0
                }
            },
            "Text" : {
                "Names" :{
                    "Label" : "Selection.TLabel",
                    "Button" : "Selection.TButton"
                },
                "fontSettings" : {
                    "family" : "Courier",
                "size" : 18,
                "weight" : "normal",
                "slant" : "roman",
                "underline" : 0,
                "overstrike" : 0
                }
            }
        }
    }

availableSettings = 0

class GUIApp: #TODO allow users to create a quiz within the app, and convert it to XML.
    QUIZ_FOLDER = "Quizzes"

    def __init__(self, master):
        self.style = ttk.Style(master)
        defaults = Settings(master, self)
        defaults.loadDefaultSettings(master, self)
        self.top = None
        self.username = ""
        self.result = None
        self.qm = QuizManager(self.QUIZ_FOLDER)
        master.geometry("640x480+200+200")
        #TODO can use Ctrl+N to open up a new quiz?
        master.state('withdrawn')
        master.option_add("*tearOff", False)
        menubar = Menu(master)
        master.config(menu = menubar)
        #TODO can add more cascading menu options
        menuoptions = ["File_", "Quiz_Options_", "Settings_", "Help_"]
        #TODO command for all menu selections not connected yet
        for m in menuoptions:
            name = str(m)
            name = Menu(menubar)
            menubar.add_cascade(menu = name, label = str(m).strip("_").replace("_", " "))
            if m == "File_":
                name.add_command(label = "Exit", command = lambda:self.closeApp(master), accelerator="Alt + F4")
                master.bind("<Alt-F4>", lambda e:self.closeApp(master))
            elif m == "Quiz_Options_":
                quizList = Menu(name)
                name.add_cascade(menu = quizList, label = "Quizzes Available")
                for k, v in self.qm.quizzes.items():
                    quizList.add_command(label = v.name, command = lambda:self.startQuiz(master, k, v.name, self.username))
                name.add_command(label = "Pause", command = lambda:print("Quiz Paused"), state="disabled")
            elif m == "Settings_":
                name.add_command(label = "Change Text Font", command=lambda:self.changeFont())
                #TODO update when color choosing is added
                name.add_command(label = "Change Window Color", command = lambda:colorchooser.askcolor())
                name.add_command(label = "Change Text Color", command = lambda:colorchooser.askcolor())
        welcome = ttk.Label(master, text = "-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-\n~~~~ Welcome to Custom Quiz! ~~~~~\n-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-",
                            style="Welcome.TLabel")
        welcome.grid(row=0, column=0, rowspan=3, columnspan=10)
        self.userEntry(master)

    def userEntry(self, master):
        self.top=Toplevel()
        self.top.title("Welcome!")
        self.top.geometry(f"320x170+250+140")
        self.top.minsize(320,170)
        self.top.wm_focusmodel("active")

        query = ttk.Label(self.top, style="Selection.TLabel", text="What is your name?") 
        query.grid(row=0, column=0, padx=15, sticky="w")
        name = ttk.Entry(self.top,width=30)
        name.grid(row=1, column=0, padx=40, pady=10, sticky="w")
        errorMessage = ttk.Label(self.top, style="Selection.TLabel", text="At least 1 character is required", foreground="red", wraplength=300)
        name.bind("<Return>", lambda e:self.validateName(master, name, errorMessage))
        ok = ttk.Button(self.top, style="Selection.TButton", text="OK", command=lambda:self.validateName(master, name, errorMessage), width=10)
        ok.grid(row=3, column=0, padx=15, columnspan=3)
        self.top.protocol("WM_DELETE_WINDOW", lambda:self.closeApp(master))   
        master.mainloop()

    def validateName(self, master, name, error):
        if len(name.get()) < 1:
            self.on_invalid(error)
        else:
            self.nameGet(master, name)

    def on_invalid(self, error):
        error.grid(row=2, column = 0, padx=15, sticky="w")
    
    def nameGet(self, master, name):
        user = name.get()
        self.top.destroy()
        master.state("zoomed")
        self.mainMenu(master, user)

    def validateFileName(self, master, name):
        if len(name.get()) < 1:
            
            pass
            
        else:
            if str.isalnum(name.get()) == False:
                #TODO make the text red or something to show the program is working
                pass
                
            else:
                fileName = name.get()
                Settings.saveCustomSettings(Settings, master, fileName)
                self.saveSuccess(master)

    def mainMenu(self, master, user):
        self.username = user
        userLabel = ttk.Label(master, text = f"Hello, {user}!", style="Selection.TLabel")
        userLabel.grid(row=3, column = 0)
        changeName = ttk.Button(master, style="Selection.TButton", text="Change Name", command=lambda:self.userEntry(master))
        changeName.grid(row=3, column=2)
        takeQuiz = ttk.Button(master, text="Take a Quiz", style="Selection.TButton", command=lambda:self.showQuizzes(master))
        takeQuiz.grid(row=5, column=0, ipadx=20, ipady=20)
        options = ttk.Button(master, text="Change Font", style="Selection.TButton", command=lambda:self.changeFont(master))
        options.grid(row=6, column=0, ipadx=20, ipady=20)
        loadSettings = ttk.Button(master, text="Load Custom Settings", style="Selection.TButton", command=lambda:self.loadStyleScreen(master))
        loadSettings.grid(row=7, column=0, ipadx=20, ipady=20)
        master.mainloop()
    
    def showQuizzes(self, master):
        if self.top != None:
            self.top.destroy()
        self.top=Toplevel(master)
        self.top.title("Custom Quiz - Available Quizzes")
        self.top.geometry("800x480+200+200")
        for k, v in self.qm.quizzes.items():
            self.buttonCreate(master, k, v)

    def confirmQuiz(self, master, quizID):
        quizInfo = self.qm.quizzes[quizID]
        self.top.destroy()
        self.top=Toplevel(master)
        self.top.title(f"Custom Quiz: {quizInfo.name}")
        self.current_window_name = f"Custom Quiz: {quizInfo.name}"
        self.top.geometry()
        nameLabel = ttk.Label(self.top, text=quizInfo.name, style="Welcome.TLabel")
        descLabel = ttk.Label(self.top, text=quizInfo.description, style="Selection.TLabel")
        lenLabel = ttk.Label(self.top, text=f"This quiz has {len(quizInfo.questions)} questions.", style="Selection.TLabel")
        totalLabel = ttk.Label(self.top, text=f"There are a total of {quizInfo.total_points} points.", style="Selection.TLabel")
        confirmButton =  ttk.Button(self.top, text="Start Quiz", style="Selection.TButton", command=lambda:self.startQuiz(master, quizID, quizInfo))
        cancelButton = ttk.Button(self.top, text="Choose another quiz", style="Selection.TButton", command=lambda:self.showQuizzes(master))
        nameLabel.grid(row=1, column=0, columnspan=3)
        descLabel.grid(row=2, column=0, columnspan=3)
        lenLabel.grid(row=3, column=0, columnspan=3)
        totalLabel.grid(row=4, column=0, columnspan=3)
        confirmButton.grid(row=5, column=0)
        cancelButton.grid(row=5, column=1)

    def startQuiz(self, master, quizID, quizInfo):
        self.top.destroy()
        master.state("withdrawn")
        results = self.qm.take_quiz(master, quizID, self.username, self)
        self.top = Toplevel(master)
        self.top.geometry()
        resLabel = ttk.Label(self.top, text = f"Results for {self.username}:", style = "Welcome.TLabel")
        resLabel.grid(row=1, column=0, columnspan=2)
        self.qm.show_results(master, self)
                #TODO will need to withdraw the quiz and show a pause window, with a button to continue
                #TODO to made this work properly, will have to change how quiz time is calculated
                #TODO when a quiz is started, need to enable the Pause command

    def quizDone(self, master):
        master.state("zoomed")
        self.top.destroy()

    def saveSuccess(self, master):
        self.top.destroy()
        self.top = Toplevel(master)
        self.top.geometry()
        label = ttk.Label(self.top, text = "Saved Successfully!", style="Selection.TLabel")
        label.grid(row=1, column=0)
        confirm = ttk.Button(self.top, text="OK", style="Selection.TButton", command=lambda:self.quizDone(master))
        confirm.grid(row=2, column=0)

    def buttonCreate(self, master, ID, Info):
        button = ttk.Button(self.top, text=Info.name, style="Selection.TButton", command=lambda:self.confirmQuiz(master, ID))
        label = ttk.Label(self.top, text=Info.description, style="Selection.TLabel")
        button.grid(row=ID, column=0)
        label.grid(row=ID, column = 1)

    def quizButtonCreate(self, master, ID, Info, question, quiz):
        useRow = int(ID) + 1
        button = ttk.Button(self.top, text=Info, style="Selection.TButton", command=lambda:question.checkAnswer(master, ID, self, quiz))
        button.grid(row=useRow, column=0)

    def TFAsk(self, master, question, quiz):
        self.top=Toplevel(master)
        title = self.current_window_name
        self.top.title(title)
        self.top.geometry()
        questionLabel = ttk.Label(self.top, text=f"True or false: {question.text}?", style="Welcome.TLabel")
        questionLabel.grid(row=1, column=0)
        trueButton = ttk.Button(self.top, text="True", style="Selection.TButton", command=lambda:question.checkAnswer(master, "t", self, quiz))
        trueButton.grid(row=2, column=0)
        falseButton = ttk.Button(self.top, text="False", style="Selection.TButton", command=lambda:question.checkAnswer(master, "f", self, quiz))
        falseButton.grid(row=2, column=2)
        master.update()
        return "done"

    def MCAsk(self, master, question, quiz):
        self.top=Toplevel(master)
        title = self.current_window_name
        self.top.title(title)
        self.top.geometry()
        questionLabel = ttk.Label(self.top, text=question.text, style="Welcome.TLabel")
        questionLabel.grid(row=1, column=0)
        for a in question.answers:
            self.quizButtonCreate(master, a.name, a.text, question, quiz)
        master.update()
        return "done"

    def buttonClick(self, master):
        self.top.destroy()
        return
       
    def retakeQuiz(self, master, quiz):
        response = ""
        self.top = Toplevel(master)
        title = self.current_window_name
        self.top.title(title)
        self.top.geometry()
        label = ttk.Label(self.top, text = "It looks like you missed some questions.  Re-do the wrong ones?", style="Welcome.TLabel")
        label.grid(row=1, column = 0, columnspan=2)
        yesButton = ttk.Button(self.top, text = "Yes", style = "Selection.TButton", command = lambda:quiz.updateLoop("y", master, self))
        yesButton.grid(row=2, column=0)
        noButton = ttk.Button(self.top, text = "No", style = "Selection.TButton", command = lambda:quiz.updateLoop("n", master, self))
        noButton.grid(row=2, column=1)
        return "done"
    
    def exitQuiz(self, master):
        #TODO create a button to allow exiting a quiz without finishing
        pass

    def changeFont(self, master):
        #TODO Label and buttons aren't centered - fix it later
        self.top = Toplevel()
        self.top.lift(master)
        self.top.title("Font Selector")
        self.top.geometry(f"600x150+250+250")
        query = ttk.Label(self.top, text="Which font would you like to change?", style="Selection.TLabel")
        query.grid(row=0, column=0, padx=15, rowspan=2)
        titleChange = ttk.Button(self.top, text="The titles and questions", style="Welcome.TButton", command=lambda:self.changeLabel(master, "Welcome.TLabel", "Welcome.TButton"))
        titleChange.grid(row=2, column=0)
        buttonChange = ttk.Button(self.top, text="Other text and answers",style= "Selection.TButton", command=lambda:self.changeLabel(master, "Selection.TLabel", "Selection.TButton"))
        buttonChange.grid(row=3, column=0)

    def changeLabel(self, master, styleLabel, styleButton):
        self.top.withdraw()
        newFont = askfont(master)
        if newFont:
            newFont["family"] = newFont["family"].replace(" ", "\ ")
            newFont_str = "%(family)s %(size)i %(weight)s %(slant)s" % newFont
            if newFont["underline"]:
                newFont_str += " underline"
            if newFont["overstrike"]:
                newFont_str += " overstrike"
            
            self.top = Toplevel(master)
            self.top.title("Confirmation")
            self.top.geometry("600x150+250+250")
            confirmation = ttk.Label(self.top, text="Is this what you wanted?", font=(newFont_str), wraplength=600)
            confirmation.grid(row=1, column=0, columnspan=2)
            change = ttk.Button(self.top, style="Selection.TButton", text="Yes, looks good", command=lambda:self.changeStyles(master, styleLabel, styleButton, newFont_str, newFont))
            change.grid(row=2, column=0)
            cancel = ttk.Button(self.top, style="Selection.TButton", text= "No thanks", command=lambda:self.top.destroy())
            cancel.grid(row=2, column=1)

    def changeColor():
        #TODO create a window, showing users which areas they can change
        pass

    def colorUpdate():
        pass

    def changeStyles(self, master, label, button, newFont_str, newFont):
        Settings.setCustomSettings(Settings, master, newFont, label)
        if label == "Welcome.TLabel":
            self.style.configure(label, font=(newFont_str))
            self.style.configure(button, font=(newFont_str))
        elif label == "Selection.TLabel":
            self.style.configure(label, font=(newFont_str))
            self.style.configure(button, font=(newFont_str))
        master.update()
        self.top.destroy()
        self.top = Toplevel(master)
        self.top.title("Save new settings?")
        self.top.geometry("500x150+250+250")
        confirmation = ttk.Label(self.top, text="Save your custom font settings?", style="Selection.TLabel")
        confirmation.grid(row=1, column=0, columnspan=2)
        save= ttk.Button(self.top, style= "Selection.TButton", text="Yes", command=lambda:self.saveStyleSettings(master, newFont, label)) 
        save.grid(row=2, column=0)
        cancel = ttk.Button(self.top, style="Selection.TButton", text= "Not now", command = lambda:self.top.destroy())
        cancel.grid(row=2, column=1)
    
    def saveStyleSettings(self, master, font, label):
        self.top.destroy()
        self.top = Toplevel(master)
        self.top.title = "File Name Selection"
        self.top.geometry()
        label = ttk.Label(self.top, text="What would you like to name these settings?", style="Selection.TLabel")
        label.grid(row=1, column=0)
        fileName = ttk.Entry(self.top, width=30,)
        fileName.grid(row=2, column=0, padx=20, pady=10)
        note = ttk.Label(self.top, style="Selection.TLabel", text="File names must be at least 1 character long and contain only alphanumeric characters.")
        note.grid(row=3, column=0)
        fileName.bind("<Return>", lambda e:self.validateFileName(master, fileName))
        ok = ttk.Button(self.top, style="Selection.TButton", text="OK", command=lambda:self.validateFileName(master, fileName), width=10)
        ok.grid(row=4, column=0, padx=15, columnspan=3)
        master.mainloop()

    def loadStyleScreen(self, master):
        self.top=Toplevel(master)
        self.top.title = "Custom Settings Selection"
        self.top.geometry()
        global availableSettings
        while availableSettings > 0:
            self.styleButtonCreate(master, availableSettings)
            availableSettings -= 1
            continue
        
    def styleButtonCreate(self, master, ID):
        button = ttk.Button(self.top, text = Settings.customSettings[ID]["Name"], style="Selection.TButton", command=lambda:Settings.loadCustomSettings(Settings, master, ID, self))
        button.grid(row=ID, column=0)

    def closeApp(self, master):
        master.quit()
        -quit()


#TODO other custom settings for labels - relief, borderwidth.  Colors include foreground (text) and background 
class Settings:
    settingsFolder = "CustomSettings"
    customSettings = dict()

    def __init__(self, master, GUI):
        self.loadDefaultSettings(master, GUI)
        self.folder = self.settingsFolder
        if (os.path.exists(self.settingsFolder) == False):
            raise FileNotFoundError("The settings folder doesn't seem to exist!")
        self._build_custom_settings_list()
    
    def _build_custom_settings_list(self):
        dircontents = os.scandir(self.settingsFolder)
        for i, f in enumerate(dircontents):
            if f.is_file():
                #TODO need to parse these for this to work!
                with open(f) as json_file:
                    self.customSettings[i+1] = json.load(json_file)
                    global availableSettings
                    availableSettings += 1
        #availableSettings = i
        
    def setCustomSettings(self, master, font, label):
        if label == "Welcome.TLabel":
            settingsToSave["Style"]["Titles"]["fontSettings"]=font
        elif label == "Selection.TLabel":
            settingsToSave["Style"]["Text"]["fontSettings"]=font
            
    #TODO allow users to delete custom settings?
            #TODO Also, instead of making a new file, ask to overwrite?  Or look up how to us os.path to open a system dialogue.
    def saveCustomSettings(self, master, file):
        fileName = f"{file}.json"
        settingsToSave["Name"] = file
        json_string = json.dumps(settingsToSave)
        n = 1
        os.chdir("CustomSettings")
        while(os.path.exists(fileName)):
            fileName = f"{file}({n}).json"
            n = n + 1
        with open(fileName, "w") as f:
            print(json_string, file=f, flush=True)
        return

    def loadCustomSettings(self, master, ID, GUI): #TODO will need to add color settings also
        setting = self.customSettings[ID]
        defaultStyle = setting["Style"]
        defaultTitles = defaultStyle["Titles"]["Names"]
        defaultTitleFont = defaultStyle["Titles"]["fontSettings"]
        defaultTitleString = (defaultTitleFont["family"], defaultTitleFont["size"], defaultTitleFont["weight"], defaultTitleFont["slant"])
        if defaultTitleFont["underline"] == 1:
            defaultTitleString += " underline"
        if defaultTitleFont["overstrike"] == 1:
            defaultTitleString += "overstrike"
            
        defaultText = defaultStyle["Text"]["Names"]
        defaultTextFont = defaultStyle["Text"]["fontSettings"]
        defaultTextString = (defaultTextFont["family"],defaultTextFont["size"], defaultTextFont["weight"], defaultTextFont["slant"])
        if defaultTextFont["underline"] == 1:
            defaultTitleString += " underline"
        if defaultTextFont["overstrike"] == 1:
            defaultTitleString += "overstrike"

        GUI.style.configure(defaultTitles["Label"], font= (defaultTitleString))
        GUI.style.configure(defaultTitles["Button"], font=(defaultTitleString))
        GUI.style.configure(defaultText["Label"], font=(defaultTextString))
        GUI.style.configure(defaultText["Button"], font=(defaultTextString))

        #TODO add color options to json file and set up in Settings Class
        master.update()
        
    def loadDefaultSettings(self, master, GUI):
        titleDefaults = "Courier 24 bold roman"
        textDefaults = "Courier 18 normal roman"
        GUI.style.configure("Welcome.TLabel", font=(titleDefaults))
        GUI.style.configure("Welcome.TButton", font=(titleDefaults))
        GUI.style.configure("Selection.TLabel", font=(textDefaults))
        GUI.style.configure("Selection.TButton", font=(textDefaults))
        master.update()
    
if __name__ == "__main__":
    root = Tk() 
    root.title("Custom Quiz")
    root.minsize(640,480)
    app = GUIApp(root)
