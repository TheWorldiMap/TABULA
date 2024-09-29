##########################################################################################
#                                                                                        #
#                                   MIT License                                          #
#                                                                                        #
#                         Copyright (c) 2024 TheWorldiMap                                #
#                                                                                        #
#    Permission is hereby granted, free of charge, to any person obtaining a copy        #
#    of this software and associated documentation files (the "Software"), to deal       #
#    in the Software without restriction, including without limitation the rights        #
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell           #
#    copies of the Software, and to permit persons to whom the Software is               #
#    furnished to do so, subject to the following conditions:                            #
#                                                                                        #                              
##########################################################################################
#                     TheWorldiMap                                     Daave             #
##########################################################################################
#              :#++:                                                                     #
#               -%%#%*:                   :-=+*+++**-                                    #
#                 +@**#%=            .-*#%###***#%#+.                                    #
#                  :%#**#%: :=====-+#%#******#%#=                                        #
#                    ##**#%%#***#@#******##*=.                                           #
#                    :@%**%%***%%****#%%%@#.                                             #
#                  :#@##%**%%#@#**#%@%****%@+                                            #
#                 +@%#%%#%#*@%#*%#+=+#%%#**#@+                            ..::-:::::.    #
#                %@@#+--::=*@@%*-::::::-+@#*#@*                      .:::::::-==-:-===   #
#               %@*-::::-**:-#+::::::::=@%***#@+   :-*#.            .--::::-::------:    #
#               @%-::::::+***##+*-::::=@#*****#@%%%%#%@           :::--:---:::---::      #
#               .%%-::*#*##**%%##::::=@#*************@=         .:-::-----::--:::.       #
#  *###****+**##%%%=::-*#%**@#*=:::::+*####%#%%%%#**#@       .:::::---:::::::::.         #
#  *@=-======----:::::::-%#%*::::::::::::::::::-@%**@=     .:::::::::------::.           #
#  -@+:::::::::::::::::::-%%-::::::::::::::::::=@**#%    .:::::::::::--::.               #
#  .@#:::::::::::::::::::::-:::::::::::::::::::%%*#%.  .::::::::::::::::.                #
#   +@=:::::::::::::::::::::::::::::::::::::::#@*#%   :::::::::::::-::::.                #
#    #@=::::::::::::::::::::::::::::::::::::-#@#%+  .:::::::::::::=:--:::                #
#     @%-::::::::::::::::::::::::::::::::::=@@%*. .::::::::::::::-=::-:::                #
#     .*@*-::::::::::::::::::::::::::::::-#@@+.  .::::::::::::::-=:.  :::                #
#       .*@#+-::::::::::::::::::::::::-+#@#-    :::::::::::::::==:    .:::               #
#          =#@#+-:::::::::::::::-=*#%@#=:     .::::::::::::::--:.      ..:::..           #
#             -+#%%##******#####*+=-:     .::::::::::::::::---:                          #
#                  .:::---:.             .::::::::::::::---::                            #
#                                        ::::::::::::---::.                              #
#                                       .:::::::::::---.                                 #
#                                      ::::::::::::::::::.                               #
#                                    .::::::::::::::::::::::                             #
#                                   ::::::::::.     ...:::::.                            #
#                                 .:::::::::.         .:::::. .                          #
#                                ::::::::::          .:::::::......                      #
#                               :::::::::.                                               #
#                             .::::::::.                                                 #
# ########################################################################################

# i learned a valuable lesson with this project.... TKINTER SUCKS ASS.
# its old and half functional and missing core features 
# the documentation is kinda raw and spread across like 3 sites 
# and everything good ive done was a worka round for crap things 
# like the stringvar and listboxes and its just damn raw
# i had no idea about this when i started cause i have never even coded a gui before 
# or even coded something from nothing but i now know this sucks 

###########################################################################################

import tkinter
import shutil 
import pickle
import os
import datetime
import sv_ttk

from datetime import datetime
from tkinter import *
from tkinter import ttk
import tkinter.dialog
import tkinter.filedialog
 
