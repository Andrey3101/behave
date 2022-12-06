import random

def ctrl_summ(nums, type):
    ctrl_type = {
        'n2_12': [7, 2, 4, 10, 3, 5, 9, 4, 6, 8],
        'n1_12': [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8],
        'n1_10': [2, 4, 10, 3, 5, 9, 4, 6, 8],
    }
    n = 0
    l = ctrl_type[type]
    for i in range(0, len(l)):
        n += nums[i] * l[i]
    return n % 11 % 10
    
def inn(l):
    nums = [
        random.randint(9, 9) if x == 0
        else random.randint(6, 6) if x == 1
        else random.randint(0, 9)
        for x in range(0, 9 if l == 10 else 10)
    ]

    if l == 10:
        n1 = ctrl_summ(nums, 'n1_10')
        nums.append(n1)

    elif l == 12:
        n2 = ctrl_summ(nums, 'n2_12')
        nums.append(n2)
        n1 = ctrl_summ(nums, 'n1_12')
        nums.append(n1)

    return ''.join([str(x) for x in nums])