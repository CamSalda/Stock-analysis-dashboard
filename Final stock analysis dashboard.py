#A. INTRODUCTION: The objective of this project was to develop a fully functional dashboard for stock analysis using Streamlit and several APIs.
# In the dashboard, the user introduces a ticker and a date, and obtains a wide set of information elements from the stock, going from price and financial statements, to recent news and Chat GPT analysis.

#B. INSTALLATIONS AND REQUIREMENTS: For the execution of this code it is needed to install the next packages:

# 1. streamlit for the web interface: pip3 install streamlit
# 2. pandas for the use of Data Frames: pip3 install pandas
# 3. numpy for data manipulation: pip3 install numpy
# 4. yfinance for the API of the stock prices: pip3 install yfinance
# 5. yahoo_fin for the API of the financial ratios and the qualitative information: pip3 install yahoo_fin
# 6. pandas_ta for the technical analysis indicators: pip3 install pandas_ta
# 7. requests_html to run yahoo_fin correctly: pip3 install requests_html
# 8. matplotlib for the graphic representations:pip3 install matplotlib
# 9. plotly for graphic representations also: pip3 install plotly
# 10. alpha_vantage to obtain the financial statements: pip3 install alpha_vantage
# 11. chat GPT API to consult Chat GPT: pip3 install openai

# For the execution of the project, I used Pycharm with a virtual environment, therefore it is important to install manually the packages in the virtual environment using the interpreter settings.
# Streamlit applications are not ran with the traditional "run" command. To run a Streamlit application you must introduce in the terminal: Streamlit run PthonPr.py
# For the use of Alpha Vantage API it is necessary to create an account and obtain a key according to the website: https://www.alphavantage.co/support/#api-key
# For the use of Chat GPT's API it is necessary to create a user and login in Chat GPT's web page: https://chat.openai.com/auth/login, additionally it is necessary to obtain an API key on https://platform.openai.com/account/api-keys

#C. IMPORT PACKAGES

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import yahoo_fin.stock_info as si
import pandas_ta as ta
import matplotlib.pyplot as plt
import plotly.express as px
from alpha_vantage.fundamentaldata import FundamentalData
import openai




# D. TITLE
# I added the University's logo, the titles and subtitles
st.image(
    'https://upload.wikimedia.org/wikipedia/fr/2/2c/Universit%C3%A9_Panth%C3%A9on-Sorbonne_%28depuis_janvier_2015%29.svg')
st.title("Cours de Data Science appliqué en finance")
st.header("Travaille final")
st.write('-SALDARRIAGA Juan Camilo')
st.header('')
st.header('')
st.title('Selected stock dashboard')

#E. DATE AND TICKER
# In the side-bar I added the spaces for the user to write the ticker the dates for the consultation.
st.sidebar.header("Please insert a stock ticker and the date range")
ticker = st.sidebar.text_input('Stock ticker')
start_date = st.sidebar.date_input('Start date')
end_date = st.sidebar.date_input('End date')

#I added an "if" function for the cases in which the user has not provided a ticker, in these cases, instead of an error, the program will send a message asking for the ticker
if ticker=="":
    st.header("Please insert a valid ticker")
else:

#F. PRICE PLOT:

    #5. Using the ticker and dates from the side-bar,I downloaded the data from Yahoo Finance and plot the price
    data = yf.download(ticker, start=start_date, end=end_date)

    fig, ax = plt.subplots()
    ax.plot(data.index, data['Adj Close'])
    plt.title(ticker)
    plt.ylabel('stock price')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("")
    st.subheader("")
    st.subheader("")

