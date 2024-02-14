import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from process_data import process
import humanize

# Load data
df = process()  # Replace "df.csv" with the path to your CSV file
df = df.sort_values('Date')

# Sidebar for page selection
st.sidebar.header("Marketing Dashboard")
page = st.sidebar.radio("", ["Overview", "Details", "Meeting Plan"], index=0, key='page')

# Main Overview Page
if page == "Overview":
    st.title("Overview")
    
    # Define the metrics and their formulas
    metrics = {
        "CPC": r"CPC = \frac{Spend}{Clicks}",
        "CPI": r"CPI = \frac{Spend}{Installs}",
        "CTR": r"CTR = \frac{Clicks}{Impressions} \times 100\%",
        "Conversion Rate": r"Conversion Rate = \frac{Orders}{Clicks} \times 100\%",
        "CPM": r"CPM = \frac{Spend}{Impressions} \times 1000\%",
        "Cost Per Order": r'Cost Per Order = \frac{Spend}{Orders}'
    }
    # Display each metric and its formula in an expandable field
    with st.expander("Show Metric Formulas"):
        for metric, formula in metrics.items():
            st.write(f"**{metric}:**")
            st.latex(formula)
            
    # Weekly overview
    # Filter data for the last week and the previous week
    last_week = df[df['Date'] >= df['Date'].max() - pd.DateOffset(weeks=1)]
    previous_week = df[(df['Date'] >= df['Date'].max() - pd.DateOffset(weeks=2)) & (df['Date'] < df['Date'].max() - pd.DateOffset(weeks=1))]

    # Calculate total numbers and metrics for the last week
    total_spend_last_week = last_week['Spend'].sum()
    total_impressions_last_week = last_week['Impressions'].sum()
    total_clicks_last_week = last_week['Clicks'].sum()
    total_installs_last_week = last_week['Installs'].sum()
    total_orders_last_week = last_week['Total_Orders'].sum()
    avg_cpi_last_week = last_week['CPI'].mean()
    avg_ctr_last_week = last_week['CTR'].mean()
    avg_cpc_last_week = last_week['CPC'].mean()
    avg_conv_last_week = last_week['Conversion_Rate'].mean()
    avg_cpconv_last_week = last_week['CPM'].mean()
    avg_cpm_last_week = last_week['CPM'].mean()
    avg_cpo_last_week = last_week['Cost_Per_Order'].mean()
    # Calculate total numbers and metrics for the previous week
    total_spend_previous_week = previous_week['Spend'].sum()
    total_impressions_previous_week = previous_week['Impressions'].sum()
    total_clicks_previous_week = previous_week['Clicks'].sum()
    total_installs_previous_week = previous_week['Installs'].sum()
    total_orders_previous_week = previous_week['Total_Orders'].sum()
    avg_cpi_previous_week = previous_week['CPI'].mean()
    avg_ctr_previous_week = previous_week['CTR'].mean()
    avg_cpc_previous_week = previous_week['CPC'].mean()
    avg_conv_previous_week = previous_week['Conversion_Rate'].mean()
    avg_cpconv_previous_week = previous_week['CPM'].mean()   
    avg_cpm_previous_week = previous_week['CPM'].mean()
    avg_cpo_previous_week = previous_week['Cost_Per_Order'].mean()
    
    st.subheader("Weekly View & Change Over Previous Week")
    col1_weekly, col2_weekly, col3_weekly, col4_weekly, col5_weekly = st.columns(5)
    # Calculate changes for raw numbers and percentage changes for metrics
    spend_diff = total_spend_last_week - total_spend_previous_week
    impressions_diff = total_impressions_last_week - total_impressions_previous_week
    clicks_diff = total_clicks_last_week - total_clicks_previous_week
    installs_diff = total_installs_last_week - total_installs_previous_week
    orders_diff = total_orders_last_week - total_orders_previous_week

    cpi_pct_change = (avg_cpi_last_week - avg_cpi_previous_week) / avg_cpi_previous_week * 100
    ctr_pct_change = (avg_ctr_last_week - avg_ctr_previous_week) / avg_ctr_previous_week * 100
    cpc_pct_change = (avg_cpc_last_week - avg_cpc_previous_week) / avg_cpc_previous_week * 100
    cpm_pct_change = (avg_cpm_last_week - avg_cpm_previous_week) / avg_cpm_previous_week * 100
    cpo_pct_change = (avg_cpo_last_week - avg_cpo_previous_week) / avg_cpo_previous_week * 100
    conv_pct_change = (avg_conv_last_week - avg_conv_previous_week) / avg_conv_previous_week * 100
    cpconv_pct_change = (avg_cpconv_last_week - avg_cpconv_previous_week) / avg_cpconv_previous_week * 100
    
    # Display the metrics with formatted numbers and percentage change

    col1_weekly.metric("Spend", humanize.intword(total_spend_last_week), humanize.intword(spend_diff))
    col2_weekly.metric("Impressions", humanize.intword(total_impressions_last_week), humanize.intword(impressions_diff))
    col3_weekly.metric("Clicks", humanize.intword(total_clicks_last_week), humanize.intword(clicks_diff))
    col4_weekly.metric("Installs", humanize.intword(total_installs_last_week), humanize.intword(installs_diff))
    col5_weekly.metric("Orders", humanize.intword(total_orders_last_week), humanize.intword(orders_diff))
    col6_weekly, col7_weekly, col8_weekly, col9_weekly , col10_weekly  = st.columns(5)
    col6_weekly.metric("CPI", f"{avg_cpi_last_week:.2f}", f"{cpi_pct_change:.1f}%")
    col7_weekly.metric("CTR", f"{avg_ctr_last_week:.2f}%", f"{ctr_pct_change:.1f}%")
    col8_weekly.metric("CPC", f"{avg_cpc_last_week:.2f}", f"{cpc_pct_change:.1f}%")
    col9_weekly.metric("CPM", f"{avg_cpm_last_week:.2f}%", f"{cpm_pct_change:.1f}%")
    col10_weekly.metric("CPO", f"{avg_cpo_last_week:.2f}", f"{cpo_pct_change:.1f}%")
            
    st.write("")
    # Total numbers and metrics
    st.subheader("Full Date View")
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    
    with col1:
        st.write("Total Spend")
        st.write(f"{df['Spend'].sum():,.0f}", "EUR", type="card", key="total_spend", width=150, height=100, border=True, background="grey", padding=5)

    with col2:
        st.write("Impressions")
        st.write(f"{df['Impressions'].sum():,.0f}", type="card", key="impressions", width=150, height=100, border=True, background="grey", padding=5)

    with col3:
        st.write("Clicks")
        st.write(f"{df['Clicks'].sum():,.0f}", type="card", key="clicks", width=150, height=100, border=True, background="grey", padding=5)

    with col4:
        st.write("Installs")
        st.write(f"{df['Installs'].sum():,.0f}", type="card", key="installs", width=150, height=100, border=True, background="grey", padding=5)

    with col5:
        st.write("Orders")
        st.write(f"{df['Total_Orders'].sum():,.0f}", type="card", key="orders", width=150, height=100, border=True, background="grey", padding=5)

    with col6:
        st.write("CPI")
        st.write(f"{df['CPI'].mean():.2f}", type="card", key="cpi", width=150, height=100, border=True, background="grey", padding=5)

    with col7:
        st.write("CTR")
        st.write(f"{df['CTR'].mean():.2f}%", type="card", key="ctr", width=150, height=100, border=True, background="grey", padding=5)

    with col8:
        st.write("CPC")
        st.write(f"{df['CPC'].mean():.2f}", type="card", key="cpc", width=150, height=100, border=True, background="grey", padding=5) 
    st.write("")
    
    # 1. Table showing raw numbers for Impressions, Clicks, and Spend for each Source
    st.subheader("Breakdown of numbers by category selected")
    category = st.radio("Select Category", ["Source", "Country", "Pricing_Model", "Platform", 'Budget'], index=0, key='category')
    
    st.write(f"Numbers for Impressions, Clicks, and Spend by {category}")
    source_stats = df.groupby(category).agg({'Impressions': 'sum', 'Clicks': 'sum', 'Spend': 'sum'}).reset_index()
    st.write(source_stats)

    # 2. Pie charts for Impressions, Clicks, Spend based on Source
    st.write(f"Pie charts for Impressions, Clicks, Spend based on {category}")
    fig_pie_impressions = px.pie(df, values='Impressions', names=category, title='Impressions')
    fig_pie_clicks = px.pie(df, values='Clicks', names=category, title='Clicks')
    fig_pie_spend = px.pie(df, values='Spend', names=category, title='Spend')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(fig_pie_impressions, use_container_width=True)
    with col2:
        st.plotly_chart(fig_pie_clicks, use_container_width=True)
    with col3:
        st.plotly_chart(fig_pie_spend, use_container_width=True)

    # 3. Bar charts for CPC and CTR based on Source
    
    st.write(f"Bar charts for CPC and CTR based on {category} Selected")
    avg_cpc = df.groupby(category)['CPC'].mean().reset_index()
    avg_ctr = df.groupby(category)['CTR'].mean().reset_index()
    # Calculate average CPI while excluding null values and zeros
    avg_cpi = df.groupby(category)['CPI'].mean().reset_index()
    
    fig_bar_cpc = px.bar(avg_cpc, x=category, y='CPC', title='Average CPC by Category', width=500, height=400)
    fig_bar_ctr = px.bar(avg_ctr, x=category, y='CTR', title='Average CTR by Category', width=500, height=400)
    fig_bar_cpi = px.bar(avg_cpi, x=category, y='CPI', title='Average CPI by Category', width=500, height=400)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.plotly_chart(fig_bar_cpc, use_container_width=True)
    with col5:
        st.plotly_chart(fig_bar_ctr, use_container_width=True)
    with col6:
        st.plotly_chart(fig_bar_cpi, use_container_width=True)
        
    # 4. Bar charts for Conversion Rate and CPM based on Source
    st.write(f"Bar charts for Conversion Rate and CPM based on {category}")
    avg_convrate = df[(df['Conversion_Rate'].notna()) & (df['Conversion_Rate'] != float('inf'))].groupby(category)['Conversion_Rate'].mean().reset_index()      
    avg_cpconv= df[(df['CPM'].notna()) & (df['CPM'] != float('inf'))].groupby(category)['CPM'].mean().reset_index()      
    
    fig_bar_conv_rate = px.bar(avg_convrate, x=category, y='Conversion_Rate', title='Average Conversion Rate by Category', width=500, height=400)
    fig_bar_cpconv = px.bar(avg_cpconv, x=category, y='CPM', title='Average CPM by Category', width=500, height=400)
    
    col7, col8 = st.columns(2)
    with col7:
        st.plotly_chart(fig_bar_conv_rate, use_container_width=True)
    with col8:
        st.plotly_chart(fig_bar_cpconv, use_container_width=True)
      
