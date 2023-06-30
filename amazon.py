from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape_amazon(search_term):
    search = search_term.replace(' ', '+')

    url = "https://www.amazon.in/s?k=" + search

    headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'})
    proxies = {
    "http": "",
    "https": "",
    }

    webpage = requests.get(url, headers=headers, proxies=proxies)
    if webpage.status_code == 503:
        print("Amazon is currently blocking our scraper. Please try again later.")

    # Parse the content
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Find the product containers
    product_class_names = ["a-section a-spacing-small puis-padding-left-small puis-padding-right-small", "a-section a-spacing-small a-spacing-top-small"]
    products = soup.find_all("div", class_=product_class_names)

    # Find the product name from products
    product_name = []
    product_element_classes = ["a-size-base-plus a-color-base a-text-normal", "a-size-medium a-color-base a-text-normal"]
    for product in products:
        product_element = product.find("span", class_=product_element_classes)
        if product_element is not None:
            product_name.append(product_element.text)
        else:
            product_name.append("N/A")

    # Find the product price from products and remove the tags
    product_price = []
    for product in products:
        price_element = product.find("span", class_="a-price-whole")
        if price_element is not None:
            product_price.append("₹"+price_element.text)
        else:
            product_price.append("N/A")

    # Find the product links from products and remove the tags
    product_link = []
    for product in products:
        link_element = product.find("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
        if link_element is not None:
            product_link.append("https://www.amazon.in/" + link_element.get('href'))
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
    # df.to_csv("amazon_products.csv", index=False)