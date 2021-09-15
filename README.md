# DnDBeyond_Parser
A repository to scrape dndbeyond and use the data in the characters sheet in an sheets document. Can also be used to update dndbeyond with information from said sheet

## Requirments
1. [Selenium](https://selenium-python.readthedocs.io/installation.html) - used for the scraping of dndbeyond. Since the site has dynamiccly loading html code based on user interaction, selenium was the obvious chcoice. 
    - Install with the following command: `pip install selenium`
2. [Chrome](https://www.google.com/chrome/) - yeah, yeah, don't at me. I used chrome since I use chrome, no other reason behind it. Might add support for other browsers later, but it's not a priority.
    - [Chrome Driver](https://sites.google.com/chromium.org/driver/) - Selenium needs the driver for the appropriate version of chrome. The driver that comes with the repository is updated for chrome 92
3. [Pandas](https://pandas.pydata.org/docs/) - for creating dataframes to later put into sheets / for taking the data from sheets in an organized manner
    - Install with the following command: `pip install pandas`
 4. [pygsheets](https://github.com/nithinmurali/pygsheets) - this wonderfull library allows for easy interaction with google sheets, and was far better than any other method I read about to interact with the google API
    - Install with the following command: `pip install pygsheets`, but I highly recommend you check the repository linked above. You'll need to generate credentials and whatnot, and they have all the explainations there
 
 
## Notes
- If you try to update beyond, the bot will ask for username and password to log into your accout (currently only through twitch, more support to come).    
 Despite the alarming claims made by the bot, the details are not used for anything nefarious, and in fact aren't even saved outside the local instance of the variables they are stored in. You can verify that by looking at the code :)
