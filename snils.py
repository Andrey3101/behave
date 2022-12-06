import random

def snils():
    nums = [
        random.randint(1, 1) if x == 0
        # else '-' if x == 3
        # else '-' if x == 7
        # else ' ' if x == 11
        else '' if x == 3
        else '' if x == 7
        else '' if x == 11
        else random.randint(0, 9)
        for x in range(0, 12)
    ]

    cont = (nums[10] * 1) + (nums[9] * 2) + (nums[8] * 3) + \
           (nums[6] * 4) + (nums[5] * 5) + (nums[4] * 6) + \
           (nums[2] * 7) + (nums[1] * 8) + (nums[0] * 9)

    if cont in (100, 101):
        cont = '00'

    elif cont > 101:
        cont = (cont % 101)
        if cont in (100, 101): cont = '00'
        elif cont < 10: cont = '0' + str(cont)

    elif cont < 10: cont = '0' + str(cont)

    nums.append(cont)
    return ''.join([str(x) for x in nums])