import Automated_Error_Checks as AEC # Shorten the name.
		
def natural_inv(number):
	AEC.AutomatedErrorTypeFinder([number],[1]) # number must be an int.
	AEC.AutomatedConditionCheck([number],["var != 0"],[2]) # For edge case 0.
	return 1 / number
		
a = natural_inv(2)
b = natural_inv(0) # return ValueError
