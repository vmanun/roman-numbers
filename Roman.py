from itertools import repeat
from re import  search


class Roman:
    # Max possible value, as the max roman number usable is M (can be scaled up)
    MAX = 5999
    # A tuple from which the toRoman method builds a Roman Number
    # the first index represents the digit to convert, meaning:
    # [0]: 1 - 9
    # [1]: 10 - 99
    # [2]: 100 - 999
    # [3]: 1000 - 5999
    # The second index gets the actual roman number corresponding to the real number
    # see ToRoman method
    ROMAN_DIGITS = (('I', 'IV', 'V', 'IX'),
                    ('X', 'XL', 'L', 'XC'),
                    ('C', 'CD', 'D', 'CM'),
                    ('M'))

    ROMAN_DIGITS_ONES = ('I', 'X', 'C', 'M')
    ROMAN_DIGITS_FIVES = ('V', 'L', 'D')
    ROMAN_DIGITS_STR = 'IVXLCDM'
    INT_DIGITS_ONES = (1, 10, 100, 1000)
    INT_DIGITS_FIVES = (5, 50, 500)

    def __init__(self, number: int = 1):
        self.value = Roman.toRoman(number)
        self.rValue = Roman.toInt(self.value)

    def add(self, number):
        result = self.rValue + number
        if result > Roman.MAX:
            print('The result is greater than the limit: {}'.format(Roman.MAX))
            return Roman.MAX
        else:
            return Roman.toRoman(result)

    def subtract(self, number):
        result = self.rValue - number
        if result < 1:
            print('The result is less than 1')
            return 'I'
        else:
            return Roman.toRoman(result)

    @classmethod
    def isValidRoman(cls, number):
        number = f'{number}'.upper()
        if search(f"[{cls.ROMAN_DIGITS_STR}]", number) != None and search(f"[^{cls.ROMAN_DIGITS_STR}]", number) == None:
            if len(number) > 1: 
                for index, digit in enumerate(number): 
                    if index > 0:
                        OneDigitIsInvalid, lastIsLesserFive, lastFiveIsInvalid = (False for _ in repeat(None, 3))
                        digitIsOne = digit in cls.ROMAN_DIGITS_ONES
                        lastDigitIsOne = number[index - 1] in cls.ROMAN_DIGITS_ONES
                        digitIsFive = digit in cls.ROMAN_DIGITS_FIVES
                        lastDigitIsFive = number[index - 1] in cls.ROMAN_DIGITS_FIVES

                        if digitIsOne and lastDigitIsOne:
                            OneDigitIsInvalid = (cls.ROMAN_DIGITS_ONES.index(digit) - cls.ROMAN_DIGITS_ONES.index(number[index - 1])) >= 2
                        elif digitIsFive and lastDigitIsFive:
                            lastIsLesserFive = (cls.ROMAN_DIGITS_FIVES.index(digit) - cls.ROMAN_DIGITS_FIVES.index(number[index - 1])) >= 0
                        elif digitIsOne and lastDigitIsFive:
                            lastFiveIsInvalid = (cls.ROMAN_DIGITS_ONES.index(digit) - cls.ROMAN_DIGITS_FIVES.index(number[index - 1])) >= 0

                        if digitIsOne and OneDigitIsInvalid: return False
                        elif digitIsOne and lastFiveIsInvalid: return False
                        elif digitIsFive and lastIsLesserFive: return False
            return True
        else: 
            return False

    @classmethod
    def toRoman(cls, n: int):
        # Validate n value
        if type(n) is not int or (n < 1 or n > cls.MAX):
            print('ERROR: Please give a positive integer between 1 and {}'.format(cls.MAX))
            return None
        # reversed string so the lowest index represents the lowest value
        n = reversed(str(n))
        result = ''

        for index, digit in enumerate(n):
            intDigit = int(digit)
            if intDigit > 0:
                if intDigit <= 3 or (index == 3 and intDigit <= 5):
                    for _ in repeat(None, intDigit):
                        result = cls.ROMAN_DIGITS[index][0] + result
                elif intDigit == 4:
                    result = cls.ROMAN_DIGITS[index][1] + result
                elif intDigit == 5:
                    result = cls.ROMAN_DIGITS[index][2] + result
                elif 5 < intDigit < 9:
                    aux = ''
                    aux = cls.ROMAN_DIGITS[index][2] + aux
                    for _ in repeat(None, (intDigit - 5)):
                        aux += cls.ROMAN_DIGITS[index][0]
                    result = aux + result
                    del aux
                elif intDigit == 9:
                    result = cls.ROMAN_DIGITS[index][3] + result
        return result

    @classmethod
    def toInt(cls, roman):
        if not cls.isValidRoman(roman):
            print('ERROR: Please give a valid roman number')
            return None

        result = 0

        for index, digit in enumerate(roman):
            onesInDigit, onesInLast, fivesInDigit = (-1 for _ in repeat(None, 3))

            if digit in cls.ROMAN_DIGITS_ONES: 
                onesInDigit = cls.ROMAN_DIGITS_ONES.index(digit) 
            if roman[index - 1] in cls.ROMAN_DIGITS_ONES:
                onesInLast = cls.ROMAN_DIGITS_ONES.index(roman[index - 1])
            if digit in cls.ROMAN_DIGITS_FIVES:
                fivesInDigit = cls.ROMAN_DIGITS_FIVES.index(digit)

            if index == 0:
                if onesInDigit != -1:
                    result += cls.INT_DIGITS_ONES[onesInDigit]
                elif fivesInDigit != -1:
                    result += cls.INT_DIGITS_FIVES[fivesInDigit]
            else:
                if onesInLast != -1 and onesInLast < onesInDigit:
                    result += (cls.INT_DIGITS_ONES[onesInDigit] - cls.INT_DIGITS_ONES[onesInLast] * 2)
                elif onesInLast != -1 and onesInLast <= fivesInDigit:
                    result += (cls.INT_DIGITS_FIVES[fivesInDigit] - cls.INT_DIGITS_ONES[onesInLast] * 2)
                elif onesInDigit != -1:
                    result += cls.INT_DIGITS_ONES[onesInDigit]
                elif fivesInDigit != -1:
                    result += cls.INT_DIGITS_FIVES[fivesInDigit]
        return result


if __name__ == "__main__":
    romanN = Roman(3888)
    print(Roman.isValidRoman('xxxhhk'))

