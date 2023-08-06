from random import randint


def roll(dicestring):
    """Rolls dice according to input string and returns the sum.

    Bonus is optional, if used, it should be positive (or zero). Not case-sensitive.

    :param dicestring: should look like "5T6+2", "1T100" or "2t6".
    """
    if '+' in dicestring:
        dicestring, bonus = dicestring.split('+')
        bonus = int(bonus)
    else:
        bonus = 0

    number_of_dice, dice_sides = [int(x) for x in dicestring.lower().split('t')]
    if dice_sides == 6:
        result = d6(number_of_dice)
    else:
        result = other_dice(number_of_dice, dice_sides)

    return result + bonus


def d6(number_of_dice):
    """Rolls a number of exploding six-sided dice.

    Whenever a 6 is rolled, it is removed and two new dice are rolled and added. This is done recursively."""
    result = 0
    for x in range(number_of_dice):
        dice_roll = randint(1, 6)
        if dice_roll == 6:
            dice_roll = d6(2)
        result += dice_roll
    return result


def other_dice(number_of_dice, sides):
    """Rolls a number of dice that are not six-sided.

    This function is intended for rolling D10's and D100's but can also be used to roll other types of dice.
    """
    result = 0
    for x in range(number_of_dice):
        result += randint(1, sides)
    return result
