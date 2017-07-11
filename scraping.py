# RASHMIT
# 16200161
# Text Data Scraping
# TASK 1

# Import necessary libraries used
import requests
from bs4 import BeautifulSoup

# Funtion to write the news in the text files
def writeNewsToTextFile(newsContent,title):

	# writing all the titles in a separate file.
	newsTitleData = open("news/titles.txt", "a")
	newsTitleData.write(title + "\n")
	newsTitleData.close()

	# writing news content in a separate file.
	newsData = open("news/newsData.txt", "a")
	newsData.write(newsContent + "\n")
	newsData.close()


# Funtion to scrape the news page
def scrapeNewsPage(newsURL, title):
	# Store the url of the news page using requests library get function
	newsPageSourceCode = requests.get(newsURL)
	# Parsing the sourcecode of the news page using beautiful soup library
	parseNewsSourceCode = BeautifulSoup(newsPageSourceCode.text, "lxml")
	# under div > main, we store all the elements of news which is in html format
	divClassMain = parseNewsSourceCode.find("div",{"class":"main"})
	# getting only the text from of the news
	newsContent = " ".join(divClassMain.text.split())
	# calling function to write the news text and title to the file
	writeNewsToTextFile(newsContent, title)


# Funtion to scrape the month page
def scrapeMonthPage(monthURL):
	# Store the url of the month page using requests library get function
	monthPageSourceCode = requests.get(monthURL)
	# Parsing the sourcecode of the month page using beautiful soup library
	parseMonthSourceCode = BeautifulSoup(monthPageSourceCode.text, "lxml")
	# For each news, below part of the url is common and by adding specific news link 
	# We get the specific url of the news.
	updatedURL = monthURL[:-14]
	# looping under every li we find the remaining month url
	for li in parseMonthSourceCode.find_all("li"):
		if li.find("a"):
			news = li.find("a")["href"]
			newsURL = updatedURL + news
			# capturing the individul news title
			title = str(li.text)
			# Calling function to scrape the individual month page
			scrapeNewsPage(newsURL, title)

			
# Funtion to scrape the index page
def scrapeIndexPage(indexURL):
	# Store the url of the index page using requests library get function
	indexPageSourceCode = requests.get(indexURL)
	# Parsing the sourcecode of the index page using beautiful soup library
	parseIndexSourceCode = BeautifulSoup(indexPageSourceCode.text, "lxml")
	# For each month, below part of the url is common and by adding specific month link 
	# We get the specific url of the month.
	updatedURL = indexURL[:-10]
	# looping under every li we find the remaining month url
	for li in parseIndexSourceCode.find_all("li"):
		month = li.find("a")["href"]
		monthURL = updatedURL + month
		# Calling function to scrape the individual month page
		scrapeMonthPage(monthURL)
	print("Data scrapping Successful")
	

# url to be scrapped
indexURL = "http://mlg.ucd.ie/modules/COMP41680/news/index.html"
# Calling function to scrape the index page
scrapeIndexPage(indexURL)
