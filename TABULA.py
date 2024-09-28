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
 
class GLOBAL_DATA:
    
    GameEntriesList = [] ## part of the next system to have seperated folders for each game       
    SourceEntriesList = [] ## list as displayed in the GOOEY (this is messy af and needs to be STOPPED)
    EntriesList = []  ## Workhorse Data stucture should be an easy JSON when i lean that
    FormattedEntries = [] ## workhorse part 2

    Today = datetime.today().strftime('%Y-%m-%d')

class LIST_MANAGER:
    
        def BackupList(): ## this looks kinda raw to my eyes but i am actually proud of how simple this is
            LIST_MANAGER.FormatEntries()
            list_full_sources = [FullSource["Full Source"] for FullSource in GLOBAL_DATA.FormattedEntries]
            list_full_destinations = [FullDestination["Full Destination"] for FullDestination in GLOBAL_DATA.FormattedEntries]
            list_destination_paths = [DestinationPath["Destination Path"] for DestinationPath in GLOBAL_DATA.FormattedEntries]
    
            for FullDestination, FullSource, DestinationPath in zip(list_full_destinations, list_full_sources, list_destination_paths):
                if not os.path.exists(DestinationPath):
                    os.makedirs(DestinationPath)
                    shutil.copy(FullSource, FullDestination)
                else:
                    shutil.copy(FullSource, FullDestination)
            
        def FormatEntries():
            list_games = [Game["Game"] for Game in GLOBAL_DATA.EntriesList]
            list_source_files = [SourceFile["Source File"] for SourceFile in GLOBAL_DATA.EntriesList]
            list_source_paths = [SourcePath["Source Path"] for SourcePath in GLOBAL_DATA.EntriesList]
            list_destination_paths = [DestinationPath["Destination Path"] for DestinationPath in GLOBAL_DATA.EntriesList]
    
            for Game, SourceFile, SourcePath, DestinationPath in zip(list_games, list_source_files, list_source_paths, list_destination_paths):
                full_source = (SourcePath + "\\" + SourceFile)
                full_destination = (DestinationPath + "\\" + Game + "\\" + GLOBAL_DATA.Today + "\\" + SourceFile)
                destination_path = (DestinationPath + "\\" + Game + "\\" + GLOBAL_DATA.Today + "\\")
        
                formatted_entry = {
            "Full Source" : full_source,
            "Full Destination" : full_destination,
            "Destination Path" : destination_path
            }
                GLOBAL_DATA.FormattedEntries.append(formatted_entry)
        
        def SaveToList(self): ## i could do this better if i knew what i was doing when i started it... -- fixed it a bit but also MAKE THIS A CLASS 
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
            GLOBAL_DATA.EntriesList.append(entires_dict)
            GLOBAL_DATA.SourceEntriesList.append(source_entered)
            GLOBAL_DATA.GameEntriesList.append(game_entered)
            self.UpdateLists()
    
        def UpdateLists(self):
            TABULA_GUI.GameNameListVar.set(GLOBAL_DATA.GameEntriesList)
            TABULA_GUI.SaveFileListVar.set(GLOBAL_DATA.SourceEntriesList)
    
        def EnableListButton(*args):
            TABULA_GUI.RemoveListButton.configure(state=ACTIVE)

        def RemoveFromList(): ## this is awful and im sure there is a nicer way to do it BUT IT JUST WORKS
            SelectedIndex = TABULA_GUI.SaveListBox.curselection()
            list(SelectedIndex)
            del GLOBAL_DATA.SourceEntriesList[SelectedIndex[0]]
            del GLOBAL_DATA.GameEntriesList[SelectedIndex[0]]
            TABULA_GUI.SaveListBox.delete([SelectedIndex[0]])
            TABULA_GUI.GameNameBox.delete([SelectedIndex[0]])
            GLOBAL_DATA.EntriesList.pop(SelectedIndex[0])
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

