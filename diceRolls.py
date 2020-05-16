import random


def coin():
    flip = random.randint(0, 1)
    if flip:
        outcome = "Head (1)"
        message = ", your flip is: " + str(outcome)

    else:
        outcome = "Tail (0)"
        message = ", your flip is: " + str(outcome)

    return message


def d4():
    roll = random.randint(1, 4)
    message = ", your roll is: " + str(roll)

    return message


def d6():
    roll = random.randint(1, 6)
    message = ", your roll is: " + str(roll)

    return message


def d8():
    roll = random.randint(1, 8)
    message = ", your roll is: " + str(roll)

    return message


def d10():
    roll = random.randint(1, 10)
    message = ", your roll is: " + str(roll)

    return message


def d12():
    roll = random.randint(1, 12)
    message = ", your roll is: " + str(roll)

    return message


def d20():
    roll = random.randint(1, 20)
    message = ", your roll is: " + str(roll)

    return message


def d100():
    roll = random.randint(1, 100)
    message = ", your roll is: " + str(roll)

    return message


