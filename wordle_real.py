import random
from wordle_wordlist import get_word_list

def get_feedback(guess: str, secret_word: str) -> str:
    guessUpper = guess.upper()
    guessList = list(guessUpper) #turn guess into list so we can check with secret word later
    secretList = list(secret_word)
    feedBack = [] #stores clues for later

    if len(guess)!=5 or guessUpper not in get_word_list():
        return 'This is an invalid word. Guess again!'
    else: 
        #only checks if guessed letter is in the right place
        for i in range(len(guessList)):
            if guessList[i] == secretList[i]:
                secretList[i] = '*' #to prevent repeating this step later for that letter
                feedBack.append(guessList[i]) #adds correct letter to clues
            else:
                feedBack.append("-") #else the letter doesn't match so feedback there is empty

        for i in range(len(guessList)):
            #feedback only has "-" if the letter position isn't the same 
            if feedBack[i] == "-":
                if guessList[i] in secretList:
                    if secretList[secretList.index(guessList[i])] != guessList[secretList.index(guessList[i])]:
                        feedBack[i] = guessList[i].lower()
                        secretList[secretList.index(guessList[i])] = "*" 
    return ''.join(feedBack) #return feedback as a string



word_list_global = set(get_word_list()) #all possible words
not_guessed_list = get_word_list()
invalid_indexes = {'A':set(), 'B':set(), 'C':set(), 'D':set(), 'E':set(), 'F':set(), 'G':set(), 'H':set(), 'I':set(), 
                   'J':set(), 'K':set(), 'L':set(), 'M':set(), 'N':set(), 'O':set(), 'P':set(), 'Q':set(), 'R':set(), 
                   'S':set(), 'T':set(), 'U':set(), 'V':set(), 'W':set(), 'X':set(), 'Y':set(), 'Z':set()}
scrabble_dict = {'A': 9, 'B': 2, 'C': 2, 'D': 4, 'E': 12, 'F': 2,
    'G': 3, 'H': 2, 'I': 9, 'J': 1, 'K': 1, 'L': 4, 'M': 2, 'N': 6,
    'O': 8, 'P': 2, 'Q': 1, 'R': 6, 'S': 4, 'T': 6, 'U': 4, 'V': 2,
    'W': 2, 'X': 1, 'Y': 2, 'Z': 1 }
confirmed_list = ['-','-','-','-','-']
lowercase_set = set()

def get_AI_guess(guesses: list[str], feedback: list[str]) -> str:
    global word_list_global, invalid_indexes, scrabble_dict, confirmed_list
    deleted = set() #so we dont need to check these words again. saves time
    max_score = 0 #best score becomes guess
    final_word = ''
    
    if len(guesses) == 0: #first guess
        return 'SIREN'
    elif len(guesses) >= 1: #second guess beyond
        for i in range(5):
            if feedback[-1][i] == '-' and len(invalid_indexes[guesses[-1][i]]) == 0 \
                and guesses[-1][i] not in confirmed_list: #update invalid_indexes with every index for letters not in word
                for x in range(len(feedback)):
                    if guesses[-1][i] not in feedback[x] and x == len(feedback)-1:
                        invalid_indexes[guesses[-1][i]].update([0,1,2,3,4])
            elif ord(feedback[-1][i]) >= 65 and ord(feedback[-1][i]) <= 90: #if upper case, add to confirmed list
                confirmed_list[i] = feedback[-1][i]
                lowercase_set.add(feedback[-1][i].upper())
            else: #if lowercase, update invalid indexess
                invalid_indexes[guesses[-1][i]].add(i)
                lowercase_set.add(feedback[-1][i].upper())
    if feedback[0] == '-----' and len(guesses) == 1:
        return 'ABOUT'
    for word in word_list_global:
        score = 0
        for index in range(len(word)):
            if (confirmed_list[index] != '-' and confirmed_list[index] != word[index]): #checks if the word fits our clues
                deleted.add(word)
                break
            elif (index in invalid_indexes[word[index]]):
                deleted.add(word)
                break
            else:
                for valid_letter in lowercase_set:
                    if valid_letter in word:
                        score += scrabble_dict[word[index]]
        if score > max_score:
            max_score = score
            final_word = word

    word_list_global = word_list_global.difference(deleted)
    return final_word



def start_game():
    print("WELCOME TO WORDLE")
    num_guesses = 0
    secret_word = word_generator()
    winner = False
    guesses = []
    while num_guesses < 6 and winner == False:
        guess = input("Please enter your guess: ")
        result = get_feedback(guess, secret_word)
        if result != 'This is an invalid word. Guess again!':
            num_guesses += 1
            guesses.append(result)
            for i in guesses:
                print(i)
        else:
            print(result)
            
        if result == secret_word:
            winner = True
    if winner == False:
        print("YOU LOST THE GAME!!")
        print(f"The secret word was {secret_word}.")
    else:
        print(f"YOU WON THE GAME IN {num_guesses} GUESSES!")
    
    start_over = input("Do you want to play again? Y/N ")
    if start_over.upper() == 'Y':
        return start_game()
    else:
        print("THANKS FOR PLAYING!")
    

def word_generator():
    word = not_guessed_list[random.randint(0, len(not_guessed_list)-1)]
    not_guessed_list.remove(word)
    return word

def ai_game():
    global word_list_global, invalid_indexes, scrabble_dict, confirmed_list

    guess_count = 0
    secret_word = word_generator()
    #print(f"secret word: {secret_word}")
    guesses = []
    feedback_list = []

    while guess_count < 6:
        AI_guess = get_AI_guess(guesses, feedback_list)
        guesses.append(AI_guess)
        feedback_list.append(get_feedback(AI_guess, secret_word))
        guess_count += 1

        if AI_guess == secret_word:
            break
    invalid_indexes = {'A':set(), 'B':set(), 'C':set(), 'D':set(), 'E':set(), 'F':set(), 'G':set(), 'H':set(), 'I':set(), 
                   'J':set(), 'K':set(), 'L':set(), 'M':set(), 'N':set(), 'O':set(), 'P':set(), 'Q':set(), 'R':set(), 
                   'S':set(), 'T':set(), 'U':set(), 'V':set(), 'W':set(), 'X':set(), 'Y':set(), 'Z':set()}
    confirmed_list = ['-','-','-','-','-']
    word_list_global = set(get_word_list())
    #print(feedback_list)
    #print(guesses)
    if guess_count <=6: return guess_count
    else: return 7

if __name__ == "__main__":
    #start_game()
    
    total_guesses = 0
    sum_of_guesses = 0
    for count in range(len(not_guessed_list)):
       sum_of_guesses += ai_game()
       total_guesses += 1
    avg = sum_of_guesses/total_guesses
    print(f"average guesses: {avg}")   
    #print(ai_game())

