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
    
notes = read_obsidian_notes("notes")

for name, content in notes:
    print(f"Name: {name}\n\nFirst 50 char of note:\n{content:50}...\n")


def parseQA(content : str)-> list[tuple[str,str]]: 
    
    lines = content.split("\n") # variable holding lines of notes

    qaPairs = []
    currentq = None
    currenta = None

    for line in lines:
        line = line.strip()
        
        if line.startswith("Q:"):
            #Save prev q/a if exists
            if currentq and currenta:
                qaPairs.append((currentq,currenta))
                currenta = None
            currentq = line[2:].strip()
        
        elif line.startswith("A:") and currentq:
            currenta = line[2:].strip()
            qaPairs.append((currentq,currenta))
            currentq = None
        
        elif currentq and currenta is None:
            #handle for multiline answer
            currenta = line.strip()
        
        elif currenta and currentq:
            #append to multiline answer
            currenta += "\n" + line.strip()
    
    if currentq and currenta:
        qaPairs.append((currentq,currenta))
    
    return qaPairs

content = """
Q: What is Python?
A: A programming language.

Q: What is Anki?
A: A flashcard app.
"""

pairs = parseQA(content)   
print(pairs)



    


'''











'''





