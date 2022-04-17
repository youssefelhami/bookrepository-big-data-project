# BookRepository/Goodreads Big Data Project

If you want to see the scraped books csv file, check the data backup folder. If you want to see the reviews data, a sample of 20k reviews are in the Hive/reviews folder. The other csv files are temporary files created/used by the Scrapping code so they're not consistent.

## Scraping the data
First scrape the book data from the BookScrapper. The results will be saved in AllBooksDataSet.csv

Then scrape the reviews (who use the isbn in AllBooksDataSet.csv) using ReviewsScrapper. The results will be saved in ReviewsDS.csv

The reviews dataset contain the isbn of the book being reviewed, the rating, the review itself, and the category of the book being reviewed.
The ratings are composed of a rating out of 5:
 - 0 -> no rating
 - did not like it -> 1/5
 - it was ok -> 2/5
 - liked it -> 3/5
 - really liked it -> 4/5
 - it was amazing -> 5/5

For more information about the books DS, check out the commented code in the BooksScrapper.py file.

## Setting Up Hive
To be able to handle the textual data (reviews), due to the size of the Dataset, we chose to use Apache Hive (Through a Docker container).
Everything you need is inside the Hive folder, inclusing a sample of the dataset (random)

- First navigate into the Hive folder and use the command:
      
		$ docker-compose up -d

Allow Docker a few minutes to spin up all the containers. 

- Then Log onto the Hive servet by using the command:

		$ docker exec -it hive-server /bin/bash

- Then navigate to the reviews folder

		# cd ..
    
		# cd reviews/
    
- Create the hive table by using the command:

		# hive -f reviews_table.hql

- Add the data into the table:

		# hadoop fs -put reviews.csv hdfs://namenode:8020/user/hive/warehouse/testdb.db/reviews
    
- Launch hive by using:
		
		# hive
    
- Enter the Database

		> use testdb;

- You are now inside the database and you can use HQL to make Queries
For example:
		
		> select * from reviews where isbn = 9781401253462;



Don't forget to close the Docker Containers after you're done by using the command:

		$ docker-compose down
