
# ver. Tue/21/Nov/2023
#
# Made by: CyberCoral
# ------------------------------------------------
# Github:
# https://www.github.com/CyberCoral
#

###
### This program makes a truth list out of a binary string of characters (made of 0s and 1s)
###

def BinaryToTruthList(binary):
    '''
    This program returns a list consisted of
    Truth and False based on a string of
    ONLY 0s and 1s (if this rule is broken, the
    program will return a SyntaxError).
    '''
    binary = str(binary)
    try:
        binary = [int(i) for i in binary]
    except ValueError:
        raise SyntaxError("{} is an invalid string from which to create a truth list.".format(binary))
    truth_list = []
    for j in range(len(binary)):
        if binary[j] not in [0,1]:
            raise SyntaxError("{} is an invalid character of a binary string.".format(binary[j]))
        else:
            truth_list.append(bool(binary[j]))
    return truth_list
            
###
### This program will be used to check common variable types
###

def ErrorTypeFinder(var, conditions):
    '''
    This program checks for variable's type
    according to conditions' truth values.
    The order of validation is this one:
    int -> float -> complex -> tuple
    -> list -> dict.         (str)
    
    Any other more input will not be considered.
    If there are less than 6 inputs, all the other
    ones are False by default, except with str.
    In that case, you have the max of 7 inputs.
    '''
    
    dict_condition = {}
    condition = ["int","float","complex","tuple","list","dict","str"]

    if isinstance(conditions, list) != True:
        return ErrorTypeFinder(conditions,BinaryToTruthList("000010"))
    
    for i in range(len(conditions)):
        if isinstance(conditions[i], bool) != True:
            raise SyntaxError("The conditions' value ({}) type ({}) is invalid.".format(conditions[i], type(conditions[i])))

    if len(conditions) <= len(condition):
        for i in range(len(condition) - len(conditions)):
            conditions.append(False)
    elif len(conditions) >= len(condition):
        conditions = conditions[0:len(condition)]
        
    if conditions.count(True) > 1:
        raise SyntaxError("A variable cannot be two types at the same time.")
    elif conditions.count(False) == len(conditions):
        raise SyntaxError("There has to be a condition that is met.")

    elif isinstance(var, str) != True and len(conditions) >= 7:
        if conditions.index(True) == 6:
            raise TypeError("{} is supposed to be {}".format(var, str))
        else:
            del conditions[6]
            
    elif isinstance(var, str) == True and len(conditions) >= 7:
        if conditions.index(True) == 6:
            return True
        else:
            raise TypeError("{} is supposed to be {}".format(var, str))
        
    elif isinstance(var, str) == True and len(conditions) < 7:
        raise TypeError("{} is supposed to be {}, but cannot be valued because of conditions' setting.".format(var, str))
    else:
        del conditions[6]

    if len(conditions) <= len(condition):
        for i in range(len(condition) - len(conditions)):
            conditions.append(False)
    elif len(conditions) >= len(condition):
        conditions = conditions[0:len(condition)]
        
    for j in range(len(condition)):
        dict_condition.update({condition[j]: conditions[j]})

    conditions = []
    
    for k in range(len(condition)):
        
        conditions.append(f"""if (lambda var, k, condition, dict_condition: False if isinstance(var, eval(condition[k])) != dict_condition[condition[k]] else True)({var},{k},{condition},{dict_condition}) == False:  raise TypeError('''Type of {var} is supposed to be {condition[list(dict_condition.values()).index(True)]}''')""")
        exec(compile(conditions[0],"<string>","exec"))
        del conditions[0]

    return True

###
### This program makes an
### automated conversion of truth lists out of a binary string of characters (made of 0s and 1s)
###

def AutomatedBinaryToTruthList(binaries: list):
    '''
    This program returns a list of lists consisted of
    Truth and False based on a string of
    ONLY 0s and 1s (if this rule is broken, the
    program will return a SyntaxError).
    '''
    if isinstance(binaries, list) != True:
        raise TypeError("binaries should be a list")

    a = []
    for i in range(len(binaries)):
        a.append(BinaryToTruthList(binaries[i]))

    return a
            
#
# This program makes an
# automated check for common variable types on variables.
#

def AutomatedErrorTypeFinder(variables: list, condition_batch: list):
    '''
    This program automatically checks for
    types of variables with condition_batch.
    It follows the same rules of ErrorTypeFinder().
    '''
    if isinstance(variables, list) != True:
        raise TypeError("variables must be a list")
    elif isinstance(condition_batch, list) != True:
        raise TypeError("condition_batch must be a list")

    if len(variables) != len(condition_batch):
        raise SyntaxError("There must be the same number of elements for variables and condition_batch ({}).".format(len(variables)))

    for i in range(len(variables)):
        condition = condition_batch[i]
        if isinstance(condition, list) != True:
            try:
                condition = BinaryToTruthList(condition)
            except SyntaxError:
                raise TypeError("condition_batch[{}] ({}) is not a truth list or a binary number.".format(i,condition))

        ErrorTypeFinder(variables[i], condition)

    return True
