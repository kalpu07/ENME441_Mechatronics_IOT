#Kalp Upadhayay - ENME441 - Fall 2025
# Lab 3: Python Mastermind

import random

#Functions that prints solid circle certain certain quantity
def print_solid_circle(quantity):
	print('\u25CF' * quantity, end ='')

def print_open_circle(quantity):
	print('\u25CB' * quantity, end ='')

guess_number = 1 #Starting off at guess 1
max_guesses = 12 # 12 Guesses max for user

#Prints basic menu / instructions
print('Guess a sequence --- 4 values from 1 - 6:')
print('\u25CF = one element is in code and in correct place')
print('\u25CB = one element is in code but in wrong place')

#Generates random sequence
random_sequence = [random.randint(1,6) for i in range(4)]

#While loop---- User keeps guessing unless exited when max guesses tried or win
while guess_number <= max_guesses:

	#User prompt for Guess
	curr_guess = input('Guess a sequence --- 4 values from 1 - 6:')

	#Removing Spaces from Guess
	curr_guess = curr_guess.replace(" ", "")

	#Validates guess 
	while len(curr_guess) !=4 or not all (digits in '123456' for digits in curr_guess):
		curr_guess = input('Invalid guess. Make sure it is a 4 digit number: ')
		curr_guess = curr_guess.replace(" ", "")

	#Stores into a list
	curr_guess_list = [int(i) for i in curr_guess]

	#Prints current user guess 
	print(f'User guess is {guess_number} of 12: {curr_guess}')

	#Making copies of lists
	random_copy = random_sequence.copy()
	guess_copy = curr_guess_list.copy()

	# These variables correspond with solid and open circles
	correct_position = 0 
	correct_digit_only = 0

	#Checks if digits are in correct position
	for i in range(4):
		if curr_guess_list[i] == random_sequence[i]:
			correct_position +=1
			guess_copy[i] = None # Marking specific guess digit as used
			random_copy[i] = None # Marking specific random digit as used

	#Checks for digits that are correct but in the wrong place
	for i in range(4):
		if guess_copy[i] is not None and guess_copy[i] in random_copy:
			correct_digit_only += 1
			random_copy[random_copy.index(guess_copy[i])] = None

	print_solid_circle(correct_position)
	print_open_circle(correct_digit_only)

	#Prints new line
	print()

	#Incrementing by 1 ---- number of guesses
	guess_number+=1

	#Exits if correct number guesses
	if(correct_position ==4):
		print('Correct - you win!')
		break

	if(guess_number >= 12):
		print('Sorry You ran out of tries!')
		break

		



