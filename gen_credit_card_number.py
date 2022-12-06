import copy
import random

def completed_number(prefix, length):
    """
    'prefix' is the start of the CC number as a string, any number of digits.
    'length' is the length of the CC number to generate. Typically 13 or 16
    """
    ccnumber = prefix
    # generate digits
    while len(ccnumber) < (length - 1):
        digit = random.choice(['0',  '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        ccnumber.append(digit)
    # Calculate sum 
    sum = 0
    pos = 0
    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()
    while pos < length - 1:
        odd = int( reversedCCnumber[pos] ) * 2
        if odd > 9:
            odd -= 9
        sum += odd
        if pos != (length - 2):
            sum += int( reversedCCnumber[pos+1] )
        pos += 2
    # Calculate check digit
    checkdigit = ((sum / 10 + 1) * 10 - sum) % 10
    ccnumber.append( str(int(checkdigit)) )
    return ''.join(ccnumber)

def credit_card_number(length, howMany, bank=['visa','mastercard','mir']):
    banks = []
    if 'visa' in bank:
        visa = [ 	['4', '5', '3', '9'], 
                        ['4', '5', '5', '6'], 
                        ['4', '9', '1', '6'],
                        ['4', '5', '3', '2'], 
                        ['4', '9', '2', '9'],
                        ['4', '0', '2', '4', '0', '0', '7', '1'],
                        ['4', '4', '8', '6'],
                        ['4', '7', '1', '6'],
                        ['4'] ]
        banks.append(visa)
    if 'mastercard' in bank:
        mastercard = [    ['5', '1'],
                                    ['5', '2'],
                                    ['5', '3'],
                                    ['5', '4'],
                                    ['5', '5'] ]
        banks.append(mastercard)
    if 'mir'in bank:
        mir = [ ['2','2','0','0','0','2']
        ]
        banks.append(mir)
    result = []
    for i in range(howMany):
        # prefixList = copy.copy( random.choice([visaPrefixList, mastercardPrefixList]) )
        bank = random.choice(banks)
        prefixList = copy.copy( random.choice([bank]) )
        ccnumber = copy.copy( random.choice(prefixList) )
        result.append( completed_number(ccnumber, length) )
    return result