class GLOBAL_VARS: ## Data that everything touches
    
    GameEntriesList = [] ## part of the next system to have seperated folders for each game       
    SourceEntriesList = [] ## list as displayed in the GOOEY (this is messy af and needs to be STOPPED)
    EntriesDictList = []  ## Workhorse Data stucture should be an easy JSON when i lean that
    FormattedEntriesDictList = [] ## workhorse part 2
    BackedUpFiles = [] ## list path to files fully backed up for listing in loading
    BackedUpPaths = [] ## list paths created to store files for listing  in loading

    Today = datetime.today().strftime('%Y-%m-%d')

class LIST_MANAGER: ## Manages all the Lists functions
    
    #def TreeViewInsertList(List, TargetTreeView):
        #print(List, TargetTreeView)
        #for item in List:
            #TargetTreeView.insert('', 'end', text=item)
            
    def ListValues(InputDict, InputKey): ## list realisation function 
        OutputValues = [Key[InputKey] for Key in InputDict]
        return OutputValues
        
    
    def FormatEntries():
        list_games = LIST_MANAGER.ListValues(GLOBAL_VARS.EntriesDictList, ("Game"))
        list_source_files = LIST_MANAGER.ListValues(GLOBAL_VARS.EntriesDictList, ("Source File"))
        list_source_paths = LIST_MANAGER.ListValues(GLOBAL_VARS.EntriesDictList, ("Source Path"))
        list_destination_paths = LIST_MANAGER.ListValues(GLOBAL_VARS.EntriesDictList, ("Destination Path"))

        for Game, SourceFile, SourcePath, DestinationPath in zip(list_games, list_source_files, list_source_paths, list_destination_paths):
            full_source = (SourcePath + "\\" + SourceFile)
            full_destination = (DestinationPath + "\\" + Game + "\\" + GLOBAL_VARS.Today + "\\" + SourceFile)
            destination_path = (DestinationPath + "\\" + Game + "\\" + GLOBAL_VARS.Today + "\\")
    
            formatted_entry = {
        "Full Source" : full_source,
        "Full Destination" : full_destination,
        "Destination Path" : destination_path
        }
            GLOBAL_VARS.FormattedEntriesDictList.append(formatted_entry)
    
    def UpdateLists():
        TABULA_GUI.GameNameListVar.set(GLOBAL_VARS.GameEntriesList)
        TABULA_GUI.SaveFileListVar.set(GLOBAL_VARS.SourceEntriesList)
    
    def SaveToList(): ## i could do this better if i knew what i was doing when i started it... -- fixed it a bit but also MAKE THIS A CLASS 
        game_entered = TABULA_GUI.GameEntered.get()
        source_entered = TABULA_GUI.SourcePathEntered.get()
        destination_entered = TABULA_GUI.DestinationPathEntered.get() 
        source_file = os.path.basename(source_entered)
        source_path = os.path.dirname(source_entered)
        entires_dict = {
            "Game" : game_entered,
            "Source File" : source_file,
            "Source Path" : source_path, 
            "Destination Path" : destination_entered,
        }
        GLOBAL_VARS.EntriesDictList.append(entires_dict)
        GLOBAL_VARS.SourceEntriesList.append(source_entered)
        GLOBAL_VARS.GameEntriesList.append(game_entered)
        LIST_MANAGER.UpdateLists()
        DATA_SAVER.SaveList()

    def EnableListButton(*args):
        TABULA_GUI.RemoveListButton.configure(state=ACTIVE)
    def RemoveFromList(): ## this is awful and im sure there is a nicer way to do it BUT IT JUST WORKS
        SelectedIndex = TABULA_GUI.SaveListBox.curselection()
        list(SelectedIndex)
        del GLOBAL_VARS.SourceEntriesList[SelectedIndex[0]]
        del GLOBAL_VARS.GameEntriesList[SelectedIndex[0]]
        TABULA_GUI.SaveListBox.delete([SelectedIndex[0]])
        TABULA_GUI.GameNameBox.delete([SelectedIndex[0]])
        GLOBAL_VARS.EntriesDictList.pop(SelectedIndex[0])
        TABULA_GUI.RemoveListButton.configure(state=DISABLED)
        LIST_MANAGER.UpdateLists()
        DATA_SAVER.SaveList()

    def SourceFileEntryBrowse():
        source_path_entered = tkinter.filedialog.askopenfilename()
        TABULA_GUI.SourcePathEntry.delete(0, END)
        TABULA_GUI.SourcePathEntry.insert(1, source_path_entered)

    def DestinationPathEntryBrowse():
        destination_path_entered = tkinter.filedialog.askdirectory()
        TABULA_GUI.DestinationPathEntry.delete(0, END)
        TABULA_GUI.DestinationPathEntry.insert(1, destination_path_entered)

