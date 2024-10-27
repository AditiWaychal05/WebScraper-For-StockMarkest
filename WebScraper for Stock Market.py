import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_stock_data(stock_symbol):
    # user defined URL
    url = "https://finance.yahoo.com/quote/" + stock_symbol
    
    # Send GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find elements containing stock price and company name (details)
        price_element = soup.find("div", {"class": "D(ib) Mend(20px)"})
        name_element = soup.find("h1", {"class": "D(ib) Fz(18px)"})
        prev_close_element = soup.find("td", {"data-test": "PREV_CLOSE-value"})
        market_cap_element = soup.find("td", {"data-test": "MARKET_CAP-value"})
        volume_element = soup.find("td", {"data-test": "TD_VOLUME-value"})
        change_element = soup.find("span", {"data-reactid": "50"})
        high_low_element = soup.find_all("td", {"class": "Ta(end) Fw(600) Lh(14px)"})
        
        # Extract text from elements
        stock_price = price_element.find("span").text if price_element else "N/A"
        company_name = name_element.text if name_element else "N/A"
        prev_close = prev_close_element.text if prev_close_element else "N/A"
        market_cap = market_cap_element.text if market_cap_element else "N/A"
        volume = volume_element.text if volume_element else "N/A"
        change = change_element.text if change_element else "N/A"
        if len(high_low_element) >= 2:
            day_high = high_low_element[0].text
            day_low = high_low_element[1].text
        else:
            day_high = "N/A"
            day_low = "N/A"
        
        # Scrape news headlines
        news_headlines = []
        news_articles = soup.find_all("h3", {"class": "Mb(5px)"})
        for article in news_articles:
            news_headlines.append(article.text)
        
        return {"Company Name": company_name, 
                "Stock Price": stock_price,
                # cureent trading price of single share
                "Previous Close": prev_close,
                # closing price of financial instrument from most recent trading session
                "Market Cap": market_cap,
                # total value of company's outstanding shares of stock
                "Volume": volume,
                # refers to how many shares of a stock or contracts of a commodity are traded in a given period
                "Change": change,
                # difference between current price of stock and it's previous closing price
                "Day's High": day_high,
                # highest price at which particular stock has traded during current trading session
                "Day's Low": day_low,
                # lowest price at which particular stock has traded during current trading session
                "News Headlines": news_headlines}
    else:
        print("Failed to fetch data")
        return None

def main():
    stock_symbol = input("Enter stock symbol (e.g., AAPL): ")
    stock_data = scrape_stock_data(stock_symbol)
    if stock_data:
        print("Stock Information:")
        print("Company Name:", stock_data['Company Name'])
        print("Stock Price:", stock_data['Stock Price'])
        print("Previous Close:", stock_data['Previous Close'])
        print("Market Cap:", stock_data['Market Cap'])
        print("Volume:", stock_data['Volume'])
        print("Change:", stock_data['Change'])
        print("Day's High:", stock_data['Day\'s High'])
        print("Day's Low:", stock_data['Day\'s Low'])
        print("News Headlines:")
        for headline in stock_data['News Headlines']:
            print("-", headline)
    else:
        print("Failed to retrieve stock data.")

if __name__ == "__main__":
    main()

 
