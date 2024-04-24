import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='Startup Analysis')

df = pd.read_csv('/Users/udayan/Startup_dashboard/startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_investor_details(investor):
    st.title(investor)
    #load recent investments of the investor
    last5_df = df[df['investors'].str.contains(investor)].head().sort_values(by='date')[['date','startup','vertical','city','investors','round','amount']]
    st.subheader('Five most recent investments')
    st.dataframe(last5_df)

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        # Load a bar chart of top 5 highest investment by investor
         big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
         st.subheader("Biggest Investments")
         fig, ax = plt.subplots()
         ax.bar(big_series.index,big_series.values)
         st.pyplot(fig)
    with col2:
        sector_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader("Distribution Of Sector Invested")
        fig1, ax1 = plt.subplots(figsize = (15,15))
        ax1.pie(sector_series,labels= sector_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)
    with col3:
        stage_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader("Distribution Of Rounds")
        fig2, ax2 = plt.subplots()
        ax2.pie(stage_series,labels= stage_series.index,autopct="%0.01f%%")
        st.pyplot(fig2)
    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader("Distribution Of City Invested")
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series,labels= city_series.index,autopct="%0.01f%%")
        st.pyplot(fig3)
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader("YoY Investments")
    fig4, ax4 = plt.subplots(figsize=(5, 3))
    ax4.plot(year_series.index,year_series.values)
    st.pyplot(fig4)





def load_company_detail(startup):
    st.title(startup)
    Industry = df[df['startup'].str.contains(startup)]['vertical'].values[0]
    Sub_Industry = df[df['startup'].str.contains(startup)]['subvertical'].values[0]
    Location = df[df['startup'].str.contains(startup)]['city'].values[0]
    st.subheader(f"Industry - {Industry}")
    st.subheader(f"Sub-Industry - {Sub_Industry}")
    st.subheader(f"Location - {Location}")
    stage = df[df['startup'].str.contains(startup)]['round'].values[0]
    Investors = df[df['startup'].str.contains(startup)]['investors'].values[0]
    Date = df[df['startup'].str.contains(startup)]['date'].values[0]
    st.markdown(
        f"""
        ### Funding Rounds-
        - {stage}
        - {Investors}
        - {Date}
        """
    )


def load_overall_analysis():
    st.title("Overall Analysis")
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        #total invested amount
        total = round(df['amount'].sum())
        st.metric('Total',str(round(total))+ 'Cr')
    with col2:
        #maximum invested amount
        max = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Max Investemenet',str(round(max))+ 'Cr')
    with col3:
        #average of all the investments
        avg = df.groupby('startup')['amount'].sum().mean()
        st.metric('Average Investemenet',str(round(avg))+ 'Cr')
    with col4:
        # Total number of startups
        Total_startups = df['startup'].nunique()
        st.metric('Total Number Of Indian Startups',str(round(Total_startups))  )
    st.header('MoM Graph')
    selected_options = st.selectbox('Select Type',['Total','Count'])
    if selected_options == 'Total':
        temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year','month'])['amount'].count().reset_index()

    
    temp_df['x-axis'] = temp_df['year'].astype('str') + '-' + temp_df['month'].astype('str')
    fig12, ax12 = plt.subplots()
    ax12.plot(temp_df['x-axis'],temp_df['amount'])
    ax12.tick_params(rotation=45)
    ax12.tick_params(labelsize=3)
    st.pyplot(fig12)






option = st.sidebar.selectbox('Select one',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
        load_overall_analysis()

elif option == 'Startup':
    selected_company = st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Detail')
    st.title('Startup Analysis')
    if btn1:
        load_company_detail(selected_company)
else:
    selected_investor = st.sidebar.selectbox('Select Ivestor',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Detail')
    if btn2:
        load_investor_details(selected_investor)


