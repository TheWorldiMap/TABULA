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


GameNameList = [] ## part of the next system to have seperated folders for each game       
SaveFileList = [] ## list as displayed in the GOOEY (this is messy af and needs to be STOPPED)
SaveBackupData = []  ## Workhorse Data stucture should be an easy JSON when i lean that

SaveFileListVar = StringVar(value=SaveFileList)
GameNameListVar = StringVar(value=GameNameList)

Today = datetime.today().strftime('%Y-%m-%d')

def SaveList():
    with open("BackupsList.dat", "wb") as Data:
        pickle.dump(SaveBackupData, Data)
        pickle.dump(SaveFileList, Data)
        pickle.dump(GameNameList, Data)
        
## this looks kinda raw to my eyes but i am actually proud of how simple this is
def BackupList():
    ListFullSources = [Source["SourceFilePath"] for Source in SaveBackupData]
    ListFullDestinations = [Destination["FullDestPath"] for Destination in SaveBackupData]
    ListDestPath = [Paths["DestPath"] for Paths in SaveBackupData]
    for Source in ListFullSources:
       for Destination in ListFullDestinations:
           for Paths in ListDestPath:
                if not os.path.exists(Paths):
                    os.makedirs(Paths)
                    shutil.copy(Source, Destination)  
                else:
                    shutil.copy(Source, Destination)
 
## i could do this better if i knew what i was doing when i started it...   
def SaveToList():
    GameNameEntered = GameName.get()
    DestinationFolderFormatted = DestinationPath.get() + "\\" + GameNameEntered + "\\" + Today
    SourceFilePathD = SourceFilePath.get()
    SourceFile = os.path.basename(SourceFilePathD)
    DestinationFilePath = DestinationFolderFormatted + "\\" + SourceFile
    SaveBackupDict = {"SourceFilePath" : SourceFilePathD, "FullDestPath" : DestinationFilePath, "FileNames" : SourceFile, "DestPath" : DestinationFolderFormatted }
    SaveBackupData.append(SaveBackupDict)
    SaveFileList.append(SourceFilePathD)
    SaveFileListVar.set(SaveFileList)
    GameNameList.append(GameNameEntered)
    GameNameListVar.set(GameNameList)

## This    
def EnableListButton(*args):
    RemoveListButton.configure(state=ACTIVE)

## this is awful and im sure there is a nicer way to do it BUT IT JUST WORKS
def RemoveFromList():
    SelectedIndex = SaveListBox.curselection()
    list(SelectedIndex)
    del SaveFileList[SelectedIndex[0]]
    del GameNameList[SelectedIndex[0]]
    SaveListBox.delete([SelectedIndex[0]])
    GameNameBox.delete([SelectedIndex[0]])
    SaveBackupData.pop(SelectedIndex[0])
    RemoveListButton.configure(state=DISABLED)
    GameNameListVar.set(GameNameList)
    
    
## GOOEY - this is kinda wackily formatted and will be a problem later but IT JUST WORKS 
mainframe = ttk.Frame(root, padding="12 12 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="TWIM's Save File Auto Backup").grid(column=2, row=1, sticky=(N))

ttk.Label(mainframe, text="Game Name").grid(column=2, row=12, sticky=(W))
GameName = StringVar()
GameNameEntry = ttk.Entry(mainframe, width=100, textvariable=GameName)
GameNameEntry.grid(column=2, row=13, sticky=(W, E))

ttk.Label(mainframe, text="Source File Path").grid(column=2, row=16, sticky=(W))
SourceFilePath = StringVar()
SourcePathEntry = ttk.Entry(mainframe, width=100, textvariable=SourceFilePath)
SourcePathEntry.grid(column=2, row=17, sticky=(W, E))

ttk.Label(mainframe, text="Destination Path").grid(column=2, row=18, sticky=(W))
DestinationPath = StringVar()
DestinationPathEntry = ttk.Entry(mainframe, width=100, textvariable=DestinationPath)
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


## autoload function lite
if os.path.exists("BackupsList.dat"):
    print("loading")
    with open("BackupsList.dat", "rb") as Data:
            SaveBackupData = pickle.load(Data)
            SaveFileList = pickle.load(Data)
            GameNameList = pickle.load(Data)
            print(SaveBackupData)
            print(SaveFileList)
            print(GameNameList)
            SaveFileListVar.set(SaveFileList)
            GameNameListVar.set(GameNameList)
            
            
root.mainloop()

