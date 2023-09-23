import streamlit as st
from PIL import Image
import mysql.connector as sql
import pulse_dataextraction
import pandas as pd
import plotly.express as px


# #To clone the Github Pulse repository use the following code
# url_name = "https://github.com/PhonePe/pulse.git"
# local_directory = "C://Users//User//Desktop//phonepe pulse data"
# git.Repo.clone_from(url_name,local_directory)

# Calling convert_to_csvfile() fn from pulse_dataextraction file("Extracting data from each JSON file, storing it in a DataFrame, and then converting the DataFrame into a CSV file.")
# pulse_dataextraction.convert_to_csvfile()

# # Creating connection with mysql workbench
connection = sql.connect(host="localhost",
                   user="user",
                   password="password",
                   database  = "phonepe_pulse")
mycursor = connection.cursor(buffered=True)

# # Inserting values into Aggregated Transaction Table:
# df_agg_trans = pulse_dataextraction.extract_aggregated_transactions()
# pulse_dataextraction.insert_values(df_agg_trans,"agg_trans",mycursor,connection)

# Inserting values into Aggregated User Table:
# df_agg_user = pulse_dataextraction.extract_aggregated_user()
# pulse_dataextraction.insert_values(df_agg_user,"agg_user",mycursor,connection)

# Inserting values into Map Transaction Table
# df_map_trans = pulse_dataextraction.extract_map_transactions()
# pulse_dataextraction.insert_values(df_map_trans,"map_trans",mycursor,connection)

# Inserting values into Map User Table
# df_map_user = pulse_dataextraction.extract_map_user()
# pulse_dataextraction.insert_values(df_map_user,"map_user",mycursor,connection)

# Inserting values into Top Transaction Table
# df_top_trans = pulse_dataextraction.extract_top_transactions()
# pulse_dataextraction.insert_values(df_top_trans,"top_trans",mycursor,connection)

# Inserting values into Top User Table
# df_top_user = pulse_dataextraction.extract_top_user()
# for i,row in df_top_user.iterrows():
#     sql = "INSERT INTO top_user VALUES (%s,%s,%s,%s,%s)"
#     mycursor.execute(sql, tuple(row))
#     connection.commit()


# Setting up page configuration
icon = Image.open("phonepeicon.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization & Exploration | By NETHRA R",
                   page_icon= icon,
                   layout= "wide")
st.header(" :violet[ Welcome to the dashboard]", divider='rainbow')


# constructing streamlit UI
tab1, tab2, tab3, tab4 = st.tabs(["$$Home$$","$Top$ $Charts$", "$$Explore Data$$", "$$About$$"])

# Setting up Home Tab
with tab1:
    st.image("phonepe.png")
    st.markdown("##  :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    st.markdown("####  :violet[Domain :] Fintech")
    st.markdown("####  :violet[Technologies Used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly")
    st.markdown("####  :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")

# Setting up Top Charts Tab
with tab2:
    st.markdown("# :violet[Top Charts]")
    column1, column2 = st.columns(2, gap="medium")
    with column1:
        Type = st.selectbox(":blue[Type]", ("Transactions", "Users"))
        Year = st.selectbox(":blue[Year]", ("2018", "2019", "2020", "2021", "2022", "2023"))
        Quarter = st.selectbox(":blue[Quarter]", ("1", "2", "3", "4"))
    with column2:
        st.info(
        """
        #### From this menu we can get insights like :
        - Overall ranking on a particular Year and Quarter.
        - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
        - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
        - Top 10 mobile brands and its percentage based on the how many people use phonepe.
        """)

    # Top Charts - Visualization of Transaction Data
    if Type  == "Transactions":
        col1, col2, col3 = st.columns([1, 1, 1], gap="small")

        with col1:
            st.markdown("### :blue[State]")
            mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(),columns=['State','Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                         names='State',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### :blue[District]")
            mycursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                         names='District',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)


        with col3:
            st.markdown("### :blue[Pincode]")
            mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    # Visualization of Users Data
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        with col1:
            st.markdown("### :blue[Brand]")
            mycursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users', 'Avg_Percentage'])
            fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)


        with col2:
            st.markdown("### :blue[State]")
            mycursor.execute(f"select state, sum(registeredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                     names='State',
                     title='Top 10',
                     color_discrete_sequence=px.colors.sequential.Agsunset,
                     hover_data=['Total_Appopens'],
                     labels={'Total_Appopens': 'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.markdown("### :blue[District]")
            mycursor.execute(f"select district, sum(registeredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users', 'Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)


        with col4:
            st.markdown("### :blue[Pincode]")
            mycursor.execute(
                f"select Pincode, sum(registeredUsers) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

# Configuring Explore Data Tab:
with tab3:
    col1,col2,col3 = st.columns([1,1,1],gap="small")
    with col1:
        Type = st.selectbox(":blue[Type]",("Transactions","Users"),key="My_selection1")
    with col2:
        Year = st.selectbox(":blue[Year]",("2018","2019","2020","2021","2022","2023"),key="My_selection2")
    with col3:
        Quarter = st.selectbox(":blue[Quarter]",("1","2","3","4"),key="My_selection3")

    # Visualization of Transaction Data on India Map
    if Type == "Transactions":
        col1,col2 = st.columns(2)
        with col1:
            st.markdown("## :blue[Overall State Wise Transactions Amount]")
            mycursor.execute(f"select State, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.State = df2
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_amount',
                                color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)


        with col2:
            st.markdown("## :blue[Overall State Wise Transactions Count]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_Transactions',
                                color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)


        # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :blue[Top Payment Type]")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions', 'Total_amount'])
        fig = px.bar(df,  title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

        # BAR CHART - District Wise Transaction Data
        st.markdown("# ")
        st.markdown("## :blue[Select any State to explore more]")
        selected_state = st.selectbox("",
                                      ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam',
                                       'bihar',
                                       'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi',
                                       'goa', 'gujarat', 'haryana',
                                       'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala',
                                       'ladakh', 'lakshadweep',
                                       'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                       'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                       'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
                                       'west-bengal'), index=30)

        mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")

        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'District', 'Year', 'Quarter',
                                                         'Total_Transactions', 'Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

    # Visualization of Users Data on India Map
    if Type == "Users":
        # Overall State Wise TOTAL APPOPENS - INDIA MAP
        st.markdown("## :blue[State Wise User App opening frequency]")
        mycursor.execute(f"select state, sum(registeredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
        df2 = pd.read_csv('Statenames.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2
        fig = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_Appopens',
                            color_continuous_scale='sunset')
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # BAR CHART TOTAL UERS - DISTRICT WISE DATA
        st.markdown("## :blue[Select any State to explore more]")
        selected_state = st.selectbox("",
                                      ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam',
                                       'bihar',
                                       'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi',
                                       'goa', 'gujarat', 'haryana',
                                       'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala',
                                       'ladakh', 'lakshadweep',
                                       'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                       'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                       'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
                                       'west-bengal'), index=30)

        mycursor.execute(f"select State,year,quarter,District,sum(registeredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")

        df = pd.DataFrame(mycursor.fetchall(),columns=['State', 'year', 'quarter', 'District', 'Total_Users', 'Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)

        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)


# Configuring the About Tab
with tab4:
    st.markdown("### :blue[About PhonePe Pulse:] ")
    st.write(
        "##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")

    st.write(
        "##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")

    st.markdown("### :blue[About PhonePe:] ")
    st.write(
        "##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
