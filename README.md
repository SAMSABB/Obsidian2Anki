# Obsidian2Anki ⚠️⚠️WIP⚠️⚠️
### A python tool that automatically Convert MD files to Anki flashcards
### Perfect for use with Obsidian Note taking
 
### What It Does
- Converts notes to flashcards: Use simple Q: and A: markers in Obsidian to create cards.

Auto-sync: 
- Updates Anki decks when your notes change (no manual work!).

Supports tags and links:
- Keeps your Obsidian tags and links in Anki.

Easy to run:
- Use a command-line tool to pick your notes and deck name.

How to Use
- Install:

````bash

git clone https://github.com/SAMSABB/Obsidian2Anki  
pip install -r requirements.txt  
````
- Add questions in Obsidian like this:

````markdown

Q: What is Python?  
A: A programming language.
````
- Run the tool:
````bash
python converter.py --notes "my_notes_folder" --deck "Study Deck"  
````
- Open the .apkg file in Anki and start studying!

### Why It’s Cool

- Saves time: No more copying notes into Anki by hand.

- Written in Python: Uses libraries like genanki for Anki integration.

 - Easy to customize: Change how questions are formatted or add tags.

### For Employers
This project shows I can:

- Build tools that solve real problems (automation!).

- Work with APIs and libraries (ankiconnect, watchdog).

- Write clean, documented code.

Check out the code on GitHub — contributions welcome!

### Demo
(Basic Demo)
