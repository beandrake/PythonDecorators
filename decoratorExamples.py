from functools import wraps # this decorator preserves function metadata when doing decorating

############################## BASIC DECORATOR AND OVERVIEW ##################################

# Let's say we have this function:
def sayMyName_original(firstName, lastName):
	return f"{firstName} {lastName}"

# If we want to supplement its functionality, we can make a wrapper function.
# But if we have numerous functions like this and want to add some functionality to many of them,
# that's when decorators can come in handy; they let us easily mass-produce wrappers.

# A decorator is a function that takes a function as an argument
# and returns a function that wraps the passed function.
#	The below decorator creates a wrapper that adds "Ser " before the return of the wrapped function.
def knight(myFunction):
	print("Creating wrapped function...")		# The application of the decorator is a function call
	@wraps(myFunction)
	def wrapper(*args, **kwargs):
		print("Wrapper is about to run function...")
		result = myFunction(*args, **kwargs)				# you could modify arguments, etc
		print("Wrapper is finished running function!")	# you could add something entirely new
		return f"Ser {result}"							# you can modify return output
	return wrapper

# Above we made a function that returns a wrapper; now let's decorate our initial function.
# We just pass our initial function into the decorating function, which then
# returns a wrapped version of our initial function.
sayMyName = knight(sayMyName_original)

# Let's see it working:
myName = sayMyName("Jon", "Arbuckle")
print(f"My name is {myName}.")
print()

# However, there's a more common way to apply decorators that uses a special syntax.
# We can apply the decorator right when we're declaring the function:
@knight
def sayYourName(firstName, lastName):
	return f"{firstName} {lastName}"

#	That did the same thing as the previous approach, except:
# 		- it looks a bit prettier
# 		- it doesn't create an extra throwaway function name

# Let's see it working:
yourName = sayYourName("Jon", "Arbuckle")
print(f"Your name is {yourName}.")


print('\n')
############################# DECORATOR WITH ARGUMENTS #################################

# To do this, we're going to need to make a function that RETURNS a decorator;
# so a function that makes a decorator function which makes a wrapper function which runs a function.
# We've added one more function layer!

def decoratorMaker(htmlTag):
	def decoratingFunction(myFunction):
		@wraps(myFunction)
		def wrapper(*args, **kwargs):
			result = myFunction(*args, **kwargs)
			return f'<{htmlTag}>{result}</{htmlTag}>'
		return wrapper
	return decoratingFunction

applyTag = decoratorMaker # alias is unnecessary, just helps conceptualize

@applyTag("b")
@applyTag("i")
def bodyText(text):
	return text

print( bodyText("Heyo!") )


print('\n')
############################# SOME NOTES #################################
#
#	The order that multiple decorators are applied can matter.
#	Each decorator adds an additional function call to calling a function;
# 		consider that for both your stack and your speed.


############################# SOME PRACTICAL EXAMPLES #################################

TEST_MODE = True

def testSpeed(myFunction):
	if not TEST_MODE:
		return myFunction

	import time
	@wraps(myFunction)
	def wrapper(*args, **kwargs):
		currentTime = time.process_time_ns()
		result = myFunction(*args, **kwargs)
		print(f"{myFunction.__name__} took {time.process_time_ns()-currentTime} nanoseconds.")
		return result
	return wrapper


def countCalls(myFunction):
	if not TEST_MODE:
		return myFunction

	@wraps(myFunction)
	def wrapper(*args, **kwargs):
		wrapper.count = wrapper.count + 1
		print(f"{myFunction.__name__} is being called; call count: {wrapper.count}.")
		result = myFunction(*args, **kwargs)
		return result
	wrapper.count = 0
	return wrapper


@testSpeed
@countCalls
def countToOneMillion():
	for i in range(0, 1000000):
		pass
	print("Finished counting!")

countToOneMillion()
countToOneMillion()
countToOneMillion()

# For more thorough explanations:
# https://stackoverflow.com/questions/739654/how-do-i-make-function-decorators-and-chain-them-together