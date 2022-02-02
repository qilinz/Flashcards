import os
import io
from random import choice
import argparse


ADD = "add"
REMOVE = "remove"
IMPORT = "import"
EXPORT = "export"
ASK = "ask"
EXIT = "exit"
LOG = "log"
HARDEST_CARD = "hardest card"
RESET = "reset stats"

# set up logger
output = io.StringIO()
cards = {}


def add():
    front = input("The card:\n")
    print(f'The card:\n{front}', file=output)

    while front in cards:
        front = input(f'The term "{front}" already exists. Try again:\n')
        print(f'The term "{front}" already exists. Try again:\n{front}', file=output)

    back = input("The definition of the card:\n")
    print(f'The definition of the card:\n{back}', file=output)

    while back in [value["definition"] for key, value in cards.items()]:
        back = input(f'The definition "{back}" already exists. Try again:\n')
        print(f'The definition "{back}" already exists. Try again:\n{back}', file=output)

    cards[front] = {
        "definition": back,
        "mistake": 0
    }
    print(f'The pair ("{front}":"{back}") has been added.')
    print(f'The pair ("{front}":"{back}") has been added.', file=output)


def remove():
    front = input("Which card?\n")
    print(f'Which card?\n{front}', file=output)

    if front in cards:
        cards.pop(front)
        print("The card has been removed.")
        print("The card has been removed.", file=output)
    else:
        print(f'Can\'t remove "{front}": there is no such card.')
        print(f'Can\'t remove "{front}": there is no such card.', file=output)


def _import(file_path):
    if os.access(file_path, os.F_OK):
        new_dict = {}
        with open(file_path) as file:
            data = file.read().splitlines()
            for card in data:
                front, back, count = card.split(", ")
                new_dict[front] = {
                    "definition": back,
                    "mistake": int(count)
                }

        print(f"{len(new_dict)} cards have been loaded.")
        print(f"{len(new_dict)} cards have been loaded.", file=output)
        cards.update(new_dict)

    else:
        print("File not found.")
        print("File not found.", file=output)


def export(file_path):
    with open(file_path, "w") as file:
        for front, value in cards.items():
            print(f"{front}, {value['definition']}, {value['mistake']}", file=file)

    print(f"{len(cards)} cards have been saved.")
    print(f"{len(cards)} cards have been saved.", file=output)


def ask():
    n_ask = int(input("How many times to ask?\n").strip())
    print(f'How many times to ask?\n{n_ask}', file=output)

    card_list = list(cards.items())
    while n_ask > 0:
        random_card = choice(card_list)
        front, value = random_card
        definition = value["definition"]
        answer = input(f'Print the definition of "{front}":\n')
        print(f'Print the definition of "{front}":\n{answer}', file=output)

        if answer == definition:
            print("Correct!")
            print("Correct!", file=output)
        else:
            match_other = ""
            for other_term, other_value in cards.items():
                if answer == other_value["definition"]:
                    match_other = other_value
                    break

            if match_other:
                print(f'Wrong. The right answer is "{definition}", '
                      f'but your definition is correct for "{match_other}"')
                print(f'Wrong. The right answer is "{definition}", '
                      f'but your definition is correct for "{match_other}"', file=output)
            else:
                print(f'Wrong. The right answer is "{definition}".')
                print(f'Wrong. The right answer is "{definition}".', file=output)

            cards[front]["mistake"] += 1

        n_ask -= 1


def _exit(file_path):
    print("Bye bye!")
    print("Bye bye!", file=output)

    if file_path:
        export(file_path)

    quit()


def log():
    file_name = input("File name:\n").strip()
    print(f'File name:\n{file_name}', file=output)

    with open(file_name, "w") as opened_file:
        contents = output.getvalue()
        print(contents, file=opened_file)

    print("The log has been saved.")
    print("The log has been saved.", file=output)


def hardest_card():
    # find the highest mistake count and card lists
    highest = 0
    hard_card_list = []
    for term, value in cards.items():
        mistake = value["mistake"]
        if mistake == 0:
            continue
        elif mistake > highest:
            hard_card_list = [term]
            highest = mistake
        elif mistake == highest:
            hard_card_list.append(term)

    # give the results
    if not hard_card_list:
        print("There are no cards with errors.")
        print("There are no cards with errors.", file=output)

    elif len(hard_card_list) == 1:
        print(f'The hardest card is "{hard_card_list[0]}". You have {highest} errors answering it.')
        print(f'The hardest card is "{hard_card_list[0]}". You have {highest} errors answering it.', file=output)

    else:
        card_string = '", "'.join(hard_card_list)
        print(f'The hardest cards are "{card_string}". You have {highest} errors answering them.')
        print(f'The hardest cards are "{card_string}". You have {highest} errors answering them.', file=output)


def reset():
    for card, value in cards.items():
        value["mistake"] = 0
    print("Card statistics have been reset.")
    print("Card statistics have been reset.", file=output)


def main():
    parser = argparse.ArgumentParser(description="This program show flashcards and save your progress.")

    parser.add_argument("--import_from", help="Provide the file path of your progress.")
    parser.add_argument("--export_to", help="Prove the file path that you would like to save your progress.")

    args = parser.parse_args()

    if args.import_from:
        _import(args.import_from)

    while True:
        func = input("\nInput the action "
                     "(add, remove, import, export, ask, exit, log, hardest card, reset stats)\n").strip().lower()
        print(f'\nInput the action (add, remove, import, export, ask, exit, log, hardest card, reset stats)'
              f'\nFile name:\n{func}', file=output)

        if func == ADD:
            add()
        elif func == REMOVE:
            remove()
        elif func == IMPORT:
            file_name = input("File name:\n").strip()
            print(f'File name:\n{file_name}', file=output)

            _import(file_name)
        elif func == EXPORT:
            file_name = input("File name:\n").strip()
            print(f'File name:\n{file_name}', file=output)

            export(file_name)
        elif func == ASK:
            ask()
        elif func == EXIT:
            _exit(args.export_to)
        elif func == LOG:
            log()
        elif func == HARDEST_CARD:
            hardest_card()
        elif func == RESET:
            reset()


if __name__ == "__main__":
    main()
