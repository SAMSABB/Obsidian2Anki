import requests
from pathlib import Path

def read_obsidian_notes(notes_dir: str)-> list[tuple[str,str]]:

    """
    Reads all .md files in a directory and returns list of (filename, content)
    """

    notes_dir = Path(notes_dir)

    if not notes_dir.exists():
        raise FileNotFoundError(f"Directory: {notes_dir} Not found")
    
    markdown_files = list(notes_dir.glob("**/*.md")) #**/* gets all md files including subfolders

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


notes = read_obsidian_notes("notes")
all_pairs = []
for name, content in notes:
    pairs = parseQA(content)
    all_pairs.extend(pairs) 
    



check_anki_connected()
create_deck("Obsidian Flashcards")
print(all_pairs)
for question,answer in all_pairs:
    add_card(question,answer, "Obsidian Flashcards")

print("cards added to anki!")




'''





'''