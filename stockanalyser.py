from datetime import datetime, timedelta
import streamlit as st 
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
 
mag7 = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "NVDA"]

st.title("5 Day Stock Performance")

end_date = datetime.now() #Finding the end date 
start_date = end_date - timedelta(days=7) #Finding 5 days before
ticker = st.selectbox("Enter Stock Ticker:", mag7).upper() #Get the ticker input and capitalise
for x in mag7:
    if ticker != x:
        print("Please only input a stock from the Magnificient 7!")

if ticker:
    try:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=7)
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        
        if stock_data.empty:
            st.warning("No data found!")
        else:
            stock_data = stock_data.tail(5)
            stock_data['SMA'] = stock_data['Close'].rolling(window=5).mean(0)
            st.subheader(f"Last 5 Trading Days: {ticker}")
            st.dataframe(stock_data[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA']])
            
            fig, ax = plt.subplots()
            ax.plot(stock_data.index, stock_data['Close'], marker='o', label='Close Price')

            # Find highest and lowest close prices
            min_close = float(stock_data['Close'].min())
            max_close = float(stock_data['Close'].max())
            min_date = stock_data['Close'].idxmin()
            max_date = stock_data['Close'].idxmax()

            # Highlight the min and max points
            ax.scatter(min_date, min_close, color='red', label='Lowest', zorder=5)
            ax.scatter(max_date, max_close, color='green', label='Highest', zorder=5)

            # Annotate the points
            ax.annotate(f'{min_close:.2f}', (min_date, min_close),
                        textcoords="offset points", xytext=(0, -15), ha='center', color='red', fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="none", lw=1))
            ax.annotate(f'{max_close:.2f}', (max_date, max_close),
                        textcoords="offset points", xytext=(0, 10), ha='center', color='green', fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="none", lw=1))

            # Chart formatting
            ax.set_title(f"{ticker} - Closing Price (Last 5 Days)")
            date_format = DateFormatter('%b %d')  #Example: 'Sep 22'
            all_dates = stock_data.index
            reduced_dates = all_dates[::1]
            ax.set_xticks(reduced_dates)
            ax.xaxis.set_major_formatter(date_format)
            ax.set_ylabel("Price (USD)")
            ax.grid(True)
            ax.legend()

            # Display the plot in Streamlit
            st.pyplot(fig)
    except Exception as e:
        st.error(f"An error occurred: {e}")