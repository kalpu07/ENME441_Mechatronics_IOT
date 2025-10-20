#Kalp Upadhayay - ENME441 - Lab 1 

#Just created the x variable for f(x)
x = 0.5

# Number of terms = k
k_terms = 5
k_starting = 1
k_curr = 1

#summation 
sum = 0;

# --------------------------------------------------------------------Question 1 Code

# For loop runs 5 iterations
for i in range(k_starting, k_terms+1):

	#Taylor Series Sum
	sum += ((-1)**(k_curr-1)) * ((x-1)**k_curr / (k_curr))
	#Updating the current k 
	k_curr += 1

print(f'f({x}) ~= {sum:.9f} with {k_terms} terms') 


#---------------------------------------------------------------------Question 2 Code

#Resetting values used in previous question
sum = 0
k_curr = 1

while True:

	curr_sum = ((-1)**(k_curr-1)) * ((x-1)**k_curr / (k_curr))

	#adding my current sum to overall sum
	sum += curr_sum

	#Iterating current k
	k_curr +=1

	#Exits and breaks while loop if and only condition is met
	if abs(curr_sum) < 10**-7:
		break

print(f'f({x}) ~= {sum:.9f} with {k_curr} terms')