class DATA_SAVER:
    
    def SaveList():
        with open("BackupsList.dat", "wb") as Data:
            pickle.dump(GLOBAL_DATA.EntriesList, Data)
            pickle.dump(GLOBAL_DATA.SourceEntriesList, Data)
            pickle.dump(GLOBAL_DATA.GameEntriesList, Data)
            pickle.dump(GLOBAL_DATA.FormattedEntries, Data)
        
    def LoadList():
            with open("BackupsList.dat", "rb") as Data:
                GLOBAL_DATA.EntriesList = pickle.load(Data)
                GLOBAL_DATA.SourceEntriesList = pickle.load(Data)
                GLOBAL_DATA.GameEntriesList = pickle.load(Data)
                GLOBAL_DATA.FormattedEntries = pickle.load(Data)    
                   
    def AutoLoad():
        if os.path.exists("BackupsList.dat"):
            print("loading")
            DATA_SAVER.LoadList()
            LIST_MANAGER.UpdateLists()

class TABULA_GUI: ## GOOEY - this is kinda wackily formatted and will be a problem later but IT JUST WORKS -- MAKE THIS A CLASS -- Made this a class
    
    def __init__(self, root):
    
        root.title("T.A.BU.L.A")
        root.geometry("850x520")
        sv_ttk.set_theme("dark")

        mainframe = ttk.Frame(root, padding="12 12 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        SaveFileListVar = StringVar(value=GLOBAL_DATA.SourceEntriesList)
        GameNameListVar = StringVar(value=GLOBAL_DATA.GameEntriesList)

        ttk.Label(mainframe, text="TWIM's semi-Automatic Back-Up & Load Application").grid(column=2, row=1, sticky=(N))

        ttk.Label(mainframe, text="Game Name").grid(column=2, row=12, sticky=(W), pady=7)
        GameEntered = StringVar()
        GameNameEntry = ttk.Entry(mainframe, width=100, textvariable=GameEntered)
        GameNameEntry.grid(column=2, row=13, sticky=(W, E))

        ttk.Label(mainframe, text="Source File Path").grid(column=2, row=16, sticky=(W),)
        SourcePathEntered = StringVar()
        SourcePathEntry = ttk.Entry(mainframe, width=100, textvariable=SourcePathEntered)
        SourcePathEntry.grid(column=2, row=17, sticky=(W, E), pady=1)

        ttk.Button(mainframe, text="Browse", command=LIST_MANAGER.SourceFileEntryBrowse).grid(column=2, row=16, sticky=(E), pady=3)

        ttk.Label(mainframe, text="Destination Path").grid(column=2, row=18, sticky=(W))
        DestinationPathEntered = StringVar()
        DestinationPathEntry = ttk.Entry(mainframe, width=100, textvariable=DestinationPathEntered)
        DestinationPathEntry.grid(column=2, row=19, sticky=(W, E), pady=1)

        ttk.Button(mainframe, text="Browse", command=LIST_MANAGER.DestinationPathEntryBrowse).grid(column=2, row=18, sticky=(E), pady=3)

        ttk.Button(mainframe, text="Add Save", command=LIST_MANAGER.SaveToList).grid(column=2, row=20, sticky=(S, W), pady=(3, 5))

        SaveListBox = Listbox(mainframe, listvariable=SaveFileListVar, height=12, width=120)
        SaveListBox.grid(column=2, row=21, sticky=(W))
        GameNameBox = Listbox(mainframe, listvariable=GameNameListVar, height=12, width=15, state=DISABLED)
        GameNameBox.grid(column=2, row=21, sticky=(E))

        RemoveListButton = ttk.Button(mainframe, text="Remove Save", state=DISABLED, command=LIST_MANAGER.RemoveFromList)
        RemoveListButton.grid(column=2, row=20, sticky=(S, E), pady=(0, 5))

        SaveListBox.bind("<Button-1>", LIST_MANAGER.EnableListButton)

        ttk.Button(mainframe, text="Backup List", command=LIST_MANAGER.BackupList).grid(column=2, row=27, sticky=(S), pady=2)

        ttk.Button(mainframe, text="Save List", command=DATA_SAVER.SaveList).grid(column=2, row=27, sticky=(S, W), pady=2)

root = Tk()            
TABULA_GUI(root) 
DATA_SAVER.AutoLoad()
root.mainloop()