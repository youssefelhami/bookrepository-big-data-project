"""
This File is a scrapper for the website bookdepository.com using Beautiful Soup.

We were able to scrape 29,753 books out of a possible 29,970 which means with over
99.27% effectivity.

"""

import requests
from bs4 import BeautifulSoup as bs
import csv
from alive_progress import alive_bar
import pandas as pd
import numpy as np
from multiprocessing import Pool
from multiprocessing import cpu_count


total = []


def get_reviews(isbn):
    
    print(isbn)
    page_url = "https://www.goodreads.com/search?q=" + str(isbn)
    try:
        page = requests.get(page_url)
        d=bs(page.text, 'html.parser')
        review = d.find_all("div", {"class": "reviewText stacked"})
        review = list(map(lambda x: x.get_text(), review))
        review_state = d.find_all('div', class_="reviewHeader uitext stacked")
        rating = []
        
        for i in range(len(review_state)):
            if 'rated it' in review_state[i].get_text():
                rate_i = review_state[i].find_all('span', class_='staticStars notranslate')[0].get_text()
                rating.append(rate_i)
            else:
                rating.append("0")
        

        if len(rating) == len(review):
            book = [str(isbn)] * len(rating)
            return list(zip(book,rating,review))

    except Exception as e:
        print("Connection Error!", e)
        return [("0","0","0")]



df = pd.read_csv('AllBooksDataset.csv')
df.drop_duplicates('isbn').reset_index(drop=True, inplace=True)
book_id = [ID for ID in df['isbn']]



def get_cat(id):
    print(id)
    cats = []
    for i in range(df.shape[0]):
        if str(df['isbn'].iloc[i]) == id:
            return df['category_1'].iloc[i]
    return None


if __name__ == '__main__':
    p = Pool(cpu_count())
    total = total + p.map(get_reviews, book_id)
    p.terminate()
    p.join()
    print("Scraping finished")
    print(len(total))
    final = []
    for data in total:
        if data != None:
            for val in data:
                if val!= None:
                    final.append(val)

    reviewsDF = pd.DataFrame(final, columns=['book','rating', 'review'])
    reviewsDF = reviewsDF.replace(r'\n',  ' ', regex=True)
    reviewsDF = reviewsDF.replace(r',',  ' ', regex=True)
    cats = reviewsDF['book'].apply(get_cat)
    reviewsDF['category'] = cats
    reviewsDF.to_csv("ReviewsDS.csv",encoding='utf-8', index=False, header=False)
    print("Saved in csv")








