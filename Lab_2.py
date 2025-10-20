#Kalp Upadhayay - ENME441 - Fall 2025
# Lab 2: Functions, Generators, and List Comprahension

#Problem 1---------------------------------------------------------------

#Checking if value is inbetween lower and upper bound if so returns true 
def between(comparison_value, lower_bound =0, upper_bound =0.3):
	if comparison_value >= lower_bound and comparison_value <= upper_bound:
		return True
	else:
		return False

#Problem 2---------------------------------------------------------------

def rangef(max, step):

	#Setting to 0 initially
	current_value = 0.0 

	#as long as current value is less than the max keep yeilding and incrementing
	while current_value <= max:
		yield current_value
		current_value+= step

#Test code Below:
for i in rangef(5, 0.5):
    print(i, end=' ')


#Problem 3--------------------------------------------------------------

alist = list(rangef(1,0.25))
print(alist)

#3a

#Creating deep copy
from copy import deepcopy

deep_alist = deepcopy(alist)

#reversing and adding onto original list
deep_alist.reverse()
alist.extend(deep_alist)

print(alist)

#3b

# Using between function to check weather in 0 - 0.3 if so all those items are at end of list
alist.sort(key = lambda curr_num: between(curr_num))

print(alist)

#Problem 4 ----------------------------------------------------------

#Using list comprehension to check if numbers are divisble by 2 or 3 and printing new list
sample_list = [integer for integer in range(17) if integer % 2 == 0 or integer % 3 ==0]
print(sample_list)