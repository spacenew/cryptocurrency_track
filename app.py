import requests

import pandas as pd
from datetime import datetime, date, timedelta
import time

import plotly.express as px

import streamlit as st



API_ENDPOINT   = 'https://api.coincap.io/v2/assets/'
ASSET_ENDPOINT = 'https://api.coincap.io/v2/assets?limit=2000'


def get_currencies_id():
    response = requests.get(ASSET_ENDPOINT)
    data = response.json()['data']
    
    return [currency['id'] for currency in data]

def format_df(data):
    
    df = pd.DataFrame(data, columns=['time', 'priceUsd'])
    df['time'] = pd.to_datetime(df['time'], unit='ms') 
    
    return df

def plotting_barchart(df, currency_id):

    fig = px.bar(df, 
                x='time', 
                y='priceUsd', 
                title=f'{currency_id} history price over time')
    return st.plotly_chart(fig)

def convert_date_to_timestamp(date):
    microseconds = time.mktime(date.timetuple()) * 1e6
    return int(round(microseconds / float(1000)))

def run_crypto_tracker():
        
    st.sidebar.title('History Crypto Currency')

    currencies = get_currencies_id()

    currency_id = st.sidebar.selectbox('Select an asset:', currencies)

    default_today     = date.today()
    default_yesterday = default_today - timedelta(days=30)

    from_date = st.sidebar.date_input('Date From', default_yesterday)
    to_date   = st.sidebar.date_input('Date To', default_today)


    if from_date < to_date:
        pass
    else:
        st.error('Error: End date is greater than start date. Change dates')

   
    # Convert the datetime objects to Unix timestamps
    start_date =  convert_date_to_timestamp(from_date)
    end_date   =  convert_date_to_timestamp(to_date)

    if st.sidebar.button('Track'):
        payload = {
            'interval': 'd1',
            'start': start_date,
            'end': end_date
        }
        response = requests.get(f'{API_ENDPOINT}/{currency_id}/history', params=payload)

        data = response.json()['data']

        if response.status_code == 200: 
            data = response.json()
            data = data['data']
        else:
            # Print an error message
            print(f'Request failed with status code {response.status_code}')

        df = format_df(data)

        plotting_barchart(df, currency_id)

        
if __name__ == "__main__":
    run_crypto_tracker()
