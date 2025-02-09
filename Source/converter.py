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


    
    


'''











'''





