import random
import time

class colors:
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
class shades:
    BLACK = '\033[0m'
    #BOLD = '\033[1m'
    STRIKE = '\u0336'
    UNDERLINE = '\033[4m'

colour = ["red","blue","yellow"]
pcolour = [colors.RED,colors.BLUE,colors.YELLOW]

shape = ["O","U","V"]
pshape = ['O','U','V']

number = ["one","two","three"]
pnumber = [1,2,3]

shade = ["empty","striped","underline"]
pshade = [shades.BLACK,shades.STRIKE,shades.UNDERLINE]

categories = [pshade, pcolour, pshape, pnumber]

def makeCards():
    cards = []
    while (len(cards) < 12):
        card = []  
        for category in categories:
            variable = random.choice(category)
            card.append(variable)
        if (card not in cards):
            cards.append(card)
    
    #bol, car1, car2, car3 = setInCards(cards)
    #If there's no set, add more cards
    while (not setInCards(cards)): 
        add3(cards)
    return cards

def add3(cards): 
    #If there's no set, make another 3 that are different from cards
    j = 0
    while (j<3): #while we've added less than 3 cards
        card = []  
        
        for category in categories:
            variable = random.choice(category)
            card.append(variable)
        if (card not in cards): #If card is not a repeat, add it
            cards.append(card)
            j+=1
    while (not setInCards(cards)): 
        add3(cards)

def printCard(card): #Returns the string to be printed
    n = card[3]
    return (shades.BLACK+card[0]+card[1]+card[2])*n
    
def printCards(cards):
    i=0
    while (i<(len(cards)-2)):
        print(shades.BLACK, i, printCard(cards[i]),
             shades.BLACK, i+1, printCard(cards[i+1]),
             shades.BLACK, i+2, printCard(cards[i+2]))
        i += 3

def isSet(card1, card2, card3):
    if (card1 == card2 == card3): #Make sure they're not all the same card
        return False
    falsified = True
    for i in range (4):
        if (not((card1[i] == card2[i] == card3[i]) or #All are the same 
                (card1[i] != card2[i] != card3[i] != card1[i]))): #All are different
            falsified = False
    
    return falsified

def check3(n1,n2,n3, cards):
    return isSet(cards[n1],cards[n2],cards[n3])   

def setInCards(cards):
    for c1 in cards:
        for c2 in cards:
            for c3 in cards:
                if (isSet(c1,c2,c3) and c1!=c2!=c3):
                    return True,c1,c2,c3
    return False

def showSet(cards):
    bol, car1, car2, car3 = setInCards(cards)
    print(shades.BLACK,"Set in these cards: ", printCard(car1)
          ,printCard(car2),printCard(car3))


#Returns true, false and card indexes or a print statement revealing the set
def oneRound(cards):
    inp = input("What 3 cards make a set? ")
    if (inp.lower() == "help"):
        return showSet(cards), "help"
    else:
        n1,n2,n3 = inp.split() #can try, catch a value error to catch input
        return check3(int(n1),int(n2),int(n3), cards), [n1,n2,n3]
    
def fullRound(cards):    
    foundSet = False, False
    while (not foundSet[0]):
        foundSet = oneRound(cards)
        if (type(foundSet[0])!=bool): #If help was pressed
            #Don't increase the score, but remove these cards and add new ones
            return False, False
        
        if (foundSet[0]): #If found, return True 
            return True, foundSet[1] 
            break
        #And if it's false, try again
        print("Try again")

def gamePlay():
    rounds = int(input("How many sets should you find to win? "))
    score = 0
    cards = makeCards()
    #Measure start time
    pre = time.perf_counter()
    
    while(score<rounds):
        print(shades.BLACK, "Score = ", score)
        printCards(cards) 
        thisRound = fullRound(cards) 
        if (thisRound[0]): #This can't be evaluated if it
            print("Correct!")
            score += 1 
            cardsToRemove = [cards[int(thisRound[1][0])],
                             cards[int(thisRound[1][1])],cards[int(thisRound[1][2])]]
        else: #If fullRound is false, then the cards to remove are known
            bol, car1, car2, car3 = setInCards(cards)
            cardsToRemove = [car1, car2, car3]
            
            #Don't remove cards if it was just a wrong guess
    
        for card in cardsToRemove:
            cards.remove(card)
            
        if (len(cards)<12 or not setInCards(cards)): #If there is less than 12 cards or (there are more than 12 and) there is no set
            add3(cards)
        
        #Measure end time
        post = time.perf_counter()
    print("Congratulations! You found", rounds, f"sets in {post - pre:0.2f} seconds")

gamePlay()
