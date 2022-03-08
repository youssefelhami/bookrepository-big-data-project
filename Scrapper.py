"""
This File is a scrapper for the website bookdepository.com using Beautiful Soup.

We were able to scrape 29,753 books out of a possible 29,970 which means with over
99.27% effectivity.

"""

import requests
from bs4 import BeautifulSoup as bs
import csv
from alive_progress import alive_bar

"""
More precisely, we scrape for the most popular paperback books to make sure that the prices are consistent for the books;
it wouldn't make sense to compare the price of an audiobook and a physical book. We chose paperback because it's the most
common book type.
Unfortunetly, the website does not allow anyone to go past 333 pages in any search, which means a total of 9,990 books.
To get past this, we used the filter by price function that divides the books by their price (low, mid or high) allowing us to
get the data of 29,970 books.
The base search links are in the list 'url'.
"""
url = ['https://www.bookdepository.com/search?format=1&price=low&searchSortBy=popularity&advanced=true&page=',
        'https://www.bookdepository.com/search?format=1&price=med&searchSortBy=popularity&advanced=true&page=',
        'https://www.bookdepository.com/search?format=1&price=high&searchSortBy=popularity&advanced=true&page=']

"""
The headers contain information about the client (our computer) that is sent to the request to the server (the Website) 
which decreases the chance of avoiding getting detected as a bot.
"""
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

"""
Function that scrapes the book links from a search page (url) and returns an array of links.
"""
def scrape_page(url, headers):
    
    #get HTML data from page
    try:
        response = requests.get(url, headers=headers)
    except:
        print("Connection Error: could not connect to page")
        return []
    
    soup = bs(response.content, 'html.parser')

    #get title links from collected data
    bookLinks = []
    for h3 in soup.find_all('h3', attrs = {"class" : "title"}):
        for a in h3.find_all("a"):
            bookLinks.append(a.attrs['href'])
    
    return bookLinks

"""
Function that helps clean up the book data by removing extra spaces and unnecessary newlines characters in the data
-> Used in get_book_data function
"""
def clean_up(text):
    text = text.replace("  ", "")
    text = text.replace("\n", "")
    return text


"""
Function that scrapes the book data from a book page (url) and returns an array of the data.
Data returned: ["isbn", "title", "author", "price", "language", "number of pages", "date", "rating", 
                "number of ratings", and first 3 categories]
"""

def get_book_data(url, headers):
    
    #get HTML data from page
    try:
        response = requests.get(url, headers=headers)
    except:
        print("Connection Error: could not connect to page")
        return []
    
    soup = bs(response.content, 'html.parser')

    #get book title and clean it up
    title = soup.find(itemprop = "name").text
    title = clean_up(title)
    
    #get rating and number of ratings (if it doesn't exist then there weren't enough ratings in the fist place)
    # so the rating in 0 and the num_rating is 0
    try:
        rating = soup.find(itemprop = "ratingValue").text
        rating = clean_up(rating)
        num_rating = soup.find(itemprop = "ratingCount").get('content')
    except:
        rating = '0.0'
        num_rating = 0

    #get the price data. If the item is in stock the class name is sale-price. But if it's out of stock it's list-price
    try:
        price = soup.find(class_ = "sale-price").text
    except:
        price = soup.find(class_ = "list-price").text

    #clean up prices by separating the number and the currency and choosing just the price. If the currency is in EGP,
    #it takes the form EGP 10 so it is seperated but any forreign currency takes the form $10 which gets an error
    #when using the float function which will be caught in the try except block in the function scrape_books.
    price = price.split(' ')
    price = price[-1]
    price = float(price.replace(",",""))

    #get author name. If it doesn't exist then the book is unauthored.
    try:
        author = soup.find(itemprop = "author").text
        author = clean_up(author)
    except:
        author = "Unauthored"
    
    #Gets the language of the book. Books in foreign languages are required to write the language so if the language data is
    #missing then it's in English
    try:
        language = soup.find(itemprop = "inLanguage").text

        language = clean_up(language)
    except:
        language = "English"

    #Gets and cleans up number of pages. It's in the form '123 Pages'. We separate the string and choose the first word (aka the number)
    num_pages = clean_up(soup.find(itemprop = "numberOfPages").text)
    num_pages = num_pages.split(' ')
    num_pages = num_pages[0]

    #Get publication date
    date = soup.find(itemprop = "datePublished").text

    #Get ISBN (will be primary key after removing possible duplicates later on)
    isbn = soup.find(itemprop = "isbn").text

    #Get Category data
    categories = []
    #We get the data from the breadcrum list containing the categories
    cats = soup.find(class_ = "breadcrumb")
    for li in cats.find_all('li'):
        categories.append(clean_up(li.text))
    
    #We remove the first element of the list which is "Categories: "
    categories = categories[1:]
    #We choose the first three categories in the list
    categories = categories[0:3]
    
    return [isbn, title, author, price, language, num_pages, date, rating, num_rating ] + categories

"""
Function that scrapes the search pages and uses the result to scrape the book data which is written in a csv file.
It's the main function that is to be called to start scraping
"""
def scrape_books(url, headers):
    
    book_links = []
    canceled_links = []
    csv_headers = ["isbn", "title", "author", "price", "language", "num_pages", "date", "rating", "num_rating", "category_1", "category_2", "category_3"]
    with open('AllBooksDataset.csv', 'w', newline='', encoding='UTF8') as f: #open csv file
        writer = csv.writer(f)
        writer.writerow(csv_headers) #write the headers at the top of csv file
        with alive_bar(29970) as bar: #progress bar [max number of books is 29970]
            for link in url: #goes through the low-mid-high price filter search links
                for i in range(1,334): #iterates through pages
                    book_links = scrape_page(link+str(i), headers) #gets array with book links in page
                    for book in book_links: #iterates through links
                        bar() #update progress bar
                        
                        # Sometimes the server return foreign prices causing a deliberate error in the get_book_data function.
                        # but it is usually fixed it when we try to get the data again. if there's a problem in the book data,
                        # we try to repeat it 5 times as to make sure that the issue is not on the server but in the scraping code
                        
                        for j in range(5): 
                            try:
                                book_data = get_book_data("https://www.bookdepository.com/" + book, headers) #get book data
                                if book_data:
                                    writer.writerow(book_data) #write data in csv file
                                    print(book_data) #UnComment if you want to see the book data while scraping.
                                break
                            except Exception as e:
                                #it contains a list of the missed books and the error if we want to use it to further perfect the scraping
                                if j == 4:
                                    canceled_links.append((book),e) 



###########################################################

scrape_books(url, headers)
print("Scraping Finished!!")

############################################################