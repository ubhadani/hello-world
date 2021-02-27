#UrveshBhadaniFinalProject

'''
Extracts speaker data fromt the website www.flipkart.com
and saves the data to the output file
'''


from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen


baseUrl = "https://www.flipkart.com/search?q=speakers&sid=0pm%2C0o7&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&as-pos=1&as-type=RECENT&suggestionId=speakers%7CSpeakers&requestId=18e04104-cf68-4131-aba9-942c15e02667&as-backfill=on&page=2"

# name of the output file in which speaker data is saved
outputFileName = "speakers.csv"


# number of pages to fetch from the website
numOfPages = 20
# min number of reviews that a product must have
minNumOfReviews = 20
# min rating that a product must have
minRatings = 3

# list of all the webpages
pages = []
# get each webpage and store it in the pages list
for i in range(1, numOfPages+1):
    url = baseUrl + str(i)
    print(f"\nFetching page {i} of {numOfPages}. Link: {url}")
    
    # try to get the page
    try:
        page = urlopen(url)
        pages.append(page)
        print(f"Fetched page {i} successfully.")
    # if the page couldn't be fetched
    except:
        print(f"Cannot fetch page {i}")


allNames = []      # list of all the speaker names
allPrices = []      # list of all the speaker prices
allRatings = []      # list of all the speaker ratings
allNumReviews = []    # number of ratings 

print()
# extract data from each page and store it in the above lists
for i in range(len(pages)):
    print("Extracting data from page", i+1)
    page = pages[i]
    soup = BeautifulSoup(page, 'html.parser')
    

    # data for each speaker
    all_div = soup.find_all('div', class_="_3liAhj")
    for div in all_div:
        name = div.find('a', class_='_2cLu-l')
        price = div.find('div', class_='_1vC4OE')
        rating = div.find('div', class_='hGSR34')
        numReviews = div.find('span', class_="_38sUEc")
        
        if name:
            allNames.append(name.text)
        else:
            allNames.append("Unknown")

        if price:
            allPrices.append(price.text)
        else:
            allPrices.append("0")

        if rating:
            allRatings.append(rating.text)
        else:
            allRatings.append("0")

        if num_reviews:
            # remove ending and trailing bracket and remove ','
            num_reviews_text = num_reviews.text[:-1]
            num_reviews_text = num_reviews_text[1:].replace(',', '')
            allNumReviews.append(num_reviews_text)
        else:
            allNumReviews.append('0')
        

# create the dataframe 
df = pd.DataFrame({'name':allNames, 'price':allPrices, 'rating':allRatings, 'num_reviews':allNumReviews})

# convert rating and num_reviews col to numerical data types
df['rating'] = df['rating'].astype('float')
df['num_reviews'] = df['num_reviews'].astype('int')

# select rows whose rating and number of reviews match the criteria
df = df[(df['rating'] >= minRatings) & (df.num_reviews >= minNumOfReviews)]
# sort the dataframe by rating (highest rating first)
df = df.sort_values('rating', ascending=False)

# display top 10 items
print("\nTop items:")
print(df.head(10))


# write the data to output file
print("\nWriting data to file", outputFileName)
df.to_csv(outputFileName, index=False)
print("Data saved to file successfully.")
