##########################
# Test WebPage functions #
##########################

import unittest
from alienHTML import WebPage

class WebPageError(Exception):
    def __init__(self,message="Could not load webpage"):
        self.message=message
        super().__init__(self.message)

class TestWebPage(unittest.TestCase):
    def setUp(self):
        self.mypage = WebPage("./test.html","w",bgcolour="powderblue")
    
    def test_init(self):
        self.assertEqual(self.mypage.file,"./test.html")
        self.assertEqual(self.mypage.action, "w")
        self.assertEqual(self.mypage.tabhead, "HTML with Python!")
        self.assertEqual(self.mypage.bgcolour, "background-color:powderblue")
    
    def test_showfile(self):
        __openfile = open("./test.html","rt")
        self.__lines = __openfile.readlines()
        self.assertEqual(self.__lines, self.mypage.List())
        cleanup()

def cleanup():
    import os
    os.remove("./test.html")
    
if __name__ == '__main__':
    unittest.main()