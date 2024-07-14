from pyswip import Prolog
import re

prolog = Prolog()
prolog.consult("resources/rules.pl")

# Main function for pattern matching and interaction
def pattern_matching():
    #   Statements
    statements = [r"(\w+) and (\w+) are siblings.", r"(\w+) is a sister of (\w+).", r"(\w+) is the mother of (\w+).",
                  r"(\w+) is a grandmother of (\w+).", r"(\w+) is a child of (\w+).", r"(\w+) is a daughter of (\w+).",
                  r"(\w+) is an uncle of (\w+).", r"(\w+) is a brother of (\w+).", r"(\w+) is the father of (\w+).",
                  r"(\w+) and (\w+) are the parents of (\w+).", r"(\w+) is a grandfather of (\w+).",
                  r"(.+?) are children of (.+?)\.", r"(\w+) is a son of (\w+).", r"(\w+) is an aunt of (\w+)."]

    #   Questions
    questions = [r"are (\w+) and (\w+) siblings?", r"is (\w+) a sister of (\w+)?", r"is (\w+) a brother of (\w+).?",
                 r"is (\w+) the mother of (\w+)?", r"is (\w+) the father of (\w+)?", r"are (\w+) and (\w+) the parents of (\w+)?",
                 r"is (\w+) a grandmother of (\w+)?", r"is (\w+) a daughter of (\w+)?", r"is (\w+) a son of (\w+)?",
                 r"is (\w+) a child of (\w+)?", r"who are the children of (\w+)?", r"is (\w+) an uncle of (\w+)?",
                 r"who are the siblings of (\w+)?", r"who are the sisters of (\w+)?", r"who are the brothers of (\w+)?",
                 r"who is the mother of (\w+)?", r"who is the father of (\w+)?", r"who are the parents of (\w+)?",
                 r"is (\w+) a grandfather of (\w+)?", r"who are the daughters of (\w+)?", r"who are the sons of (\w+)?",
                 r"are (.+?) children of (.+?)\?", r"is (\w+) an aunt of (\w+)?", r"are (\w+) and (\w+) relatives?"]

    while 1:
        #   User input (converts to lowercase and removes whitespaces)
        prompt = input("Hello! How can I help you? ").lower().strip()

        is_match = False

        #   If prompt is a statement
        if prompt[-1] == '.':

            #   Checks if pattern matches the statement prompts
            for i in range(len(statements)):
                #   Adds the names to a list
                match = re.search(statements[i], prompt)

                #   If pattern matches, program runs prolog statements
                if match:
                    is_match = True
                    statement_prolog(match, i)

        #   If prompt is a question
        elif prompt[-1] == '?':

            #   Checks if pattern matches the question prompts
            for i in range(len(questions)):

                #   Adds the names to a list
                match = re.search(questions[i], prompt)

                #   If pattern matches, program runs prolog statements
                if match:
                    is_match = True
                    question_prolog(match, i)
                    break

        #   If there's no match
        if is_match is False:
            print("Invalid prompt. Please try again.")


