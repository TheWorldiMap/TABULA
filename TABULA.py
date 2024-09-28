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
import sv_ttk

from datetime import datetime
from tkinter import *
from tkinter import ttk
import tkinter.dialog
import tkinter.filedialog
 
class GLOBAL_VARS: ## Data that everything touches 
    
    GameEntriesList = [] ## part of the next system to have seperated folders for each game       
    SourceEntriesList = [] ## list as displayed in the GOOEY (this is messy af and needs to be STOPPED)
    EntriesList = []  ## Workhorse Data stucture should be an easy JSON when i lean that
    FormattedEntries = [] ## workhorse part 2
    BackedUpFiles = [] ## list path to files fully backed up for listing in loading
    BackedUpPaths = [] ## list paths created to store files for listing  in loading

    Today = datetime.today().strftime('%Y-%m-%d')

class LIST_MANAGER: ## Manages all the Lists functions
           
    def FormatEntries():
        list_games = [Game["Game"] for Game in GLOBAL_VARS.EntriesList]
        list_source_files = [SourceFile["Source File"] for SourceFile in GLOBAL_VARS.EntriesList]
        list_source_paths = [SourcePath["Source Path"] for SourcePath in GLOBAL_VARS.EntriesList]
        list_destination_paths = [DestinationPath["Destination Path"] for DestinationPath in GLOBAL_VARS.EntriesList]

        for Game, SourceFile, SourcePath, DestinationPath in zip(list_games, list_source_files, list_source_paths, list_destination_paths):
            full_source = (SourcePath + "\\" + SourceFile)
            full_destination = (DestinationPath + "\\" + Game + "\\" + GLOBAL_VARS.Today + "\\" + SourceFile)
            destination_path = (DestinationPath + "\\" + Game + "\\" + GLOBAL_VARS.Today + "\\")
    
            formatted_entry = {
        "Full Source" : full_source,
        "Full Destination" : full_destination,
        "Destination Path" : destination_path
        }
            GLOBAL_VARS.FormattedEntries.append(formatted_entry)
    
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
        GLOBAL_VARS.EntriesList.append(entires_dict)
        GLOBAL_VARS.SourceEntriesList.append(source_entered)
        GLOBAL_VARS.GameEntriesList.append(game_entered)
        LIST_MANAGER.UpdateLists()

    def EnableListButton(*args):
        TABULA_GUI.RemoveListButton.configure(state=ACTIVE)
    def RemoveFromList(): ## this is awful and im sure there is a nicer way to do it BUT IT JUST WORKS
        SelectedIndex = TABULA_GUI.SaveListBox.curselection()
        list(SelectedIndex)
        del GLOBAL_VARS.SourceEntriesList[SelectedIndex[0]]
        del GLOBAL_VARS.GameEntriesList[SelectedIndex[0]]
        TABULA_GUI.SaveListBox.delete([SelectedIndex[0]])
        TABULA_GUI.GameNameBox.delete([SelectedIndex[0]])
        GLOBAL_VARS.EntriesList.pop(SelectedIndex[0])
        TABULA_GUI.RemoveListButton.configure(state=DISABLED)
        LIST_MANAGER.UpdateLists()

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
        list_full_sources = [FullSource["Full Source"] for FullSource in GLOBAL_VARS.FormattedEntries]
        list_full_destinations = [FullDestination["Full Destination"] for FullDestination in GLOBAL_VARS.FormattedEntries]
        list_destination_paths = [DestinationPath["Destination Path"] for DestinationPath in GLOBAL_VARS.FormattedEntries]
        
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
            pickle.dump(GLOBAL_VARS.EntriesList, Data)
            pickle.dump(GLOBAL_VARS.SourceEntriesList, Data)
            pickle.dump(GLOBAL_VARS.GameEntriesList, Data)
            pickle.dump(GLOBAL_VARS.FormattedEntries, Data)
        
    def LoadList():
            with open("BackupsList.dat", "rb") as Data:
                GLOBAL_VARS.EntriesList = pickle.load(Data)
                GLOBAL_VARS.SourceEntriesList = pickle.load(Data)
                GLOBAL_VARS.GameEntriesList = pickle.load(Data)
                GLOBAL_VARS.FormattedEntries = pickle.load(Data)    
                   
    def AutoLoad():
        if os.path.exists("BackupsList.dat"):
            print("loading")
            DATA_SAVER.LoadList()
            LIST_MANAGER.UpdateLists()

class TABULA_GUI: ## GOOEY - this is kinda wackily formatted and will be a problem later but IT JUST WORKS -- MAKE THIS A CLASS -- Made this a class
    
    def __init__(self, mainframe):

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
        GameNameEntry = ttk.Entry(mainframe, width=100, textvariable=TABULA_GUI.GameEntered)
        GameNameEntry.grid(column=2, row=13, sticky=(W, E))

        ttk.Label(mainframe, text="Source File Path").grid(column=2, row=16, sticky=(W),)
        TABULA_GUI.SourcePathEntered = StringVar()
        SourcePathEntry = ttk.Entry(mainframe, width=100, textvariable=TABULA_GUI.SourcePathEntered)
        SourcePathEntry.grid(column=2, row=17, sticky=(W, E), pady=1)

        ttk.Button(mainframe, text="Browse", command=LIST_MANAGER.SourceFileEntryBrowse).grid(column=2, row=16, sticky=(E), pady=3)

        ttk.Label(mainframe, text="Destination Path").grid(column=2, row=18, sticky=(W))
        TABULA_GUI.DestinationPathEntered = StringVar()
        DestinationPathEntry = ttk.Entry(mainframe, width=100, textvariable=TABULA_GUI.DestinationPathEntered)
        DestinationPathEntry.grid(column=2, row=19, sticky=(W, E), pady=1)

        ttk.Button(mainframe, text="Browse", command=LIST_MANAGER.DestinationPathEntryBrowse).grid(column=2, row=18, sticky=(E), pady=3)

        ttk.Button(mainframe, text="Add Save", command=LIST_MANAGER.SaveToList).grid(column=2, row=20, sticky=(S, W), pady=(3, 5))
        
        ### MAKE THIS A TREEVIEW MY GOD 
        SaveListBox = Listbox(mainframe, listvariable=TABULA_GUI.SaveFileListVar, height=12, width=120)
        SaveListBox.grid(column=2, row=21, sticky=(W))
        GameNameBox = Listbox(mainframe, listvariable=TABULA_GUI.GameNameListVar, height=12, width=15, state=DISABLED)
        GameNameBox.grid(column=2, row=21, sticky=(E))

        RemoveListButton = ttk.Button(mainframe, text="Remove Save", state=DISABLED, command=LIST_MANAGER.RemoveFromList)
        RemoveListButton.grid(column=2, row=20, sticky=(S, E), pady=(0, 5))
        ## SERIOUSLY DO IT DUMMY

        SaveListBox.bind("<Button-1>", LIST_MANAGER.EnableListButton)

        ttk.Button(mainframe, text="Backup List", command=BACKUP_AND_LOAD.BackupSaves).grid(column=2, row=27, sticky=(S), pady=2)

        ttk.Button(mainframe, text="Save List", command=DATA_SAVER.SaveList).grid(column=2, row=27, sticky=(S, W), pady=2)

root = Tk()            
TABULA_GUI(root) 
DATA_SAVER.AutoLoad()
root.mainloop()