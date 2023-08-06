# pyweb
# Python Module for creating websites
# Made by TomTheCodingGuy
#
# Main class WebPage creates a html file, which can be edited through functions and its starting parameters.     

import webbrowser # Uses webbrowser module

class WebPage():
    def __init__(self, file, action, tabhead=None, bgcolour=None, icon = None):
        self.file = file
        self.action = action
        
        # Set Defaults
        if icon == None:
            self.icon = "./alien_hurt.ico"
        else:
            self.icon = icon
            
        if tabhead == None:
            self.tabhead = "HTML with Python!"
        else:
            self.tabhead = tabhead
            
        if bgcolour == None:
            self.bgcolour = "background-color:white"
        else:
            self.bgcolour = "background-color:"+bgcolour
            
        # Open/Create HTML File
        if action == "w":
            self.webfile = open(self.file,"w")
            self.webfile.write("<!DOCTYPE html>")
            self.webfile.write("\n<html> \n <head> \n  \t<title>"+self.tabhead+"</title> \n  \t<link rel=\"shortcut icon\" href=\""+self.icon+"\" type=\"image/x-icon\">\n </head> \n <body style = "+self.bgcolour+"> \n\n </body> \n</html>")
            self.webfile.close()
        elif action == "a":
            self.webfile = open(self.file,"a")
    
    ###################
    # Important Stuff #
    ###################
    
    def openpage(self): # Opens the webpage in your browser
        site = 'file://'+self.file
        webbrowser.open(site, new=2)
            
    def showfile(self): # Prints the .txt version of the HTML file with line numbers
        openfile = open(self.file,"rt")
        self.lines = openfile.readlines()
        x = 1
        print("=========================================================================================\n")
        for line in lines:  
            print(str(x)+"   "+line)
            x+=1
        
        print("\n=========================================================================================")
    
    ##################
    # Web Page Items #
    ##################
    
    def Heading(self, text, num): # Any sized title on webpage
        self.webfile = open(self.file, "r")
        lines = self.webfile.readlines()
        self.showfile()
        line = int(input("Line to enter heading (in <body> section): "))
        lines[line-1] = "\n\t<h"+str(num)+">"+text+"<h"+str(num)+">\n\n"
        self.webfile = open(self.file, "w")
        self.webfile.writelines(lines)
        self.webfile.close()
        
    def Image(self,image,alt): # Any image on webpage with alt text
        self.webfile = open(self.file, "r")
        lines = self.webfile.readlines()
        self.showfile()
        line = int(input("Line of code to enter image (in <body> section): "))
        lines[line-1] = "\n\t<img src="+image+" alt="+alt+">\n\n"
        self.webfile = open(self.file, "w")
        self.webfile.writelines(lines)
        self.webfile.close()
        
    def Paragraph(self, text):
        self.webfile = open(self.file, "r")
        lines = self.webfile.readlines()
        self.showfile()
        line = int(input("Line of code to enter paragraph (in <body> section): "))
        lines[line-1] = "\n\t<p>"+text+"</p>\n\n"
        self.webfile = open(self.file, "w")
        self.webfile.writelines(lines)
        self.webfile.close()