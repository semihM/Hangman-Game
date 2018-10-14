# =============================================================================
# Hangman Game
# =============================================================================
"""

A basic hangman game without any visual effects which you can play by yourself or
against a friend! 

Make sure you have your own API key and ID which you can get for free from:
https://developer.oxforddictionaries.com/

If you want to play on your own, current version doesn't have online dictionary
dataset to pick words from. You can use the small collection of words shared on
the repository among the main script.

Find "wordsdir" variable and change it to the dataset's directory you are going 
to use (Not tested for any file extensions other than ".txt")

Please consider sharing issues or improvements on the functions and have fun!

"""
# =============================================================================
# DEPENDENCIES
# =============================================================================
import random
import string
import requests
import json

# =============================================================================
#  LOAD AND CHOOSE FROM LOCAL WORDS     
# =============================================================================
def loadWords(directory,lim=1):
    """
    Returns a list filled with words
    """
    #IMPORTING WORDS' FILE
    filedir = open(directory, 'r')
    lines = filedir.readline()
    wordlist = lines.split()
    filteredlist=list()
    filteredlist=[wordlist[c] for c in range(len(wordlist)) if len(wordlist[c])>=lim]
    #print(len(filteredlist), " words loaded.")
    return filteredlist


def chooseWord(wordlist):
    """
    Returns a randomly choosen word from the given list 
    """
    return random.choice(wordlist)

# =============================================================================
# OXFORD DICTIONARIES API 
# =============================================================================
# http://docs.python-requests.org/en/master/user/install/#install
    
def apistuff(word,api_id,api_key):
    """
    Sends a http request through the oxforddictionaries API to get the word's definition
    word: secret word,
    api_id: your app id
    api_key: your app key
    
    """
    #Getting required keys etc.
    
    app_id=api_id #Your app_id from oxforddictionaries
    app_key=api_key #Your app_key from oxforddictionaries
    language='en'
    secretWord=word
    word_id = secretWord
    
    
    #Creating the url and making it accessible outside
    
    global __url__
    __url__ = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id
    req = requests.get(__url__, headers = {'app_id':app_id, 'app_key':app_key})
    return req


