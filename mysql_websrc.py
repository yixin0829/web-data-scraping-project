import mysql.connector
import pandas as pd
from log_util import Logger


logger = Logger().logger

#该函数最后用，将all_sql_tables的命令全部执行。
def build_database(db_name, host_name, user_name, password, all_sql_tables):
  #  Define the connection and the cursor that is used for executing the SQL commands
    my_db = mysql.connector.connect(host=host_name, user=user_name, passwd=password, database=db_name)
    cursor = my_db.cursor()
    try:
  # Execute all SQL commands and commit it into the DB
        for sql_q in all_sql_tables:
            cursor.execute(sql_q)
        my_db.commit()
        logger.info("\n*** Database was created successfully. ***\n")  # log into a logs file

    # If we get an error at some point, the my_db.rollback() reverts everything to the state we had in our last commit
    except mysql.connector.Error as error:
        my_db.rollback()  # rollback if any exception occured
        logger.critical("Failed creating database {}.".format(error)) # log into a logs file

    # Close database connection no matter what happened before
    finally:
        if my_db is not None and my_db.is_connected():
            cursor.close() ; my_db.close()
            logger.info("MySQL connection is closed.")
        else:
            logger.info("connection to MySQL did not succeed.")

def update_num_citations(my_db, cursor): #这个函数要求在线更新，不适合我们爬取的网站。
    # Get all articles from DB (doi_link is a unique key)
    sql_get_articles = """SELECT doi_link, citations, last_name FROM authors;"""
    cursor.execute(sql_get_articles)
    articles = cursor.fetchall()
    
    # Get the updated number of citations (Using requests and BeautifulSoup, open each URL of each doi_link and extract the number of citations)
    articles_dict = [{'doi_link': articles[ind][0], 'citations': articles[ind][1]} for ind in range(len(authors_no_gen))]
    articles_dict = get_citations(articles_dict)
    
    # Update the data in the DB
    # 这里doi_link是主键，从网上实时爬取citations，存入对应条目
    for doi_link, citations in articles_dict:
        sql_update = """ UPDATE articles SET citations = {0} WHERE (doi_link = '{1}');""".format(int(citations), doi_link)
        cursor.execute(sql_update)
    # The for loop can be replaced with:
    # cur.executemany("UPDATE articles SET citations = {0} WHERE  (doi_link = '{1}');".format(int(citations), doi_link),[--tuples of the data to be updated--])
    my_db.commit()




mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "123456"
)
all_sql_tables = [...]

# An example of a single table creation called "articles" in SQL command  
sql_articles = """CREATE TABLE IF NOT EXISTS articles (ID int AUTO_INCREMENT,
                                                     doi_link varchar(255) NOT NULL,
                                                     title varchar(255),
                                                     abstract TEXT,
                                                     publication_date varchar(255),
                                                     citations int,
                                                     UNIQUE (doi_link),  
                                                     PRIMARY KEY(ID));"""
all_sql_tables.append(sql_articles) # list of all sql tables creation

# all_articles应该是article的集合（具体也不太清楚）。
try:
    # Instert all articles into the articles table.
    # Note that we use INSERT IGNORE which means that duplicates will not be inserted to DB (checked against doi_link).
    for key, item in all_articles.items():
        cursor.execute("""INSERT IGNORE INTO articles (doi_link, title, abstract, publication_date, citations) 
                        VALUES ('{}', '{}', '{}', '{}', {});""".format(key, item[0], item[1], item[2], int(item[3])))
        
    # The for loop above can be replaced with:
    # cur.executemany("""INSERT IGNORE INTO articles (doi_link, title, abstract, publication_date, citations) 
    #                   VALUES ('{}', '{}', '{}', '{}', {});""".format(key, item[0], item[1], item[2], int(item[3])),
    #                   [--tuples of the data to be updated--])

# Catch any error that might occur and logging it into the logs file.
except (KeyError, IndexError, TypeError) as err:
    logger.error("There was an error during articles insertion. The error: {}".format(err))
    
    # Save the problematic articles to csv file for future inspection
    df = pd.DataFrame(list(all_articles.values()), index=list(all_articles.keys()))
    df.to_csv("Articles.csv", sep=',')
    
    # This is for debugging. 
    # steps is a dict whose keys are the steps in the scraping processand its values are 1 or 0 (succeeded or failed)
    #steps['Articles'] = 0
