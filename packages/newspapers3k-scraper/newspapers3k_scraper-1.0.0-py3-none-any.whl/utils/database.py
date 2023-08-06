import mysql.connector
from mysql.connector import pooling
import validators
import json

# Read config from file
with open('config.json', 'r') as f:
    config = json.load(f)
print(config)
# Access config values
host = config['host']
user = config['user']
password = config['password']
database = config['database']

connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_size=5, **config)

# Define a function to get a connection from the pool
def get_connection():
    return connection_pool.get_connection()

# Use the connection pool to execute queries
def save_article_to_db(article):
    if article.url is None or not validators.url(article.url):
        # Save rejected URL to a text file
        with open('rejected_urls.txt', 'a') as f:
            f.write(article.url + '\n')
        return

    if len(article.title.split()) < 6:
        # Save rejected URL to a text file
        with open('rejected_urls.txt', 'a') as f:
            f.write(article.url + '\n')
        return

    connection = get_connection()
    cursor = connection.cursor()
    sql = "INSERT INTO news (title, keywords, url, text, description, summary, category, top_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (article.title, ','.join(article.keywords), article.url, article.text, article.meta_description, article.summary, ','.join(article.tags), article.top_image)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    connection.close()