def getHint(req):
    """
    Uses the request to display the desired part of the json file recieved
    If status code is 200, prints the definition
    Else prints the error code and quits the process
    """
    try:      
        if req.status_code==200:
    #        ["results"][0]["lexicalEntries"][0]["entries"]["senses"][0]["definitions"]
    #        print("code {}\n".format(req.status_code))
    #        print("text \n" + r.text)["senses"][0]["definitions"]
    
            #Loading data in JSON format and iterating through to find definition   
            json_string = json.dumps(req.json())
            datastore = json.loads(json_string)
            a=datastore["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
            return a
        else:
            print("ERROR CODE: ",req.status_code)
            print("Sorry couldn't find a hint!")
            return None
    except:
        print("Sorry, an unexpected error occured!")
        
# =============================================================================
# INPUT FUNCTIONS
# =============================================================================
def getInput():
    """
    Gets input 1 or 2 to start a game
    """
    gettingInput=True
    
    while gettingInput:
        try:
            #Get input to set the game
            f=int(input("Press 1 to play against your friends, press 2 to play by yourself! "))
            assert f==1 or f==2
        except:
            print("Enter 1 or 2 !")
        else:
            return f

#==============================================================================
# VALIDATIONS
# ============================================================================= 

def numberCheck(num,limit=25):
    """
    Gets 2 parameters,
    num for the comparison
    limit for the upper bound
    """
    try:
        num=int(num)
        limit=int(limit)
        if num>0 and num<=limit:
            return num
        else:
            num=input("Please enter a valid number ! ")
            return numberCheck(num,limit)
    except:
        num=input("Please enter a valid number ! ")
        return numberCheck(num,limit)
 
    
def wordCheck(word):
    """
    Checks the word's validity, returns True if valid, False if not
    """
    try:
        s=0
        l=list(word)
        for letter in l:
           if letter in string.ascii_lowercase and letter!="":
               s+=1    
        if s==len(str(word)) and s!=0:
            return True
        else:
            return False
    except:
     print("Invalid word!")

# =============================================================================
# WORD RELATED FUNCTIONS
# =============================================================================

def isWordGuessed(w,l):
    '''
    Gets a copy of the secret word as a list, and removes duplicated letters
    Compares each letter guessed to the secret word's letters
    '''
    copy=set(list(w))
    fnd=0
    for letters in l:
        if letters in copy:
            fnd+=1
#    print(len(secretWord),fnd)
    if len(copy)<=fnd:
        return True
    else: 
        return False    


def getGuessedPart(w, l):
    '''
    Prints underscore characters instead of secret word's letters
    If a letter is guessed, underscores turn into the actual letter
    '''
    copy=list(w)
    guessed=["_"]*len(copy)

    for ltr in l:
        index=0
        for b in range(len(copy)):
            if ltr==copy[b]:
               guessed[index]=w[index]  
            index+=1
#    print("".join(guessed))
    return " ".join(guessed)


def getAvailableLetters(l):
    """
    Returns a list of the letters left available to be guessed
    """
    lettersLeft=list(string.ascii_lowercase)

    for letter in l:
        if letter in lettersLeft:
            lettersLeft.remove(str(letter))
          
    return " ".join(lettersLeft) 
# =============================================================================
# GAME END/RESET FUNCTIONS
# =============================================================================
def gameEnded(during,later,w):
    """
    Gets  2 boolean values and the secret word as parameters:
    during = wheter or not if the player called for a hint during game
    later = wheter or not if the player called for a hint after the game ended
    w = the secret word which the player was trying to guess
    """
    print("")
    if during == False and later == False:
        print('Type "meaning" to get the dictionary meaning of the "',w,'".')
    gameEnd=input('Want to play again? Type "yes" or "no".')
    testing=True
    while testing:
        if gameEnd.lower()=="yes" or gameEnd.lower()=="no" or gameEnd.lower()=="meaning":
            testing=False
            return gameEnd.lower()
        else:
            gameEnd=input("Please enter a valid input! ")
 
def gameReset(word,guesses,r,ending):
    """
    Resets the parameters the main function takes
    word=secret word,
    guesses= number of guesses given to player
    r = http request
    ending = answer given after the game ends
    """
    del word,guesses,r,ending
   
# =============================================================================
# MAIN FUNCTION
# =============================================================================

def hangman(w,g,req):
    """
    w: string, the secret word to guess.
    g: amount of guesses to let user have.
    req=request code from API
    Starts up an interactive game of Hangman.
    """ 
    print("I am thinking of a word that is ",len(w)," letters long")
    print("-----------")
    guessesleft=g
    lettersGuessed=[]
    didHintGetCalled=False
    result=""
    #Keeps looping and getting inputs if you haven't found the answer and still have guesses
    while not isWordGuessed(w,lettersGuessed) and not guessesleft==0:
        
        if guessesleft==1:
                print("")
                print("You have 1 guesses left!")  
                if not didHintGetCalled:
                    print("You can type 'hint' to request the meaning of the word!")
        elif guessesleft>1:
                print("You have ",guessesleft," guesses left!")
        
        print("Available letters:",getAvailableLetters(lettersGuessed))
        letter=input("Please guess a letter:").lower()
        
        if letter == "hint" and guessesleft==1:
            print("*********************************************")
            print(getHint(req))
            if req.status_code==200:
                didHintGetCalled=True
            print("*********************************************")
            letter=input("Please guess a letter:").lower()
        
        #Conditioning the input to be in alphabeth
        while letter=="" or letter not in string.ascii_lowercase and letter !="hint":
                letter=input("Invalid character! Please guess a letter:").lower()
                if letter=="hint" and guessesleft==1:
                    print("*********************************************")
                    print(getHint(req))
                    if req.status_code==200:
                        didHintGetCalled=True
                    print("*********************************************")
                    letter=input("Please guess a letter:").lower()
                    isWordGuessed(w,lettersGuessed)    
            
        #Letter in secret word and not guessed yet 
        if letter in w and letter not in lettersGuessed:
            lettersGuessed.append(letter)
            isWordGuessed(w,lettersGuessed)
            print("Good guess: ",getGuessedPart(w,lettersGuessed))
            print("------------")
              
            
        #Letter already guessed
        elif letter in lettersGuessed:
            isWordGuessed(w,lettersGuessed)
            print("Oops! You've already guessed that letter: ",getGuessedPart(w,lettersGuessed))
            print("------------")

        #Letter is neither in secret word nor guessed yet     
        elif letter not in lettersGuessed and letter not in w:
                if letter!="hint":
                    isWordGuessed(w,lettersGuessed)
                    lettersGuessed.append(letter)
                    guessesleft-=1
                    print("Oops! That letter is not in my word: ",getGuessedPart(w,lettersGuessed))                  
                    print("------------")
                    
                    
        #Check if the word is guessed while you still have guesses and not in demand of a hint        
        if isWordGuessed(w,lettersGuessed) and guessesleft>=0 and letter!="hint":
            #You won!     
            if g-guessesleft==0:
                print("Congratulations, you guessed the word '",w,"' and won by doing no mistakes!")
                result="victory"
            elif g-guessesleft==1:
                print("Congratulations, you guessed the word '",w,"' and won by doing only 1 mistake!")
                result="victory"
            else:
                print("Congratulations, you guessed the word '" ,w,"' and won by using "+str(g-guessesleft)+" guesses out of "+str(g)+"!")
                result="victory"
        #You lost!           
        elif not isWordGuessed(w,lettersGuessed) and guessesleft<1 and letter!="hint":
            print("Sorry, you ran out of guesses. The word was: ",w)
            result="loss"

    return {"game result":result,"secret word":w,"guessed letters":lettersGuessed[:],"mistakes made":g-guessesleft,"hint used? ":didHintGetCalled, "asked for hint later? ": False,"dictionary link":"https://en.oxforddictionaries.com/definition/"+str(w),"api link":__url__}


# =============================================================================
# CALLING FUNCTIONS AND CREATING NEEDED VARIABLES FOR LOOPS ETC.
# =============================================================================

#Get input to set the game
flag=getInput()
gamesPlayed=[]
gameIsOn=1
afterGame=0
asked=0
#CHANGE THIS TO YOUR DIRECTORY OF WORDS FILE
wordsdir="words.txt"
#THE LIST OF WORDS
allWords=loadWords(wordsdir,1)
# =============================================================================
# LOOPS UNTIL QUITTING
# =============================================================================
while gameIsOn:
    
    # =============================================================================
    # GAME TO PLAY AGAINST A PLAYER
    # =============================================================================
    while flag==1:
        try:
            secretWord=str(input("Enter the secret word! : ")).lower()
            assert wordCheck(secretWord)==True
        except:
            print("Please enter a valid word!")

        else:
            totalguesses=input("Enter the amount of guesses possible! : ")
            totalguesses=numberCheck(totalguesses)
            for i in range(45):
                print("____________________________________________________________________________________________________") 
            print("")
            #ENTER YOUR API KEY/ID HERE
            r=apistuff(secretWord,api_id="2fbfbe4f",api_key="e633c614e9eb48bee70d3ca3c662cc11")
            ###########################################
            
            lastGame=hangman(secretWord,totalguesses,r)
            afterGame=1            
            gamesPlayed.append(lastGame)
            hintused=gamesPlayed[-1]["hint used? "]
            hintlater=gamesPlayed[-1]["asked for hint later? "]
            gameEnd=gameEnded(hintused,hintlater,secretWord)        
            del i
            break
    # =============================================================================
    # GAME TO PLAY BY YOURSELF
    # ============================================================================= 
    while flag==2:
        try:
            #Getting words ready
            a=int(input("Enter the minimum length possible for a word(1-10):"))
            assert a>=1 and a<=10
        except:
            print("Enter a valid number!: ")
        else:
            print("")
            filteredList= loadWords(wordsdir,a)
            secretWord = str(chooseWord(filteredList))
            totalguesses=random.randint(6,11)
            
            #ENTER YOUR API KEY/ID HERE
            r=apistuff(secretWord,api_id="2fbfbe4f",api_key="e633c614e9eb48bee70d3ca3c662cc11")
            ###########################################
            
            lastGame=hangman(secretWord,totalguesses,r)
            gamesPlayed.append(lastGame)
            hintused=gamesPlayed[-1]["hint used? "]
            hintlater=gamesPlayed[-1]["asked for hint later? "]        
            gameEnd=gameEnded(hintused,hintlater,secretWord)
            afterGame=1
            #Remove the unnecessary variables
            del a,filteredList
            break
    # =============================================================================
    # GETTING INPUTS AFTER GAME   
    # =============================================================================
    while afterGame:                

        if gameEnd=="yes":
            #Start the input loop to select a game mode
            gameIsOn=1
            #Prevent the loop
            afterGame=0
            asked=0
            gameReset(secretWord,totalguesses,r,gameEnd)
            #Get game mode input
            flag=getInput()
        elif gameEnd=="no":
            gameReset(secretWord,totalguesses,r,gameEnd)
            print("")
            print("Come back any time to play again!")
            gameIsOn=0
            break
        elif gameEnd=="meaning" :
            if not lastGame["hint used? "] and asked==0:
                print("")
                print("Word '",secretWord,"' means: ",getHint(r),".")
                asked=1
                lastGame["asked for hint later? "]=True
                hintused=gamesPlayed[-1]["hint used? "]
                hintlater=gamesPlayed[-1]["asked for hint later? "]   
                gameEnd=gameEnded(hintused,hintlater,w=secretWord)
            else:
                print("You already called for the meaning!")
                gameEnd=input("Please type 'yes' to play again or 'no' to quit! ")
        else:
            gameEnd=input("Please enter a valid input! ")
            
# =============================================================================
# REMOVE REMANING LOCAL UNNECESSARY VARIABLES
# =============================================================================
try:
    del asked,flag,gameEnd,gameIsOn,afterGame,totalguesses,secretWord,lastGame,hintlater,hintused,wordsdir
except NameError:
    print("Couldn't delete the variables!")
# =============================================================================
# Links:
#            https://en.oxforddictionaries.com/
#            https://developer.oxforddictionaries.com/
# =============================================================================


