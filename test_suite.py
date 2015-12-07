import unittest
from base62coder import Base62Coder
from Views import is_valid_url
class TestBase62Coder(unittest.TestCase):
    __base62_test_object = Base62Coder()
    def test_convert_to_base62(self):
        self.assertEqual(self.__base62_test_object.convert_to_base62(0),'0')
        self.assertEqual(self.__base62_test_object.convert_to_base62(-223),'-1')
        self.assertEqual(self.__base62_test_object.convert_to_base62(9),'9')
    def test_back_to_decimal(self):
        self.assertEqual(self.__base62_test_object.back_to_decimal(''),0)
        self.assertLess(self.__base62_test_object.back_to_decimal('-22'),0)
        self.assertEqual(self.__base62_test_object.back_to_decimal('9'),9)
        self.assertLess(self.__base62_test_object.back_to_decimal('@@'),0)
        self.assertLess(self.__base62_test_object.back_to_decimal('1@'),0)

class TestUrlValidator(unittest.TestCase):
    def test_is_valid_url(self):
        self.assertFalse(is_valid_url('url'))
        self.assertFalse(is_valid_url('google.se'))
        self.assertFalse(is_valid_url('www.google.se'))
        self.assertFalse(is_valid_url('hb@gmail.com'))
        self.assertFalse(is_valid_url('http://hb@gmail.com'))
        self.assertTrue(is_valid_url('http://google.se'))
        self.assertTrue(is_valid_url('http://google.se/?'))
        self.assertTrue(is_valid_url('http://google.se/?hb@gmail.com'))
        self.assertTrue(is_valid_url('https://scontent-ams3-1.xx.fbcdn.net/hphotos-xfp1/t31.0-8/11950318_10153019623646426_2111207839878398465_o.jpg'))
        

if __name__ == '__main__':
    unittest.main()
