from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape_flipkart(search_term):
    search = search_term.replace(' ', '%20')

    url = "https://www.flipkart.com/search?q=" + search

    headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'})
    proxies = {
    "http": "",
    "https": "",
    }

    webpage = requests.get(url, headers=headers)

    # Parse the content
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Find the product containers
    product_class_names = ["_2kHMtA", "_4ddWXP"]
    products = soup.find_all("div", class_=product_class_names)

    # Find the product names from products
    product_name = []
    for product in products:
        product_element = product.find("a", class_="s1Q9rs")
        if product_element is None:
            product_element = product.find("div", class_="_4rR01T")
        if product_element is not None:
            product_name.append(product_element.text)
        else:
            product_name.append("N/A")

    # Find the product prices from products
    product_price = []
    for product in products:
        price_element = product.find("div", class_="_30jeq3")
        if price_element is None:
            price_element = product.find("div", class_="_30jeq3 _1_WHN1")
        if price_element is not None:
            product_price.append(price_element.text)
        else:
            product_price.append("N/A")

    # Find the product links from products
    product_link = []
    for product in products:
        link_element = product.find("a", class_="s1Q9rs")
        if link_element is not None:
            link_element = link_element.get('href')
            product_link.append("https://www.flipkart.com" + link_element)
        else:
            div_element = product.find("a", class_="_1fQZEK")
            if div_element is not None:
                try:
                    link_element = div_element.get('href')
                    product_link.append("https://www.flipkart.com" + link_element)
                except AttributeError:
                    product_link.append("N/A")
            else:
                product_link.append("N/A")

    # iterate over the list and print the product name, price and link
    # for i in range(len(product_name)):
    #     print("Product Name: ", product_name[i])
    #     print("Product Price: ", product_price[i])
    #     print("Product Link: ", product_link[i])
    #     print("")

    # Create a dataframe
    df = pd.DataFrame({"Product Name": product_name, "Product Price": product_price, "Product Link": product_link})
    return df

    # Save the dataframe to a csv file
    # df.to_csv("flipkart_products.csv", index=False)