class BACKUP_AND_LOAD:
            
    def BackupSaves(): ## this looks kinda raw to my eyes but i am actually proud of how simple this is
        LIST_MANAGER.FormatEntries()
        list_full_sources = [FullSource["Full Source"] for FullSource in GLOBAL_VARS.FormattedEntriesDictList]
        list_full_destinations = [FullDestination["Full Destination"] for FullDestination in GLOBAL_VARS.FormattedEntriesDictList]
        list_destination_paths = [DestinationPath["Destination Path"] for DestinationPath in GLOBAL_VARS.FormattedEntriesDictList]
        
        for FullDestination, FullSource, DestinationPath in zip(list_full_destinations, list_full_sources, list_destination_paths):
            if not os.path.exists(DestinationPath):
                os.makedirs(DestinationPath)
                shutil.copy(FullSource, FullDestination)
                GLOBAL_VARS.BackedUpFiles.append(FullDestination)
                GLOBAL_VARS.BackedUpPaths.append(DestinationPath)
            else:
                shutil.copy(FullSource, FullDestination)
                GLOBAL_VARS.BackedUpFiles.append(FullDestination)
                GLOBAL_VARS.BackedUpPaths.append(DestinationPath)
    
class DATA_SAVER: ## Saves Backup lists and other things to a dat
    
    def SaveList():
        with open("BackupsList.dat", "wb") as Data:
            pickle.dump(GLOBAL_VARS.EntriesDictList, Data)
            print("saved", GLOBAL_VARS.EntriesDictList)
            pickle.dump(GLOBAL_VARS.SourceEntriesList, Data)
            pickle.dump(GLOBAL_VARS.GameEntriesList, Data)
            pickle.dump(GLOBAL_VARS.FormattedEntriesDictList, Data)
        
    def LoadList():
            with open("BackupsList.dat", "rb") as Data:
                GLOBAL_VARS.EntriesDictList = pickle.load(Data)
                print("Loaded", GLOBAL_VARS.EntriesDictList)
                GLOBAL_VARS.SourceEntriesList = pickle.load(Data)
                GLOBAL_VARS.GameEntriesList = pickle.load(Data)
                GLOBAL_VARS.FormattedEntriesDictList = pickle.load(Data)    
                   
    def AutoLoad():
        if os.path.exists("BackupsList.dat"):
            print("loading")
            DATA_SAVER.LoadList()
            LIST_MANAGER.UpdateLists()

