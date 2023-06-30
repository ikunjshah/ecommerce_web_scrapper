from amazon import scrape_amazon;
from flipkart import scrape_flipkart;
import pandas as pd;


def scrape(search_item):
    # Get the search term from the user
    search = search_item

    # Get the data from amazon
    amazon_data = scrape_amazon(search)

    # Get the data from flipkart
    flipkart_data = scrape_flipkart(search)

    # Create a dataframe from the data
    df = pd.concat([amazon_data, flipkart_data], ignore_index=True)
    is_na_row = df.isin(["N/A"]).all(axis=1)
    df = df.drop(df[is_na_row].index)
    return df

    # Save the dataframe to a csv file
    # df.to_csv("products.csv", index=False)