# Checks statement logic
def statement_prolog(match, i):
    is_valid = False

    match i:
        case 0: # Sibling assertion
            sibling_of_1 = f'sibling_of({match.group(1)},{match.group(2)})'
            sibling_of_2 = f'sibling_of({match.group(2)},{match.group(1)})'
            prolog.assertz(sibling_of_1)
            prolog.assertz(sibling_of_2)

            is_valid = bool(list(prolog.query(f'siblings({match.group(1)},{match.group(2)})')))

        case 1: # Sister assertion
            female = f'female({match.group(1)})'
            male = f'male({match.group(1)})'
            sibling_of_1 = f'sibling_of({match.group(1)},{match.group(2)})'
            sibling_of_2 = f'sibling_of({match.group(2)},{match.group(1)})'

            if (bool(list(prolog.query(female))) or bool(list(prolog.query(male)))) is False:
                prolog.assertz(female)
            prolog.assertz(sibling_of_1)
            prolog.assertz(sibling_of_2)

            is_valid = bool(list(prolog.query(f'sister_of({match.group(1)},{match.group(2)})')))

        case 2: # Mother assertion
            female = f'female({match.group(1)})'
            male = f'male({match.group(1)})'
            parent_of = f'parent_of({match.group(1)},{match.group(2)})'

            if (bool(list(prolog.query(female))) or bool(list(prolog.query(male)))) is False:
                prolog.assertz(female)

            prolog.assertz(parent_of)

            is_valid = bool(list(prolog.query(f'mother_of({match.group(1)},{match.group(2)})')))

        case 3: # Grandmother assertion
            female = f'female({match.group(1)})'
            male = f'male({match.group(1)})'
            mother_of = f'mother_of({match.group(1)},X)'
            parent_of = f'parent_of(X,{match.group(2)})'

            if (bool(list(prolog.query(female))) or bool(list(prolog.query(male)))) is False:
                prolog.assertz(female)
            prolog.assertz(mother_of)
            prolog.assertz(parent_of)

            is_valid = bool(list(prolog.query(f'grandmother_of({match.group(1)},{match.group(2)})')))

        case 4: # Child assertion
            parent_of = f'parent_of({match.group(2)},{match.group(1)})'

            prolog.assertz(parent_of)

            is_valid = bool(list(prolog.query(f'child_of({match.group(1)},{match.group(2)})')))
            
        case 5: # Daughter assertion
            female = f'female({match.group(1)})'
            male = f'male({match.group(1)})'
            parent_of = f'parent_of({match.group(2)},{match.group(1)})'

            if (bool(list(prolog.query(female))) or bool(list(prolog.query(male)))) is False:
                prolog.assertz(female)
            prolog.assertz(parent_of)

            is_valid = bool(list(prolog.query(f'daughter_of({match.group(1)},{match.group(2)})')))
        
        case 6: # Uncle assertion
            male = f'male({match.group(1)})'
            female = f'female({match.group(1)})'
            parent_of = f'parent_of(X,{match.group(2)})'
            brother_of = f'brother_of({match.group(1)}, X)'

            if (bool(list(prolog.query(female))) or bool(list(prolog.query(male)))) is False:
                prolog.assertz(male)
            prolog.assertz(parent_of)
            prolog.assertz(brother_of)

            is_valid = bool(list(prolog.query(f'uncle_of({match.group(1)},{match.group(2)})')))

        case 7: # Brother assertion
            male = f'male({match.group(1)})'
            female = f'female({match.group(1)})'
            sibling_of_1 = f'sibling_of({match.group(1)},{match.group(2)})'
            sibling_of_2 = f'sibling_of({match.group(2)},{match.group(1)})'

            if (bool(list(prolog.query(female))) or bool(list(prolog.query(male)))) is False:
                prolog.assertz(male)
            prolog.assertz(sibling_of_1)
            prolog.assertz(sibling_of_2)

            is_valid = bool(list(prolog.query(f'brother_of({match.group(1)},{match.group(2)})')))

        case 8: # Father assertion
            male = f'male({match.group(1)})'
            female = f'female({match.group(1)})'
            parent_of = f'parent_of({match.group(1)},{match.group(2)})'

            if (bool(list(prolog.query(female))) or bool(list(prolog.query(male)))) is False:
                prolog.assertz(male)
            prolog.assertz(parent_of)

            is_valid = bool(list(prolog.query(f'father_of({match.group(1)},{match.group(2)})')))

        case 9: # Parents assertion
            parent_of_1 = f'parent_of({match.group(1)},{match.group(3)})'
            parent_of_2 = f'parent_of({match.group(2)},{match.group(3)})'

            if bool(list(prolog.query(f'parent_of(X,{match.group(3)})'))) is False and \
                (match.group(1) != match.group(2)) and (match.group(2) != match.group(3)) and (match.group(1) != match.group(3)):
                prolog.assertz(parent_of_1)
                prolog.assertz(parent_of_2)

            is_valid = bool(list(prolog.query(f'(parent_of({match.group(1)},{match.group(3)}) , parent_of({match.group(2)},{match.group(3)}))')))

        case 10: # Grandfather assertion
            male = f'male({match.group(1)})'
            female = f'female({match.group(1)})'
            parent_of_1 = f'parent_of({match.group(1)},X)'
            parent_of_2 = f'parent_of(X,{match.group(2)})'

            if (bool(list(prolog.query(female))) or bool(list(prolog.query(male)))) is False:
                prolog.assertz(male)
            prolog.assertz(parent_of_1)
            prolog.assertz(parent_of_2)

            is_valid = bool(list(prolog.query(f'grandfather_of({match.group(1)},{match.group(2)})')))

        case 11: # Children assertion
            child_input = match.group(1)
            parent = match.group(2)

            children = [child.strip() for child in re.split(r',\s*|\s+and\s*|\s+', child_input) if
                        child.lower() != 'and']

            if parent not in children:
                if len(set(children)) == len(children):
                    is_valid = True  # Assume it's valid unless proven otherwise

                    for child in children:
                        if bool(list(prolog.query(f'relatives(\'{child}\', \'{parent}\')'))):
                            is_valid = False
                            break
                        else:
                            continue

                    if is_valid:
                        for child in children:
                            prolog.assertz(f'child_of(\'{child}\', \'{parent}\')')

        case 12: # Son assertion
            male = f'male({match.group(1)})'
            female = f'female({match.group(1)})'
            parent_of = f'parent_of({match.group(2)},{match.group(1)})'

            if (bool(list(prolog.query(female))) or bool(list(prolog.query(male)))) is False:
                prolog.assertz(male)
            prolog.assertz(parent_of)

            is_valid = bool(list(prolog.query(f'son_of({match.group(1)},{match.group(2)})')))

        case 13: # Aunt assertion
            female = f'female({match.group(1)})'
            male = f'male({match.group(1)})'
            parent_of = f'parent_of(X,{match.group(2)})'
            sister_of = f'sister_of({match.group(1)}, X)'

            if (bool(list(prolog.query(female))) or bool(list(prolog.query(male)))) is False:
                prolog.assertz(female)
            prolog.assertz(parent_of)
            prolog.assertz(sister_of)

            is_valid = bool(list(prolog.query(f'aunt_of({match.group(1)},{match.group(2)})')))

    # Chatbot replies
    if is_valid is False:
        print("That's impossible!")
    else:
        print("OK! I learned something.")


