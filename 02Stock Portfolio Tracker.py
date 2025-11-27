import yfinance as yf
import pandas as pd

class StockPortfolio:
    def __init__(self):
        self.portfolio = pd.DataFrame(columns=['Ticker', 'Shares', 'Buy Price'])

    def add_stock(self, ticker, shares, buy_price):
        
        if ticker in self.portfolio['Ticker'].values:
           
            self.portfolio.loc[self.portfolio['Ticker'] == ticker, 'Shares'] += shares
            self.portfolio.loc[self.portfolio['Ticker'] == ticker, 'Buy Price'] = buy_price
            print(f"Updated {ticker}: Added {shares} shares at ${buy_price:.2f} each.")
        
        else:
            new_stock = pd.DataFrame({'Ticker': [ticker], 'Shares': [shares], 'Buy Price': [buy_price]})
            self.portfolio = pd.concat([self.portfolio, new_stock], ignore_index=True)
            print(f"Added {shares} shares of {ticker} at ${buy_price:.2f} each.")

    def remove_stock(self, ticker):
        if ticker in self.portfolio['Ticker'].values:
            self.portfolio = self.portfolio[self.portfolio['Ticker'] != ticker]
            print(f"Removed {ticker} from the portfolio.")
        else:
            print(f"{ticker} not found in the portfolio.")

    def view_portfolio(self):
        if self.portfolio.empty:
            print("Your portfolio is empty.")
            return
        current_prices = self.get_current_prices()
        self.portfolio['Current Price'] = self.portfolio['Ticker'].map(current_prices)
        self.portfolio['Value'] = self.portfolio['Shares'] * self.portfolio['Current Price']
        print(self.portfolio)

    def get_current_prices(self):
        tickers = self.portfolio['Ticker'].tolist()
        prices = yf.download(tickers, period='1d')['Close'].iloc[-1]
        return prices

    def track_performance(self):
        if self.portfolio.empty:
            print("Your portfolio is empty.")
            return
        current_prices = self.get_current_prices()
        
        self.portfolio['Current Price'] = self.portfolio['Ticker'].map(current_prices)
        self.portfolio['Current Value'] = self.portfolio['Shares'] * self.portfolio['Current Price']
        self.portfolio['Profit/Loss'] = (self.portfolio['Current Price'] - self.portfolio['Buy Price']) * self.portfolio['Shares']
        total_value = self.portfolio['Current Value'].sum()
        total_profit_loss = self.portfolio['Profit/Loss'].sum()
        
        print(self.portfolio[['Ticker', 'Shares', 'Buy Price', 'Current Price', 'Current Value', 'Profit/Loss']])
       
        print(f"\nTotal Portfolio Value: ${total_value:.2f}")
       
        print(f"Total Profit/Loss: ${total_profit_loss:.2f}")

def main():
    tracker = StockPortfolio()

    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Track Performance")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")

        if choice == '1':
            ticker = input("Enter stock ticker: ").upper()
            shares = int(input("Enter number of shares: "))
            buy_price = float(input("Enter buy price per share: "))
            tracker.add_stock(ticker, shares, buy_price)
        
        elif choice == '2':
            ticker = input("Enter stock ticker to remove: ").upper()
            tracker.remove_stock(ticker)
        
        elif choice == '3':
            tracker.view_portfolio()
        
        elif choice == '4':
            tracker.track_performance()
        
        elif choice == '5':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()