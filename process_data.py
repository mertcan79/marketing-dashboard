import pandas as pd
import numpy as np

def process():
    twitter_data = pd.read_csv('data/Twitter Data.csv', skiprows = 5)
    snapchat_data = pd.read_csv('data/Snapchat Data.csv', skiprows = 5)

    twitter_adjust_data = pd.read_csv('data/Twitter-Adjust data.csv', skiprows = 5)
    snapchat_adjust_data = pd.read_csv('data/Snapchat-Adjust data.csv', skiprows = 5)

    twitter_data.columns = ['Date', 'Campaign', 'Campaign_ID', 'Spend', 'Clicks', 'Impressions']
    snapchat_data.columns = ['Date', 'Campaign', 'Campaign_ID', 'Spend', 'Clicks', 'Impressions']

    twitter_adjust_data.columns = ['Date', 'Campaign', 'Installs', 'First_Order', 'Second_Order', 'Third_Order']
    snapchat_adjust_data.columns = ['Date', 'Campaign', 'Installs', 'First_Order', 'Second_Order', 'Third_Order']

    snapchat_adjust_data['Campaign'] = snapchat_adjust_data['Campaign'].str.split().str[0]
    snapchat = snapchat_data.merge(snapchat_adjust_data, on=['Campaign', 'Date'], how='outer')

    twitter_adjust_data['Campaign'] = twitter_adjust_data['Campaign'].str.split().str[0]
    twitter = twitter_data.merge(twitter_adjust_data, on=['Campaign', 'Date'], how='outer')

    twitter['Source'] = 'Twitter'
    snapchat['Source'] = 'Snapchat'

    df = pd.concat([twitter, snapchat], ignore_index=True)

    # Function to extract the country code
    def extract_country_code(campaign):
        parts = campaign.split('_')
        for i, part in enumerate(parts):
            if part in ['performance', 'Performance']:
                return parts[i + 1]  # Country code is after 'Snapchat' or 'Twitter'

    # Apply the function to extract the country code
    df['Country'] = df['Campaign'].apply(extract_country_code)

    def extract_platform(campaign):
        if 'ios' in campaign.lower():
            return 'iOS'
        elif 'android' in campaign.lower():
            return 'Android'
        else:
            return 'All'

    df['Platform'] = df['Campaign'].apply(extract_platform)
    
    def extract_budget(campaign):
        if 'digitalbudget' in campaign.lower():
            return 'Digital_Budget'
        elif 'hqbudget' in campaign.lower():
            return 'HQBudget'
        else:
            return 'Other'

    df['Budget'] = df['Campaign'].apply(extract_budget)
    
    df['CTR'] = df['Clicks'] * 100 / df['Impressions']
    df['CPC'] = df['Spend'] / df['Clicks']

    # Add Pricing_Model column based on Campaign column
    df['Pricing_Model'] = df['Campaign'].apply(lambda x: 'CPI' if 'cpi' in x.lower() else ('CPC' if 'cpc' in x.lower() else 'Other'))
    #Calculate CPI
    df['CPI'] = df['Spend'] / df['Installs']

    # Calculate Conversion Rate
    df['Conversion_Rate'] = df['Installs'] * 100 / df['Clicks']

    # Calculate Cost Per Conversion
    df['CPM'] = df['Spend'] / df['Installs']

    df['Total_Orders'] = df['First_Order'] + df['Second_Order'] + df['Third_Order']
    
    df['Cost_Per_Order'] = df['Spend'] / df['Total_Orders']
    
    df = df.replace(float('inf'), 0)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    return df

if __name__ == "__main__":
    df = process()
    df.to_csv('df.csv')