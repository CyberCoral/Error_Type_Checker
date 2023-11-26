
# ver. Sun/26/Nov/2023
#
# Made by: CyberCoral
# ------------------------------------------------
# Github:
# https://www.github.com/CyberCoral
#

import re

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
### This program checks for conditions on the variable var with 2 different severity_mode types.
###
def ConditionCheck(var, conditions: str, severity_mode: int = 1):
    '''
    The function checks for str conditions
    and if they are correct or not.
    Also, depending on severity_mode, it can
    return different types of errors:
    
    - severity_mode = 1: False if the conditions
    are not met.

    - severity_mode = 2: SyntaxError if the
    conditions are not met.

    The structure of conditions is the next one:
    "<condition> & <condition>" for "and" structures.
    "<condition> | <condition>" for "or" structures.

    All the conditions must have "var" in them.
    '''

    if isinstance(conditions, str) != True:
        raise TypeError("conditions must be a str.")
    elif re.search(".*var",conditions) == None:
        raise SyntaxError("conditions must contain var at least once.")

    if isinstance(severity_mode, int) != True:
        raise TypeError("severity_mode must be an int.")

    c = "".join([str(i) for i in conditions]).replace("&"," and ").replace("|"," or ")
    l = []
    

    match severity_mode:
        
        case 1:

            try:
                exec(compile(f"b = {c}\nl.append(b)","<string>","exec"))
                b = l[0]
                if b == False:
                    return False
                return True
            except SyntaxError:
                return False

        case 2:
            
            try:
                exec(compile(f"b = {c}\nl.append(b)","<string>","exec"))
                b = l[0]
                if b == False:
                    raise ValueError(f"The conditions ({c}) are not met with var = {var}.")
                return True
            except SyntaxError:
                raise SyntaxError(f"The conditions ({c}) do not make sense, they raise SyntaxError.")

        case _:

            raise OSError(f"This severity mode ({severity_mode}) is not included in the program.") 

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
            
###
### This program makes an
### automated check for common variable types on variables.
###

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

###
### This program makes an
### automated check for conditions on variables with 2 different types of severity_modes.
###
def AutomatedConditionCheck(variables: list, condition_batch: list, severity_modes: list):
    '''
    This program automatically checks for
    conditions in variables with
    condition_batch and with
    severity_modes.
    It follows the same rules of
    ConditionCheck().
    '''
    if isinstance(variables, list) != True:
        raise TypeError("variables must be a list")
    elif isinstance(condition_batch, list) != True:
        raise TypeError("condition_batch must be a list")
    elif isinstance(severity_modes, list) != True:
        raise TypeError("severity_modes must be a list")

    if len(variables) != len(condition_batch) and len(variables) != len(severity_modes):
        raise SyntaxError("There must be the same number of elements for variables and condition_batch ({}).".format(len(variables)))

    for i in range(len(condition_batch)):
        if isinstance(condition_batch[i], str) != True:
            raise TypeError("conditions must be a str.")
        elif re.search(".*var",condition_batch[i]) == None:
            raise SyntaxError("conditions must contain var at least once.")

    for i in range(len(severity_modes)):
        if isinstance(severity_modes[i], int) != True:
            raise TypeError("severity_mode must be an int.")

    results = []

    for i in range(len(variables)):
        results.append(ConditionCheck(variables[i], condition_batch[i], severity_modes[i]))

    return results
