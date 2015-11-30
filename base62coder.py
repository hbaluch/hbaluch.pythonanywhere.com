import string
from math import floor
class Base62Coder:
    def __init__(self):
        self.__base62_dictionary = string.digits + string.ascii_uppercase + string.ascii_lowercase

    #Returns the number converted to base 62
    #In case of bad input returns -1
    def convert_to_base62(self, number):
        if number < 0:
            return '-1'
        remainder   = number % 62
        result      = self.__base62_dictionary[remainder]
        quotient    = floor(number / 62)

        while quotient > 0:
            remainder   = quotient % 62
            result      = self.__base62_dictionary[remainder] + result
            number      = quotient
            quotient    = floor(number / 62)

        return result
    #Returns decimal value for base 62 number
    #In case of bad input returns negative value
    def back_to_decimal(self, number):
        length  = len(number)
        index   = 0
        result = 0
        while index < length:
            result = 62 * result + self.__base62_dictionary.find(number[index])
            index += 1
        return result
