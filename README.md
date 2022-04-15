# BookRepository/Goodreads Big Data Project

If you want to see the scraped csv file, check the data backup folder.

## Setting Up Hive
To be able to handle the textual data (reviews), due to the size of the Dataset, we chose to use Apache Hive (Through a Docker container).
Everything you need is inside the Hive folder, inclusing a sample of the dataset (random)

- First navigate into the Hive folder and use the command:
      
		$ docker-compose up -d

Allow Docker a few minutes to spin up all the containers. 

- Then Log onto the Hive servet by using the command:

    $ docker exec -it hive-server /bin/bash

- Then navigate to the reviews folder

    $ cd ..
    $ cd reviews/
    
- Create the hive table by using the command:

    $ hive -f employee_table.hql

- Add the data into the table:

    $ hadoop fs -put employee.csv hdfs://namenode:8020/user/hive/warehouse/testdb.db/reviews
    
- launch hive by using:
    
    $ hive
    
- enter the Database

    > use testdb;

You are now inside the database and you can use HQL to make Queries
For example:
    > select * from reviews where isbn = 9781401253462;

