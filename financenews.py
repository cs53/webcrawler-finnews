import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# Define a list of financial news websites to scrape
websites = ['https://www.reuters.com', 'https://www.bloomberg.com', 'https://www.wsj.com']

# Initialize an empty list to store article information
articles = []

# Initialize a webdriver to navigate dynamic websites (e.g. WSJ)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run browser in background
driver = webdriver.Chrome(options=options)

# Scrape each website for article information
for website in websites:
    # Make a request to the website's homepage
    response = requests.get(website)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all article links on the homepage
    article_links = soup.find_all('a', {'class': 'article'})

    # Loop through each article link and scrape article information
    for link in article_links:
        # Make a request to the article link
        article_response = requests.get(link['href'])
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        
        # Extract article title, date, and content
        title = article_soup.find('h1').get_text()
        date = article_soup.find('time').get_text()
        content = article_soup.find('div', {'class': 'ArticleBodyWrapper'}).get_text()

        # Append article information to articles list
        articles.append({'Website': website, 'Title': title, 'Date': date, 'Content': content})

# Close the webdriver
driver.quit()

# Convert articles list to pandas DataFrame
df = pd.DataFrame(articles)

# Clean the Content column (remove newlines and extra whitespace)
df['Content'] = df['Content'].str.replace('\n', ' ').str.strip()

# Save the DataFrame to a CSV file
df.to_csv('financial_news_corpus.csv', index=False)

# Display the DataFrame
print(df.head())
