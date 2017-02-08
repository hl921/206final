import random
import unittest

# SI 206 Winter 2017
# Homework 2 - Code

##COMMENT YOUR CODE WITH:
# Section Day/Time: Thursday 3pm
# People you worked with: 

######### DO NOT CHANGE PROVIDED CODE #########
### Below is the same cards.py code you saw in lecture.
### Scroll down for assignment instructions.
#########

class Card(object):
	suit_names =  ["Diamonds","Clubs","Hearts","Spades"]
	rank_levels = [1,2,3,4,5,6,7,8,9,10,11,12,13]
	faces = {1:"Ace",11:"Jack",12:"Queen",13:"King"}

	def __init__(self, suit=0, rank=2):
		self.suit = self.suit_names[suit]
		if rank in self.faces: # self.rank handles printed representation
			self.rank = self.faces[rank]
		else:
			self.rank = rank
		self.rank_num = rank # To handle winning comparison 

	def __str__(self):
		return "{} of {}".format(self.rank,self.suit)

class Deck(object):
	def __init__(self): # Don't need any input to create a deck of cards
		# This working depends on Card class existing above
		self.cards = []
		for suit in range(4):
			for rank in range(1,14):
				card = Card(suit,rank)
				self.cards.append(card) # appends in a sorted order

	def __str__(self):
		total = []
		for card in self.cards:
			total.append(card.__str__())
		# shows up in whatever order the cards are in
		return "\n".join(total) # returns a multi-line string listing each card

	def pop_card(self, i=-1):
		# removes and returns a card from the Deck
		# default is the last card in the Deck
		return self.cards.pop(i) # this card is no longer in the deck -- taken off

	def shuffle(self):
		random.shuffle(self.cards)

	def replace_card(self, card):
		card_strs = [] # forming an empty list
		for c in self.cards: # each card in self.cards (the initial list)
			card_strs.append(c.__str__()) # appends the string that represents that card to the empty list 
		if card.__str__() not in card_strs: # if the string representing this card is not in the list already
			self.cards.append(card) # append it to the list

	def sort_cards(self):
		# Basically, remake the deck in a sorted way
		# This is assuming you cannot have more than the normal 52 cars in a deck
		self.cards = []
		for suit in range(4):
			for rank in range(1,14):
				card = Card(suit,rank)
				self.cards.append(card)


def play_war_game(testing=False):
	# Call this with testing = True and it won't print out all the game stuff -- makes it hard to see test results
	player1 = Deck()
	player2 = Deck()

	p1_score = 0
	p2_score = 0

	player1.shuffle()
	player2.shuffle()
	if not testing:
		print("\n*** BEGIN THE GAME ***\n")
	for i in range(52):
		p1_card = player1.pop_card()
		p2_card = player2.pop_card()
		if not testing:
			print("Player 1 plays", p1_card,"& Player 2 plays", p2_card)

		if p1_card.rank_num > p2_card.rank_num:
			if not testing:
				print("Player 1 wins a point!")
			p1_score += 1
		elif p1_card.rank_num < p2_card.rank_num:
			if not testing:
				print("Player 2 wins a point!")
			p2_score += 1
		else:
			if not testing:
				print("Tie. Next turn.")

	if p1_score > p2_score:
		return "Player1", p1_score, p2_score
	elif p2_score > p1_score:
		return "Player2", p1_score, p2_score
	else:
		return "Tie", p1_score, p2_score

if __name__ == "__main__":
	result = play_war_game()
	print("""\n\n******\nTOTAL SCORES:\nPlayer 1: {}\nPlayer 2: {}\n\n""".format(result[1],result[2]))
	if result[0] != "Tie":
		print(result[0], "wins")
	else:
		print("TIE!")


######### DO NOT CHANGE CODE ABOVE THIS LINE #########

## You can write any additional debugging/trying stuff out code here... 
## OK to add debugging print statements, but do NOT change functionality of existing code.
## Also OK to add comments!

#########

