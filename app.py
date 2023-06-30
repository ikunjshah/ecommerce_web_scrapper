import streamlit as st
from scraper import scrape

st.set_page_config(page_title="Product Scraper")

st.title("Product Scraper")
st.write("#### This tool allows you to fetch information related to your products from Amazon and Flipkart")

product_name = st.text_input("Enter Product Name:")

if st.button("Find Details"):
    final_df = scrape(product_name)
    st.write("Combined Data:")
    st.dataframe(final_df)
    csv_data = final_df.to_csv(index=False)
    st.download_button(
        label='Download CSV',
        data=csv_data,
        file_name='products.csv',
        mime='text/csv'
    )
