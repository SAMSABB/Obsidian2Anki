import requests
from pathlib import Path
import os



def read_vaults(vaults_dir:str)-> list[tuple[str,str]]:
    """
    Reads all subdirectories in a directory and returns list
    containing(vault_name,vault_path) 
    """
    vaults_dir = Path(vaults_dir)
    
    if not vaults_dir.exists():
        raise FileNotFoundError(f"Directory: {vaults_dir} Not found. :(")
    
    vaults = [vault for vault in vaults_dir.iterdir()if vault.is_dir()] # Loops through directory returning all vaults

    vaults_info= []

    for vault_path in vaults: # Loops thorugh vaults returning their name and path
        vault_name = vault_path.name
        vaults_info.append((vault_name,vault_path))
    
    return vaults_info

def read_obsidian_notes(vault_path: str)-> list[tuple[str,str]]:

    """
    Reads all .md files in a directory and returns list of (filename, content)
    """

    vault_path = Path(vault_path)


    if not vault_path.exists():
        raise FileNotFoundError(f"Vault: {vault_path} Not found")
    
    markdown_files = list(vault_path.glob("**/*.md")) #**/* gets all md files including subfolders

    notes = []

    for file_path in markdown_files: #Loop through files and read their content
        try:
            content = file_path.read_text(encoding="utf-8")
            notes.append((file_path.name,content)) 
        
        except Exception as e:
            print (f"Error reading {file_path}: {e}")

    return notes
    

def parseQA(content : str)-> list[tuple[str,str]]: 
    
    lines = content.split("\n") # variable holding lines of notes

    qaPairs = []
    currentq = None
    currenta = None
    inAnswer = False

    for line in lines:
        line = line.strip()
        
        if line.startswith("Q:"):
            #Save prev q/a if exists
            if currentq:
                if currenta:
                    qaPairs.append((currentq,"\n".join(currenta)))
                else:
                    print(f"Warning! Question {currentq} has NO ANSWER")
                
            currentq = line[2:].strip()
            currenta = []
            inAnswer = False
        
        elif line.startswith("A:") and currentq:
            inAnswer = True
            currenta.append(line[2:].strip())
            
        
        elif inAnswer and line.startswith("-"):
            #handle for multiline answer
            currenta.append(line.strip())
        
        elif currentq and not inAnswer and line.startswith("-"):
            #append lines part of the answer without prefix
            currenta.append(line.strip())
        
    if currentq and currenta:
        qaPairs.append((currentq,"\n".join(currenta)))
    
    return qaPairs




def check_anki_connected():
    try:
        response = requests.post("http://localhost:8765", json={"action":"version","version": 6})
        print("Connected to Anki")
    except:
        print("Error????????? Is Anki running? Try Again after opening Anki.")
        exit()

def create_deck(deck_name):
    requests.post("http://localhost:8765",json={"action":"createDeck",
                    "version":6, "params":{"deck": deck_name}})

def add_card(question,answer, deck_name):
    requests.post("http://localhost:8765", json={"action":"addNote","version":6,
    "params":{
        "note":{
            "deckName": deck_name,
            "modelName": "Basic",
            "fields":{"Front":question,"Back": answer}
            }
        }
    })

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
INPUT PATH TO FOLDER CONTAINING VAULTS HERE
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

vaults_dir = "notes"

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
INPUT PATH TO FOLDER CONTAINING VAULTS HERE
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
vaults_info = read_vaults(vaults_dir)

check_anki_connected()

#Processing vaults to create decks
for vault_name, vault_path in vaults_info:
    notes = read_obsidian_notes(vault_path)
    all_pairs = []
    for name, content in notes:
        all_pairs.extend(parseQA(content)) 
    
    deck_name = f"Obsidian Flashcards - {vault_name}"
    create_deck(deck_name)


    for question,answer in all_pairs:
        add_card(question,answer, deck_name)
    







print(all_pairs)


print("cards added to anki!")




'''





'''