class TABULA_GUI: ## GOOEY - this is kinda wackily formatted and will be a problem later but IT JUST WORKS -- MAKE THIS A CLASS
    
    def __init__(self, root):

        root.title("T.A.BU.L.A")
        root.geometry("850x520")
        sv_ttk.set_theme("dark")

        mainframe = ttk.Frame(root, padding="12 12 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        TABULA_GUI.SaveFileListVar = StringVar(value=GLOBAL_VARS.SourceEntriesList)
        TABULA_GUI.GameNameListVar = StringVar(value=GLOBAL_VARS.GameEntriesList)

        ttk.Label(mainframe, text="TWIM's semi-Automatic Back-Up & Load Application").grid(column=2, row=1, sticky=(N))

        ttk.Label(mainframe, text="Game Name").grid(column=2, row=12, sticky=(W), pady=7)
        TABULA_GUI.GameEntered = StringVar()
        TABULA_GUI.GameNameEntry = ttk.Entry(mainframe, width=100, textvariable=TABULA_GUI.GameEntered)
        TABULA_GUI.GameNameEntry.grid(column=2, row=13, sticky=(W, E))

        ttk.Label(mainframe, text="Source File Path").grid(column=2, row=16, sticky=(W),)
        TABULA_GUI.SourcePathEntered = StringVar()
        TABULA_GUI.SourcePathEntry = ttk.Entry(mainframe, width=100, textvariable=TABULA_GUI.SourcePathEntered)
        TABULA_GUI.SourcePathEntry.grid(column=2, row=17, sticky=(W, E), pady=1)

        ttk.Button(mainframe, text="Browse", command=LIST_MANAGER.SourceFileEntryBrowse).grid(column=2, row=16, sticky=(E), pady=3)

        ttk.Label(mainframe, text="Destination Path").grid(column=2, row=18, sticky=(W))
        TABULA_GUI.DestinationPathEntered = StringVar()
        TABULA_GUI.DestinationPathEntry = ttk.Entry(mainframe, width=100, textvariable=TABULA_GUI.DestinationPathEntered)
        TABULA_GUI.DestinationPathEntry.grid(column=2, row=19, sticky=(W, E), pady=1)

        ttk.Button(mainframe, text="Browse", command=LIST_MANAGER.DestinationPathEntryBrowse).grid(column=2, row=18, sticky=(E), pady=3)

        ttk.Button(mainframe, text="Add Save", command=LIST_MANAGER.SaveToList).grid(column=2, row=20, sticky=(S, W), pady=(3, 5))
        
        ### MAKE THIS A TREEVIEW MY GOD 
        TABULA_GUI.SaveListBox = Listbox(mainframe, listvariable=TABULA_GUI.SaveFileListVar, height=12, width=120)
        TABULA_GUI.SaveListBox.grid(column=2, row=21, sticky=(W))
        TABULA_GUI.GameNameBox = Listbox(mainframe, listvariable=TABULA_GUI.GameNameListVar, height=12, width=15, state=DISABLED)
        TABULA_GUI.GameNameBox.grid(column=2, row=21, sticky=(E))

        TABULA_GUI.RemoveListButton = ttk.Button(mainframe, text="Remove Save", state=DISABLED, command=LIST_MANAGER.RemoveFromList)
        TABULA_GUI.RemoveListButton.grid(column=2, row=20, sticky=(S, E), pady=(0, 5))
        ## SERIOUSLY DO IT DUMMY
        
        TABULA_GUI.SaveListBox.bind("<Button-1>", LIST_MANAGER.EnableListButton)

        ttk.Button(mainframe, text="Backup", command=BACKUP_AND_LOAD.BackupSaves).grid(column=2, row=27, sticky=(S), pady=2)
        
        
        ### Future New Window, learning treeview first and getting it all ready before making it a tab ###
        
        TABULA_GUI.LoadTree = ttk.Treeview(mainframe)  ## leaning loadtree
        TABULA_GUI.LoadTree.grid(column=2, row=30, sticky=S)
        ## TABULA_GUI.LoadTree.insert('', 'end', text="banana") ## insert with this
        TABULA_GUI.LoadTree['columns'] = ('Date', 'Path')
        
        TABULA_GUI.LoadTree.column('#0', width=200, anchor='w')
        TABULA_GUI.LoadTree.heading('#0', text="Game")
        
        TABULA_GUI.LoadTree.column('Date', width=200, anchor='center')
        TABULA_GUI.LoadTree.heading('Date', text="DATE")
        
        TABULA_GUI.LoadTree.column('Path', width=420, anchor='e')
        TABULA_GUI.LoadTree.heading('Path', text="Path")
        
        ## TABULA_GUI.DEBUGBUTTON = ttk.Button(mainframe, text="DEBUG BUTTON", command=lambda: LIST_MANAGER.TreeViewInsertList(LIST_MANAGER.ListValues(GLOBAL_VARS.EntriesDictList, ("Source Path")), TABULA_GUI.LoadTree))
        ## TABULA_GUI.DEBUGBUTTON.grid(column=2, row=20, sticky=(S))
        
        ### Future New Window, learning treeview first and getting it all ready before making it a tab ###

def main():
    root = Tk()            
    TABULA_GUI(root) 
    DATA_SAVER.AutoLoad()
    root.mainloop()

if __name__ == "__main__":
    main()