# Details Page
elif page == "Details":
    st.title("Details")
    # Multi-selection for filtering by source and pricing model
    st.sidebar.subheader("Filters")
    campaign_filter = st.sidebar.text_input("Search Campaign:")

    date_range = st.sidebar.date_input("Select Date Range:", [df['Date'].min(), df['Date'].max()])
    selected_sources = st.sidebar.multiselect("Select Source(s):", options=df['Source'].unique(), default=df['Source'].unique())
    selected_pricing_models = st.sidebar.multiselect("Select Pricing Model(s):", options=df['Pricing_Model'].unique(), default=df['Pricing_Model'].unique())
    selected_platforms = st.sidebar.multiselect("Select Platform(s):", options=df['Platform'].unique(), default=df['Platform'].unique())
    selected_budget = st.sidebar.multiselect("Select Budget(s):", options=df['Budget'].unique(), default=df['Budget'].unique())
    selected_country = st.sidebar.multiselect("Select Country(s):", options=df['Country'].unique(), default=df['Country'].unique())
    
    filtered_df = df[(df['Source'].isin(selected_sources)) & (df['Pricing_Model'].isin(selected_pricing_models)) & (df['Platform'].isin(selected_platforms)) 
                     & (df['Budget'].isin(selected_budget)) & (df['Country'].isin(selected_country)) & (df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])]
    
    if campaign_filter:
        filtered_df = filtered_df[filtered_df['Campaign'].str.contains(campaign_filter, case=False)]
        
    filtered_df['Month_Week'] = filtered_df['Date'].dt.strftime('%Y-%m Week %U')
    
    # 1. Impressions
    st.subheader("Impressions and CTR over Time")
    # Graph for order per spend
    grouped_per_week = filtered_df.groupby('Month_Week', as_index=False).agg({"Impressions": "sum", "CTR": 'mean',
                                                                                    'Clicks': 'sum', 'CPC': 'mean',
                                                                                    'Installs': 'sum', 'CPI': 'mean'})
    impressions_ctr = px.bar(grouped_per_week, x='Month_Week', y='Impressions', title='Impressions vs CTR')

    # Add Total Order/Installs Ratio line
    impressions_ctr.add_scatter(x=grouped_per_week['Month_Week'], y=grouped_per_week['CTR'], 
                            mode='markers', name='CTR', yaxis='y2', marker_color='green')

    # Update layout to include two y-axes
    impressions_ctr.update_layout(yaxis=dict(title='Impressions', color='blue', side='left'),
                    yaxis2=dict( color='red', overlaying='y', side='right'),
                    legend=dict(y=0.3, traceorder='reversed'))

    st.plotly_chart(impressions_ctr, use_container_width=True)
    
    # 2. Clicks
    st.subheader("Clicks and CPC over Time")
    # Graph for order per spend
    clicks_cpc = px.bar(grouped_per_week, x='Month_Week', y='Clicks', title='CLicks vs CPC')

    # Add Total Order/Installs Ratio line
    clicks_cpc.add_scatter(x=grouped_per_week['Month_Week'], y=grouped_per_week['CPC'], 
                            mode='markers', name='CPC', yaxis='y2', marker_color='green')

    # Update layout to include two y-axes
    clicks_cpc.update_layout(yaxis=dict(title='Clicks', color='blue', side='left'),
                    yaxis2=dict( color='red', overlaying='y', side='right'),
                    legend=dict(y=0.3, traceorder='reversed'))

    st.plotly_chart(clicks_cpc, use_container_width=True)
    
    # 3. Installs
    st.subheader("Installs and CPI over Time")
    # Graph for order per spend
    installs_cpi = px.bar(grouped_per_week, x='Month_Week', y='Installs', title='Installs vs CPI')

    # Add Total Order/Installs Ratio line
    installs_cpi.add_scatter(x=grouped_per_week['Month_Week'], y=grouped_per_week['CPI'], 
                            mode='markers', name='CPI', yaxis='y2', marker_color='green')

    # Update layout to include two y-axes
    installs_cpi.update_layout(yaxis=dict(title='Installs', color='blue', side='left'),
                    yaxis2=dict( color='red', overlaying='y', side='right'),
                    legend=dict(y=0.3, traceorder='reversed'))

    st.plotly_chart(installs_cpi, use_container_width=True)   
    
    # 4. Graph for order per spend
    st.subheader("Spend and CPM over Time")
    grouped_per_week_order = filtered_df.groupby('Month_Week', as_index=False).agg({"Spend": "sum", "CPM": 'mean'})
    order_spend = px.bar(grouped_per_week_order, x='Month_Week', y='Spend', title='CPM vs Spend')

    # Add Total Order/Installs Ratio line
    order_spend.add_scatter(x=grouped_per_week_order['Month_Week'], y=grouped_per_week_order['CPM'], 
                            mode='markers', name='CPM', yaxis='y2', marker_color='green')

    # Update layout to include two y-axes
    order_spend.update_layout(yaxis=dict(title='Spend', color='blue', side='left'),
                    yaxis2=dict( color='red', overlaying='y', side='right'),
                    legend=dict(y=0.3, traceorder='reversed'))

    st.plotly_chart(order_spend, use_container_width=True)
       
    # 5. Cards showing third/first order ratio and first_order/install ratio
    st.subheader("Order Analysis")
    
    order_stats = df.groupby(['Source', 'Platform']).agg({'Installs': 'sum', 'Total_Orders': 'sum', 'Spend': 'sum',
                                                          'First_Order': 'sum', 'Second_Order': 'sum', 'Third_Order': 'sum'}).reset_index()
    st.write(order_stats)
    
    third_first_order_ratio = (filtered_df['Third_Order'].mean() / filtered_df['First_Order'].mean())
    first_order_install_ratio = (filtered_df['First_Order'].mean() / filtered_df['Installs'].mean())
    total_order_install_ratio = (filtered_df['Total_Orders'].mean() / filtered_df['Installs'].mean())
    
    col3, col4, col5 = st.columns(3)
    with col3:
        st.info(f"Third/First Order Ratio: {third_first_order_ratio:.2f}")
    with col4:
        st.info(f"First Order/Install Ratio: {first_order_install_ratio:.2f}")
    with col5:
        st.info(f"Total Orders/Installs Ratio: {total_order_install_ratio:.2f}")
    
    # 6. Search dataset
    grouped_df = filtered_df.groupby('Campaign', as_index=False).agg({'CTR':'mean', 'CPC':'mean', 'CPI':'mean',
                                                     'CPM': 'mean', 'Conversion_Rate':'mean',
                                                     'Platform':'unique', 'Country':'unique', 'Source':'unique',
                                                     'Budget': 'unique', 'Pricing_Model': 'unique'})
    grouped_df = grouped_df[grouped_df['Campaign'].str.contains(campaign_filter, case=False)]
    
 
    st.write("Dataset")
    st.dataframe(grouped_df)
     
    # 7. Graphs per campaign
    st.subheader("Performance per Campaign")
    # Metric selection button
    selected_metric = st.radio("Select Metric", options=['CPM', 'CTR', 'CPC', 'CPI', 'Conversion_Rate'])

    # Group the data by campaign and month_week, aggregating the selected metric
    campaign_date_df = filtered_df.groupby(['Campaign', 'Month_Week']).agg({selected_metric: 'mean'}).reset_index().sort_values('Month_Week')
    campaign_df = filtered_df.groupby(['Campaign', ]).agg({selected_metric: 'mean'}).reset_index()
    
    # Create line charts for each metric
    per_campaign_date = px.line(campaign_date_df, x='Month_Week', y=selected_metric, color='Campaign',)
    per_campaign = px.bar(campaign_df, x='Campaign', y=selected_metric, title='Campaign Performance')
    # Customize the layout
    per_campaign.update_layout(
        xaxis_title='Campaign',
        yaxis_title=selected_metric,
        legend_title='Campaign',
        hovermode='x',
        template='plotly_white',  # You can change the template if needed
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1)
    )
    # Customize the layout
    per_campaign_date.update_layout(
        xaxis_title='Month_Week',
        yaxis_title=selected_metric,
        legend_title='Campaign',
        hovermode=False,
        template='plotly_white',  # You can change the template if needed
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1)
    )
    st.plotly_chart(per_campaign, use_container_width=True)
    campaign_over_time = st.expander("Click to see campaign trends over time")
    with campaign_over_time:
        st.plotly_chart(per_campaign_date, use_container_width=True)