# Function to list relations based on a Prolog query
def list_relation(match, relation):
    # Set to keep track of past values to avoid duplicates
    past_values = set()

    # Results for the specified relation
    results = list(prolog.query(f"{relation}(Y, {match.group(1)})"))

    # If there is no relationship
    if not results:
        print("None.")

    # Iterate through the results and print unique values
    for p in results:
        if p is not None and p["Y"] is not None and p["Y"] not in past_values:
            past_values.add(p["Y"])
            print(p["Y"].capitalize())

# Checks question logic
def question_prolog(match, i):
    is_true = None

    match i:
        case 0: # Sibling question
            print("are siblings?")
            is_true = bool(list(prolog.query(f'siblings({match.group(1)},{match.group(2)})')))

        case 1: # Sister question
            print("is sister?")
            is_true = bool(list(prolog.query(f'sister_of({match.group(1)},{match.group(2)})')))

        case 2: # Brother question
            print("is brother?")
            is_true = bool(list(prolog.query(f'brother_of({match.group(1)},{match.group(2)})')))

        case 3: # Mother question
            print("is mother?")
            is_true = bool(list(prolog.query(f'mother_of({match.group(1)},{match.group(2)})')))

        case 4: # Father question
            print("is father?")
            is_true = bool(list(prolog.query(f'father_of({match.group(1)},{match.group(2)})')))

        case 5: # Parents question
            print("are parents?")
            is_true = bool(list(prolog.query(f'(parent_of({match.group(1)},{match.group(3)}) , parent_of({match.group(2)},{match.group(3)}))')))

        case 6: # Grandmother question
            print("is grandmother?")
            is_true = bool(list(prolog.query(f'grandmother_of({match.group(1)},{match.group(2)})')))

        case 7: # Daughter question
            print("is daughter?")
            is_true = bool(list(prolog.query(f'daughter_of({match.group(1)},{match.group(2)})')))

        case 8: # Son question
            print("is son?")
            is_true = bool(list(prolog.query(f'son_of({match.group(1)},{match.group(2)})')))

        case 9: # Child question
            print("is child?")
            is_true = bool(list(prolog.query(f'child_of({match.group(1)},{match.group(2)})')))

        case 21:  # Children question
            print("are children?")

            child_input = match.group(1)
            parent = match.group(2)

            children = [child.strip() for child in re.split(r',\s*|\s+and\s*|\s+', child_input) if
                        child.lower() != 'and']

            is_true = True
            if parent not in children:
                if len(set(children)) == len(children):
                    for child in children:
                        if bool(list(prolog.query(f'child_of(\'{child}\', \'{parent}\')'))) is False:
                            is_true = False

        case 11: # Uncle question
            print("is uncle?")
            is_true = bool(list(prolog.query(f'uncle_of({match.group(1)},{match.group(2)})')))

        case 12: # Siblings list
            list_relation(match, "siblings")

        case 13: # Sisters list
            list_relation(match, "sister_of")

        case 14: # Brothers list
            list_relation(match, "brother_of")

        case 15: # Mother list
            list_relation(match, "mother_of")

        case 16: # Father list
            list_relation(match, "father_of")

        case 17: # Parents list
            list_relation(match, "parent_of")

        case 18: # Grandfather question
            print("is grandfather?")
            is_true = bool(list(prolog.query(f'grandfather_of({match.group(1)},{match.group(2)})')))

        case 19: # Daughters list
            list_relation(match, "daughter_of")

        case 20: # Sons list
            list_relation(match, "son_of")

        case 10: # Children list
            list_relation(match, "child_of")

        case 22: # Aunt question
            print("is aunt?")
            is_true = bool(list(prolog.query(f'aunt_of({match.group(1)},{match.group(2)})')))

        case 23: # Relatives question
            print("are they relatives?")
            is_true = bool(list(prolog.query(f'relatives({match.group(1)},{match.group(2)})')))

    # Chatbot replies
    if is_true is not None:
        if is_true is False:
            print("No.")
        else:
            print("Yes.")

def main():
    print("Welcome to the chatbot!")
    pattern_matching()


if __name__ == "__main__":
    main()
