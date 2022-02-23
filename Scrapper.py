import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import csv
from alive_progress import alive_bar

base_url = "https://www.bookdepository.com/search?searchSortBy=popularity&format=1&advanced=true&page="
url = ['https://www.bookdepository.com/search?format=1&price=low&searchSortBy=popularity&advanced=true&page=',
        'https://www.bookdepository.com/search?format=1&price=med&searchSortBy=popularity&advanced=true&page=',
        'https://www.bookdepository.com/search?format=1&price=high&searchSortBy=popularity&advanced=true&page=']
book_url = "https://www.bookdepository.com/Silent-Patient-Alex-Michaelides/9781409181637?ref=grid-view&qid=1645520860979&sr=1-31"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

def scrape_page(url, headers):
    
    try:
        response = requests.get(url, headers=headers)
    except:
        print("Connection Error: could not connect to page")
        return []
    
    soup = bs(response.content, 'html.parser')

    bookLinks = []
    for h3 in soup.find_all('h3', attrs = {"class" : "title"}):
        for a in h3.find_all("a"):
            bookLinks.append(a.attrs['href'])
    
    return bookLinks

def clean_up(text):
    text = text.replace("  ", "")
    text = text.replace("\n", "")
    return text

def get_book_data(url, headers):
    try:
        response = requests.get(url, headers=headers)
    except:
        print("Connection Error: could not connect to page")
        return []
    
    soup = bs(response.content, 'html.parser')

    title = soup.find(itemprop = "name").text

    title = clean_up(title)

    rating = soup.find(itemprop = "ratingValue").text

    rating = clean_up(rating)

    num_rating = soup.find(itemprop = "ratingCount").get('content')
    try:
        price = soup.find(class_ = "sale-price").text
    except:
        price = soup.find(class_ = "list-price").text

    price = price.split(' ')

    price = price[-1]
    
    price = float(price)

    try:
        author = soup.find(itemprop = "author").text
        author = clean_up(author)
    except:
        author = "Unauthored"
    
    language = soup.find(itemprop = "inLanguage").text

    language = clean_up(language)

    num_pages = clean_up(soup.find(itemprop = "numberOfPages").text)

    num_pages = num_pages.split(' ')

    num_pages = num_pages[0]

    date = soup.find(itemprop = "datePublished").text

    isbn = soup.find(itemprop = "isbn").text

    categories = []

    cats = soup.find(class_ = "breadcrumb")
    for li in cats.find_all('li'):
        categories.append(clean_up(li.text))

    categories = categories[1:]

    categories = categories[0:3]
    
    return [isbn, title, author, price, language, num_pages, date, rating, num_rating ] + categories


def scrape_books(url, headers):
    
    book_links = []
    csv_headers = ["isbn", "title", "author", "price", "language", "num_pages", "date", "rating", "num_rating", "category 1", "category 2", "category 3"]
    with open('AllBooksDataset.csv', 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)
        for link in url:
            with alive_bar(29970) as bar:
                for i in range(1,334):
                    
                    book_links = scrape_page(link+str(i), headers)
                    for book in book_links:
                        bar()
                        try:
                            book_data = get_book_data("https://www.bookdepository.com/" + book, headers)
                            if book_data:
                                writer.writerow(book_data)
                                # print(book_data)
                        except Exception as e:
                            print(e)
                            print("Problem in data: skipping Book")
                            print(book)



scrape_books(url, headers)
# url_header = "https://www.bookdepository.com/"
# print(get_book_data(url_header+"/Harry-Potter-Magical-Creatures-Colouring-Book/9781783705825?ref=grid-view&qid=1645646235723&sr=1-957",headers))