#G.QUANTITATIVE INFORMATION

    st.header(" Quantitative information")
    # I created the 4 Tabs that will contain the quantitative information
    pricing_data, financial_statements, fundamentals, other_data = st.tabs(
        ["Pricing data", 'Financial statements', 'Fundamentals and key data ', 'Additional financial data'])

    # G.1 PRICING DATA
    # I filled the first tab with the table of price info and some basic statistics for the period
    with pricing_data:
        st.subheader('Daily pricing data')
        data2 = data
        data2['Percentual change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
        data2.dropna(inplace=True)
        st.write(data2)

        # I provided the highest, lowest and median closing price
        highest_cp = round(np.max(data['Adj Close']), 2)
        lowest_cp = round(np.min(data['Adj Close']), 2)
        median_cp = round(np.median(data['Adj Close']), 2)
        st.write('The period \'s highest price is=', highest_cp)
        st.write('The period\'s lowest price is=', lowest_cp)
        st.write('The period\'s median price is =', median_cp)

        # Now I calculate some basic metrics for the return during the selected period
        annual_return = round(data2['Percentual change'].mean() * 100, 4)
        st.write('The period\'s mean return is=', annual_return, '%')
        stdev = round(np.std(data2['Percentual change']) * 100, 4)
        st.write('The period\'s return standard deviation is=', stdev, '%')
        st.write('The period\'s risk-adjusted return is=', round(annual_return / (stdev * 100), 4), '%')

    #G.2 FINANCIAL STATEMENTS
    # Now I use the Alpha Vantage API, which is a provider of financial data. To access the API I must obtain an API key from the webpage:https://www.alphavantage.co/support/#api-key
    # As this is a free version of the API, it only supports 5 calls per minute and 500 calls per day. Therefore, if several consultations are made in a reduced time-lapse it will throw and error asking for a premium upgrade
    with financial_statements:
        st.subheader('Financial Statements')
        st.write("")
        st.write("")
        st.write("")

        #I import the balance sheet
        st.subheader('Balance Sheet')
        key = 'XZDSJSKPLGN96HER'
        fd = FundamentalData(key, output_format='pandas')
        balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
        bs = balance_sheet.T[2:]
        bs.columns = list(balance_sheet.T.iloc[0])
        st.write(bs)

        #I import the income statement
        st.subheader('Income Statement')
        income_statement = fd.get_income_statement_annual(ticker)[0]
        is1 = income_statement.T[2:]
        is1.columns = list(income_statement.T.iloc[0])
        st.write(is1)

        #I import the cash flow
        st.subheader('Cash Flow Statement')
        cash_flow = fd.get_cash_flow_annual(ticker)[0]
        cf = cash_flow.T[2:]
        cf.columns = list(cash_flow.T.iloc[0])
        st.write(cf)

    #G.3 FUNDAMENTALS
    #From the yahoo_fin.stock_info package I import a table with the fundamentals of the stock
    with fundamentals:
        st.subheader('Valuation ratios')
        st.write(si.get_quote_table(ticker, dict_result=False))

    #G.4 ADDITIONAL FINANCIAL DATA
    # In the other_data tab I will add a list of indicators from pandas_ta package
    with other_data:
        st.header('Additional financial data')
        # I create the dataframe library
        df = pd.DataFrame()
        # I generate a dataframe with all the list of technical indicators available in the pandas_ta library
        ind_list = df.ta.indicators(as_list=True)
        # I add a dropdown list whose options are the elements of the dataframe
        st.subheader('Technical indicator')
        technical_indicator = st.selectbox('Please select a technical indicator', options=ind_list)
        # With the indicator selected by the user, I extract the information. For getattr I must specify the columns from the yahoo finance data frame
        method = technical_indicator
        indicator = pd.DataFrame(
            getattr(ta, method)(low=data['Low'], close=data['Close'], high=data['High'], open=data['Open'],
                                volume=data['Volume']))
        indicator['Close'] = data['Close']
        st.write("Graph of the technical indicator selected for the close price")
        figw_ind_new = px.line(indicator)
        st.plotly_chart(figw_ind_new)
        st.write("Data of the technical indicator selected for the close price")
        st.write(indicator)

    st.subheader("")
    st.subheader("")
    st.subheader("")

#H. QUALITATIVE INFORMATION

    #For this section I will be using a different Yahoo Finance API: yfinance
    st.header("Qualitative information")
    #I create the set of tabs that will contain the data
    business_description, ownership_data, management_data, news = st.tabs(
        ["Business description", 'Ownership data', "Management data", 'Top 5 related news'])

    #I create the consultation variable to use it with the yfinance API
    consultation = yf.Ticker(ticker)

    #H.1 BUSINESS DESCRIPTION
    #Using the yfinance method on consultation I obtain the business summary
    with business_description:
        st.subheader('Business description')
        st.write('Industry: ', consultation.get_info()["industry"])
        st.write('Business summary: ', consultation.get_info()["longBusinessSummary"])

    #H.2 OWNERSHIP DATA
    #Using the yfinance method on consultation I obtain the ownership data
    with ownership_data:
        st.subheader('Ownership data')
        st.write("Major holders breakdown")
        st.write(si.get_holders(ticker)["Major Holders"])
        st.write("Top institutional holders")
        st.write(si.get_holders(ticker)["Top Institutional Holders"])

    #H.3 MANAGEMENT DATA
    # Using the yfinance method on consultation on a loop, I obtain the main 5 executives of the company
    with management_data:
        st.subheader('5 main executives')
        for i in range(5):
            st.write('Main executive ', i + 1)
            st.write('Name: ', consultation.get_info()["companyOfficers"][i]["name"])
            st.write('Age: ', consultation.get_info()["companyOfficers"][i]["age"])
            st.write('Position: ', consultation.get_info()["companyOfficers"][i]["title"])
            st.write('  ')
            st.write('  ')
            st.write('  ')

    #H.4 NEWS
    # Using the yfinance method on consultation on a loop, I obtain the 5 latest news on the company
    with news:
        st.subheader('Main 5 news')
        consultation = yf.Ticker(ticker)

        for i in range(5):
            st.write('News numer ', i + 1)
            st.write('Age: ', consultation.get_news()[i]["title"])
            st.write('Age: ', consultation.get_news()[i]["publisher"])
            st.write('Age: ', consultation.get_news()[i]["link"])
            st.write('  ')
            st.write('  ')
            st.write('  ')

#I.STRATEGIC ANALYSIS
    #In this section I will develop a strategic analysis using Chat GPT's official API
    #it is necessary to create a user and login in ChatGPT's web page: https://chat.openai.com/auth/login, additionally it is necessary to obtain an API key on https://platform.openai.com/account/api-keys
    openai.api_key = "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"
    st.subheader("")
    st.subheader("")
    st.subheader("")
    st.header("Strategic analysis")

    #I create the tabs for the strategical analysis section
    reasons_buy, reasons_sell, swot = st.tabs(["Chat GPT: reasons to buy", "Chat GPT: reasons to sell", "Chat GPT: SWOT analysis"])

    #I.1 REASONS TO BUY
    # I ask Chat GPT to provide 3 reasons to buy the selected stock and import the results
    #For this I replicate the code specified in Openai website's https://platform.openai.com/docs/api-reference/authentication
    with reasons_buy:
        st.subheader(f"3 reasons to buy {ticker} stock")
        #I create the variable completion with the question made to Chat GPT and the answer
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Give me 3 reasons to buy {ticker} stock"}])
        #I print ChatGPT's answer
        st.write(completion.choices[0].message.content)

    #I.2 REASONS TO SELL
    # I ask Chat GPT to provide 3 reasons to sell the selected stock and import the results
    with reasons_sell:
        st.subheader(f"3 reasons to sell {ticker} stock")
        #I create the variable completion2 with the question made to Chat GPT and the answer
        completion2 = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Give me 3 reasons to sell {ticker} stock"}])
        # I print ChatGPT's answer
        st.write(completion2.choices[0].message.content)

    #I.3 SWOT
    with swot:
        st.subheader(f"SWOT analysis")
        #I create the variable completion3 with the question made to Chat GPT and the answer
        completion3 = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Give me a SWOT analysis of {ticker} stock"}])
        # I print ChatGPT's answer
        st.write(completion3.choices[0].message.content)



#J REFERENCES

#On Alpha Vantage
# https://www.alphavantage.co/support/#api-key
# https://www.youtube.com/watch?v=fdFfpEtv5BU&list=PLxvRLWqiBMjq01Ge8vpMfdYcgSjj0uVRf&index=3
# https://pub.towardsai.net/technical-analysis-with-python-quickstart-guide-for-pandas-ta-fe4b152e95a2

#On Matplotlib
# https://www.datacamp.com/tutorial/matplotlib-tutorial-python

#On Openai's Chat GPT API
# https://platform.openai.com/docs/api-reference/making-requests
# https://platform.openai.com/docs/api-reference/authentication
# https://www.youtube.com/watch?v=XxIfSkkyAaQ

#On plotly
# https://www.datacamp.com/courses/introduction-to-data-visualization-with-plotly-in-python

#On PyCharm
# https://www.youtube.com/watch?v=56bPIGf4us0

#On Streamlit:
# https://docs.streamlit.io/library/get-started/create-an-app
# https://towardsdatascience.com/streamlit-from-scratch-getting-started-f4baa7dd6493#:~:text=The%20consequence%20of%20this%20is,command%20in%20a%20command%20window
# https://blog.streamlit.io/how-to-build-a-real-time-live-dashboard-with-streamlit/
# https://www.youtube.com/watch?v=zHAM5MGehV8&list=PLxvRLWqiBMjq01Ge8vpMfdYcgSjj0uVRf
# https://www.youtube.com/watch?v=oIzFaVr1Bm8&list=PLxvRLWqiBMjq01Ge8vpMfdYcgSjj0uVRf&index=2

#On Yahoo Finance API's
# https://algotrading101.com/learn/yahoo-finance-api-guide/
# https://www.youtube.com/watch?v=IMCbi6cvRmY
# https://www.qmr.ai/yfinance-library-the-definitive-guide/







