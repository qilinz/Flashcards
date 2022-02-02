# Flashcards

This program can be used to do memory exercise. Cards can be loaded from or saved to file.

# How to use
- Run the file to start, e.g. `python flashcards.py.`
  - If you'd like to load cards:`python flashcards.py --import_from=YourCardFile.txt`
  - If you'd like to save the cards: `python flashcards.py --export_to=YourCardFile.txt`
  - The above two arguments can be used at the same time. 
- Commands supported: 
  - add: add a new card
  - remove: remove a card
  - import: import a file of cards
  - export: export cards to a file
  - ask: ask questions to test
  - exit: exit the program
  - log: save all the inputs and outputs to the log file
  - hardest card: show the cards receiving the highest wrong answers.
  - reset stats: reset the wrong answer times of all cards to 0
- If you would like to create a card file using .txt, the format should follow:
  - One card in a line
  - the definition and the explanation should be separated by " ,"
  - e.g. "Hello, Bonjour"



Disclaimer: The original project idea is from [JetBrains Academy](https://hyperskill.org/projects/127). All codes were written by myself.