### Write unit tests below this line for the cards code above.
### You should include tests for the following described cases.
### You must test at least 2 additional cases that you decide on, but you may also add more additional tests if you want to.
### You may create as many or few unittest.TestCase subclasses as you like. 
### You must arrange your code so that if you were to fail a test, that would not cause any other tests to fail as a result of that test failing. (See lecture notes.)

### IMPORTANT: IF YOU INVOKE THE play_war_game FUNCTION IN A TEST CASE, YOU MUST INVOKE IT WITH THE PARAMETER testing=True, like this:
### play_war_game(testing=True) AS OPPOSED TO play_war_game()
### If you do not do that, we will not be able to grade your homework properly!

### You may assume that other programmers will NOT invoke these functions with unacceptable inputs (e.g. no one will try to create a card with rank 0). You just need to ensure that the code works as intended.

##**##**##**##@##**##**##**## # DO NOT CHANGE OR DELETE THIS COMMENT LINE -- we use it for grading your file
###############################################
class Testing(unittest.TestCase):
## Test that if you create a card with rank 12, its rank will be "Queen"
	def test_1(self):
		q = Card(rank=12)
		self.assertEqual("Queen", q.rank)
## Test that if you create a card with rank 1, its rank will be "Ace"
	def test_2(self):	
		a = Card(rank=1)
		self.assertEqual("Ace", a.rank)
## Test that if you create a card instance with rank 3, its rank will be 3
	def test_3(self):
		e = Card(suit=0, rank=3)
		self.assertEqual(e.rank, 3)
## Test that if you create a card instance with suit 1, it will be suit "Clubs"
	def test_4(self):
		f = Card(suit=1, rank=2)
		self.assertEqual(f.suit, "Clubs")
## Test that if you create a card instance with suit 2, it will be suit "Hearts"
	def test_5(self):
		g = Card(suit=2, rank=2)
		self.assertEqual(g.suit, "Hearts")
## Test that if you create a card instance, it will have access to a variable suit_names that contains the list ["Diamonds","Clubs","Hearts","Spades"]
	def test_6(self):
		h = Card(suit=0, rank=2)
		self.assertEqual(type(h.suit_names),type([1,2]))
## Test that if you invoke the __str__ method of a card instance that is created with suit=2, rank=7, it returns the string "7 of Hearts"
	def test_7(self):
		i = Card(suit=2, rank=7)
		self.assertEqual(i.__str__(), "7 of Hearts")
## Test that if you create a deck instance, it will have 52 cards in its cards instance variable
	def test_8(self):
		j = Deck()
		self.assertEqual(len(j.cards), 52)
## Test that if you invoke the pop_card method on a deck, it will return a card instance.
	def test_9(self):
		k = Deck()
		i = Card(suit=0, rank=2)
		self.assertEqual(type(k.pop_card()), type(i)) #is this right????!?!?**** not sure
## Test that the return value of the play_war_game function is a tuple with three elements, the first of which is a string. (This will probably require multiple test methods!)
	def test_10a(self):
		l = play_war_game(testing=True)
		self.assertEqual(type(l), type((1,2,3)))
	def test_10b(self):
		l = play_war_game(testing=True)
		self.assertEqual(len(l), 3)
	def test_10c(self):
		l = play_war_game(testing=True)
		self.assertEqual(type(l[0]), type("hi"))
## Write at least 2 additional tests (not repeats of the above described tests). Make sure to include a descriptive message in these two so we can easily see what you are testing!
	def test_11(self):
		l = play_war_game(testing=True)
		self.assertEqual(type(l[1]), type(5), "testing if the second return value of play_war_game function is an integer")

	def test_12(self):
		f = Card(suit=3, rank=13)
		self.assertEqual(f.__str__(), "King of Spades", "testing if invoking the __str__ method of a card instance that is created with suit=3, rank=13, it returns the value 'King of Spades'")



#############
## The following is a line to run all of the tests you include:
unittest.main(verbosity=2) 
## verbosity 2 to see detail about the tests the code fails/passes/etc.