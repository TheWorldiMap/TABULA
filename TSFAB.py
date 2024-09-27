###############################################################################################################################################
#                                                                                                                                             #
#  This program is free software:                                                                                                             #
#                                                                                                                                             #
#  you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software #Foundation;  #
#  either version 3 of the License, or (at your option) any later version.                                                                    #
#                                                                                                                                             #
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;                                                  #
#  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A #PARTICULAR PURPOSE.                                                 #
#  See the GNU General Public License for more details.                                                                                       #
#                                                                                                                                             #
#  You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.      #
#                                                                                                                                             #
###############################################################################################################################################

import tkinter
import shutil 
import pickle
import os
import datetime

from datetime import datetime
from tkinter import *
from tkinter import ttk

#### Frame #### 
root = Tk()
root.title("TSFAB")
root.geometry("630x470")


GameEntriesList = [] ## part of the next system to have seperated folders for each game       
SourceEntriesList = [] ## list as displayed in the GOOEY (this is messy af and needs to be STOPPED)
EntriesList = []  ## Workhorse Data stucture should be an easy JSON when i lean that
FormattedEntries = [] ## workhorse part 2

SaveFileListVar = StringVar(value=SourceEntriesList)
GameNameListVar = StringVar(value=GameEntriesList)

Today = datetime.today().strftime('%Y-%m-%d')

def SaveList():
    with open("BackupsList.dat", "wb") as Data:
        pickle.dump(EntriesList, Data)
        pickle.dump(SourceEntriesList, Data)
        pickle.dump(GameEntriesList, Data)
        pickle.dump(FormattedEntries, Data)
        
## this looks kinda raw to my eyes but i am actually proud of how simple this is
def BackupList():
    FormatEntries()
    list_full_sources = [FullSource["Full Source"] for FullSource in FormattedEntries]
    list_full_destinations = [FullDestination["Full Destination"] for FullDestination in FormattedEntries]
    list_destination_paths = [DestinationPath["Destination Path"] for DestinationPath in FormattedEntries]
    
    for FullDestination, FullSource, DestinationPath in zip(list_full_destinations, list_full_sources, list_destination_paths):
        if not os.path.exists(DestinationPath):
            os.makedirs(DestinationPath)
            shutil.copy(FullSource, FullDestination)
        else:
            shutil.copy(FullSource, FullDestination)
            
def FormatEntries():
    list_games = [Game["Game"] for Game in EntriesList]
    list_source_files = [SourceFile["Source File"] for SourceFile in EntriesList]
    list_source_paths = [SourcePath["Source Path"] for SourcePath in EntriesList]
    list_destination_paths = [DestinationPath["Destination Path"] for DestinationPath in EntriesList]
    
    for Game, SourceFile, SourcePath, DestinationPath in zip(list_games, list_source_files, list_source_paths, list_destination_paths):
        full_source = (SourcePath + "\\" + SourceFile)
        full_destination = (DestinationPath + "\\" + Game + "\\" + Today + "\\" + SourceFile)
        destination_path = (DestinationPath + "\\" + Game + "\\" + Today + "\\")
        
        formatted_entry = {
            "Full Source" : full_source,
            "Full Destination" : full_destination,
            "Destination Path" : destination_path
            }
        FormattedEntries.append(formatted_entry)
        
        
## i could do this better if i knew what i was doing when i started it... -- fixed it a bit but also MAKE THIS A CLASS  
def SaveToList():
    game_entered = GameEntered.get()
    source_entered = SourceFile.get()
    destination_entered = DestinationPathEntered.get() 
    source_file = os.path.basename(source_entered)
    source_path = os.path.dirname(source_entered)
    entires_dict = {
        "Game" : game_entered,
        "Source File" : source_file,
        "Source Path" : source_path, 
        "Destination Path" : destination_entered,
    }
    EntriesList.append(entires_dict)
    SourceEntriesList.append(source_entered)
    GameEntriesList.append(game_entered)
    UpdateLists()
    
def UpdateLists():
    GameNameListVar.set(GameEntriesList)
    SaveFileListVar.set(SourceEntriesList)
    
## This    
def EnableListButton(*args):
    RemoveListButton.configure(state=ACTIVE)

## this is awful and im sure there is a nicer way to do it BUT IT JUST WORKS
def RemoveFromList():
    SelectedIndex = SaveListBox.curselection()
    list(SelectedIndex)
    del SourceEntriesList[SelectedIndex[0]]
    del GameEntriesList[SelectedIndex[0]]
    SaveListBox.delete([SelectedIndex[0]])
    GameNameBox.delete([SelectedIndex[0]])
    EntriesList.pop(SelectedIndex[0])
    RemoveListButton.configure(state=DISABLED)
    UpdateLists()
    
    
## GOOEY - this is kinda wackily formatted and will be a problem later but IT JUST WORKS 
mainframe = ttk.Frame(root, padding="12 12 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="TWIM's Save File Auto Backup").grid(column=2, row=1, sticky=(N))

ttk.Label(mainframe, text="Game Name").grid(column=2, row=12, sticky=(W))
GameEntered = StringVar()
GameNameEntry = ttk.Entry(mainframe, width=100, textvariable=GameEntered)
GameNameEntry.grid(column=2, row=13, sticky=(W, E))

ttk.Label(mainframe, text="Source File Path").grid(column=2, row=16, sticky=(W))
SourceFile = StringVar()
SourcePathEntry = ttk.Entry(mainframe, width=100, textvariable=SourceFile)
SourcePathEntry.grid(column=2, row=17, sticky=(W, E))

ttk.Label(mainframe, text="Destination Path").grid(column=2, row=18, sticky=(W))
DestinationPathEntered = StringVar()
DestinationPathEntry = ttk.Entry(mainframe, width=100, textvariable=DestinationPathEntered)
DestinationPathEntry.grid(column=2, row=19, sticky=(W, E))

ttk.Button(mainframe, text="Save To list", command=SaveToList).grid(column=2, row=20, sticky=(S, W))

SaveListBox = Listbox(mainframe, listvariable=SaveFileListVar, height=10, width=80)
SaveListBox.grid(column=2, row=21, sticky=(N, W))
GameNameBox = Listbox(mainframe, listvariable=GameNameListVar, height=10, width=20, state=DISABLED)
GameNameBox.grid(column=2, row=21, sticky=(N, E))

RemoveListButton = ttk.Button(mainframe, text="Remove From List", state=DISABLED, command=RemoveFromList)
RemoveListButton.grid(column=2, row=20, sticky=(S))

SaveListBox.bind("<Button-1>", EnableListButton)

ttk.Button(mainframe, text="Backup List", command=BackupList).grid(column=2, row=27, sticky=(S))

ttk.Button(mainframe, text="Save List", command=SaveList).grid(column=2, row=27, sticky=(S, W))


## autoload function lite make this a class
if os.path.exists("BackupsList.dat"):
    print("loading")
    with open("BackupsList.dat", "rb") as Data:
            EntriesList = pickle.load(Data)
            SourceEntriesList = pickle.load(Data)
            GameEntriesList = pickle.load(Data)
            FormattedEntries = pickle.load(Data)
            print(EntriesList)
            print(SourceEntriesList)
            print(GameEntriesList)
            print(FormattedEntries)
            UpdateLists()
            
            
root.mainloop()

