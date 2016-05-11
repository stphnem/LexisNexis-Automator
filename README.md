# LexisNexis Automator

##Installation
The following program requires:
 - Chrome
 - Python 2.7
 - Chrome Webdriver (Included in the repo)

##Usage
 Before using, make sure that the chromedriver.exe and LNAutomator class are in
 the same directory.

 1. Instantiate an instance of LNAutomator

 ```python
    myAutomator = LNAutomator()
 ```

 2. Call the search method with the search query as
    an argument. 
 ```python
    myAutomator.search("gun control")
 ```

 3. After calling search, calling download_all_docs will automate the 
 downloading of documents until it is exhausted
 ```python
    myAutomator.download_all_docs()
 ```


 #####In LNAutomator File
 ```python
    if __name__ == "__main__":
        myAutomator = LNAutomator()
        myAutomator.search("gun control")
        myAutomator.download_all_docs()
 ```

##Future Support
 Web Drivers are needed to use the automator in other browsers. Drivers can be 
 found in the link below.
 http://www.seleniumhq.org/download/

 Selenium IDE can be a very useful tool in the instance that the layout
 of LexisNexis changes. Selenium IDE is a Mozilla Firefox plugin that records
 the user clicks, inputs, etc. It provides plenty of informative information
 to modifying the automator such as when to switch frames, what ids are selected,
 and much more. 
 
 http://www.seleniumhq.org/projects/ide/