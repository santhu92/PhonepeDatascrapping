import streamlit as st
import pandas as pd
import os
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point

sns.set_style('whitegrid')

st.sidebar.write("Please select the below options to get more detailed insits in the data")

Option = st.sidebar.selectbox('Search the category of Phoe Pe data to be visualised',('aggregated_transaction', 'aggregated_user', 'map_transaction', 'map_user', 'top_transaction', 'top_user'))

Year = st.sidebar.selectbox('Select the year',('2018', '2019', "2020",'2021','2022'))
Quater = st.sidebar.selectbox('Select the Quater of the selected year',('1', '2', '3','4'))

st.sidebar.write("Note: pages with tabs has more visualisation for the selected category")

from sqlalchemy import create_engine

# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="root123",
                               db="phonepe"))


input = str('select * from ' +Option+' where Year = ' +Year+ ' and ' 'Quater = '+Quater)
input1 = str('select * from ' +Option)

SQL_Query = pd.read_sql_query(input, engine)
SQL_Query2 = pd.read_sql_query(input1, engine)
st.header('Phone Pe Data visualisation with the past 5 year Data shared by Phone Pe')

st.write(SQL_Query)
path=r"C:\Users\kisho\Downloads\pulse-master\pulse-master2\pulse-master\data\aggregated\transaction\country\india\state\\"
Agg_state_list=os.listdir(path)
district_ltlo = pd.read_csv(r'C:\Users\kisho\Downloads\PhonePe-Pulse-Data-2018-2022-Analysis-main\PhonePe-Pulse-Data-2018-2022-Analysis-main\data\Data_Map_Districts_Longitude_Latitude.csv')
district_ltlo['District']=district_ltlo['District'].str.replace('district', '')
district_ltlo['District']=district_ltlo['District'].str.strip()


df_state_Agg_userlist = Agg_state_list


state_ltlo = pd.read_csv(r'C:\Users\kisho\Downloads\PhonePe-Pulse-Data-2018-2022-Analysis-main\PhonePe-Pulse-Data-2018-2022-Analysis-main\data\Longitude_Latitude_State_Table.csv')
state_ltlolist=state_ltlo['state'].tolist()
state_ltlolist.sort()
state_ltlo['state'] =state_ltlo['state'].replace(state_ltlolist, df_state_Agg_userlist)


from streamlit.components.v1 import html


if Option == 'aggregated_transaction' :
    tab1, tab2, tab3 = st.tabs(["📈 Map", "🗃 Bar Graph", "Complete data"])
    with tab1:
        Brand = st.selectbox('Select Mode of transaction', ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services', 'Others'))
        st.write('Number of  transaction happened in state wise for the year selected ')
        merged_df_Agg_tran = SQL_Query
        merged_df_Agg_tran = merged_df_Agg_tran.drop(['name'], axis=1)
        merged_df_Agg_tran = merged_df_Agg_tran.groupby(['State']).agg({'count': 'sum', 'amount': 'sum'})
        merged_df_Agg_tran['State'] = merged_df_Agg_tran.index
        merged_df_Agg_tran = merged_df_Agg_tran.reset_index(drop=True)
        merged_df_Agg_tran = merged_df_Agg_tran.set_index('State').join(state_ltlo.set_index('state'))
        merged_df_Agg_tran = merged_df_Agg_tran[merged_df_Agg_tran.Latitude.notna()]
        #st.write(merged_df_Agg_tran)
        #st.write('This is aggregated total values of amount of transaction happened with how many number of transaction happened in state wise ')
        merged_df_Agg_tran['State'] = merged_df_Agg_tran.index
        geometry = [Point(xy) for xy in zip(merged_df_Agg_tran.Longitude, merged_df_Agg_tran.Latitude)]
        merged_df_Agg_tran = merged_df_Agg_tran.reset_index(drop=True)
        merged_df_Agg_tran = merged_df_Agg_tran.drop(['Latitude', 'Longitude'], axis=1)
        gdf_df_Agg_tran = gpd.GeoDataFrame(merged_df_Agg_tran, crs="EPSG:4326", geometry=geometry)
        fig = gdf_df_Agg_tran.explore(column='count', cmap='Set2', legend=True, tooltip=['count', 'State'])
        html_map = fig._repr_html_()
        st.components.v1.html(html_map, width=700, height=500, scrolling=True)

        st.write('For the particula Transaction type how many Number of transaction happened in state wise for the year selected ')
        #Brand = st.selectbox('Select Mode of transaction', ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services', 'Others'))
        SQL_Query1 = SQL_Query[SQL_Query['name'] == Brand]
        merged_df_Agg_tran1 = SQL_Query1.set_index('State').join(state_ltlo.set_index('state'))
        merged_df_Agg_tran1['State'] = merged_df_Agg_tran1.index
        merged_df_Agg_tran1 = merged_df_Agg_tran1[merged_df_Agg_tran1.Latitude.notna()]
        #st.write(merged_df_Agg_tran1)
        geometry1 = [Point(xy) for xy in zip(merged_df_Agg_tran1.Longitude, merged_df_Agg_tran1.Latitude)]
        merged_df_Agg_tran1 = merged_df_Agg_tran1.reset_index(drop=True)
        #merged_df_Agg_tran1 = merged_df_Agg_tran.drop(['Latitude', 'Longitude'], axis=1)
        gdf_df_Agg_tran1 = gpd.GeoDataFrame(merged_df_Agg_tran1, crs="EPSG:4326", geometry=geometry1)
        fig1 = gdf_df_Agg_tran1.explore(column='count', cmap='Set2', legend=True, tooltip=['State', 'count', 'amount'])
        html_map1 = fig1._repr_html_()
        st.components.v1.html(html_map1, width=700, height=500, scrolling=True)

    with tab2:
        st.header("Mode of transaction vs count and amount")
        figpx1 = px.bar(SQL_Query, x="name", y="count", color="name", hover_name="amount", animation_frame="Year", range_y=[0, 150000000])
        st.plotly_chart(figpx1, use_container_width=True)

        st.header("Particular Mode of transaction vs count and amount")
        figpx = px.bar(SQL_Query1, x="name", y="count", color="amount", hover_name="count", animation_frame="Year", range_y=[0, 150000000])
        st.plotly_chart(figpx, use_container_width=True)

    with tab3:
        st.header("Complete data")
        figpx2 = px.bar(SQL_Query2, x="name", y="count", color="amount", hover_name="count", animation_frame="Year", range_y=[0, 150000000])
        st.plotly_chart(figpx2, use_container_width=True)
        widgets = st.selectbox('Select option to view particular data for all the year data is available', ('Top 10 more Transaction for the particular mode', 'Top 10 Less Transaction for the particular mode', "Top 10 states of Highest Transaction happened", 'Top 10 State with less transaction happened'))
        if widgets == 'Top 10 more Transaction for the particular mode':
            top=SQL_Query2.sort_values('count', ascending=False).head(10)
            top=top[['count','name']]
            top = top.set_index('name', drop=True)
            st.write(top)

        elif widgets == 'Top 10 Less Transaction for the particular mode':
            top=SQL_Query2.sort_values('count', ascending=True).head(10)
            top=top[['count','name']]
            top = top.set_index('name', drop=True)
            st.write(top)
        elif widgets == "Top 10 states of Highest Transaction happened":
            top1=SQL_Query2.sort_values('count', ascending=False)
            top1=top1[['count','State']]
            top1 = top1.groupby(['State']).agg({'count': 'sum'})
            st.write(top1.head(10))
        else:
            top2=SQL_Query2.sort_values('count', ascending=True)
            top2=top2[['count','State']]
            top2 = top2.groupby(['State']).agg({'count': 'sum'})
            #top2 = top2.set_index('State', drop=True)
            st.dataframe(top2.head(10))
    #except BaseException as e:
        #st.write('Search data is not avaialble , Please select other options')
elif Option == 'aggregated_user':
    tab1, tab2, tab3 = st.tabs(["📈 Map", "🗃 Bar Graph", "Complete data"])
    with tab1:
        st.header('Aggregated number of users transaction with particular mobile device')
        #st.write('This is the over all cumulated data of the users state wise/ district wise,  Please hover on the map to get the counts and value')

        merged_df_Agg_tran = SQL_Query
        merged_df_Agg_tran = merged_df_Agg_tran.drop(['brand'], axis=1)
        merged_df_Agg_tran = merged_df_Agg_tran.groupby(['State']).agg({'count': 'sum', 'percentage': 'sum'})
        merged_df_Agg_tran['State'] = merged_df_Agg_tran.index
        merged_df_Agg_tran = merged_df_Agg_tran.reset_index(drop=True)
        #st.write(merged_df_Agg_tran)

        #merged_df_Agg_tran= SQL_Query
        #merged_df_Agg_tran = merged_df_Agg_tran.groupby(['State']).sum('count')
        #merged_df_Agg_tran = merged_df_Agg_tran[merged_df_Agg_tran.notna()]
        merged_df_Agg_tran = merged_df_Agg_tran.set_index('State').join(state_ltlo.set_index('state'))
        merged_df_Agg_tran['State'] = merged_df_Agg_tran.index
        merged_df_Agg_tran = merged_df_Agg_tran[merged_df_Agg_tran.Latitude.notna()]
        geometry = [Point(xy) for xy in zip(merged_df_Agg_tran.Longitude, merged_df_Agg_tran.Latitude)]
        merged_df_Agg_tran = merged_df_Agg_tran.reset_index(drop=True)
        merged_df_Agg_tran = merged_df_Agg_tran.drop(['Latitude', 'Longitude'], axis=1)
        gdf_df_Agg_tran = gpd.GeoDataFrame(merged_df_Agg_tran, crs="EPSG:4326", geometry=geometry)
        fig = gdf_df_Agg_tran.explore(column='count', cmap='Set2', legend=True, tooltip=['count', 'State'])
        html_map = fig._repr_html_()
        st.components.v1.html(html_map, width=700, height=500, scrolling=True)

        st.header('Aggregated number of users transaction with particular mobile device')
        #st.write('This is the over all cumulated data of the users with the type of mobile model used for transaction,  Please hover on the map to get the counts and value')
        Brand = st.selectbox('Select Brand to hover brand wise', ('Xiaomi', 'Samsung', 'Vivo', 'Oppo', 'OnePlus', 'Realme', 'Apple', 'Motorola', 'Lenovo', 'Huawei', 'Others'))
        SQL_Query1 = SQL_Query[SQL_Query['brand'] == Brand]
        merged_df_Agg_tran1 = SQL_Query1.set_index('State').join(state_ltlo.set_index('state'))
        #merged_df_Agg_tran['State'] = merged_df_Agg_tran.index
        merged_df_Agg_tran1 = merged_df_Agg_tran1[merged_df_Agg_tran1.Latitude.notna()]
        geometry1 = [Point(xy) for xy in zip(merged_df_Agg_tran1.Longitude, merged_df_Agg_tran1.Latitude)]
        merged_df_Agg_tran1 = merged_df_Agg_tran1.drop(['Latitude', 'Longitude'], axis=1)
        gdf_df_Agg_tran1 = gpd.GeoDataFrame(merged_df_Agg_tran1, crs="EPSG:4326", geometry=geometry1)
        fig1 = gdf_df_Agg_tran1.explore(column='brand', cmap='Set3', legend=True, tooltip=['brand', 'count', 'percentage', 'State'])
        html_map1 = fig1._repr_html_()
        st.components.v1.html(html_map1, width=700, height=500, scrolling=True)
    #except BaseException as e:
        #st.write('Search data is not avaialble , Please select other options')
    with tab2:
        st.header("Over all count of transaction happened in each state with particular Mobile device")
        figpx1 = px.bar(SQL_Query, x="brand", y="count", color="State", hover_name="percentage", animation_frame="Year", range_y=[0, 150000000])
        st.plotly_chart(figpx1, use_container_width=True)

        st.header("Mobile device used vs count of transaction in each state")
        figpx = px.bar(SQL_Query1, x="brand", y="count", color="State", hover_name="percentage", animation_frame="Year", range_y=[0, 15000000])
        st.plotly_chart(figpx, use_container_width=True)

    with tab3:
        st.header("Complete data")
        figpx2 = px.bar(SQL_Query2, x="brand", y="count", color="State", hover_name="percentage", animation_frame="Year", range_y=[0, 150000000])
        st.plotly_chart(figpx2, use_container_width=True)
        widgets = st.selectbox('Select option to view particular data for all the year data is available', ('Top 10 number of transaction using particular Mobile model', 'Top 10 Less Transaction for the particular Mobile mode', "Top 3 brands with high transaction happened", 'Top 3 brand with less transaction happened'))
        if widgets == 'Top 10 number of transaction using particular Mobile model':
            top=SQL_Query2.sort_values('count', ascending=False).head(10)
            top=top[['count','brand','State']]
            top = top.groupby(['State', 'brand'])['count'].sum()
            #top = top.set_index('brand', drop=True)
            st.write(top)

        elif widgets == 'Top 10 Less Transaction for the particular Mobile mode':
            top=SQL_Query2.sort_values('count', ascending=True).head(10)
            top=top[['count','brand','State']]
            top = top.groupby(['State', 'brand'])['count'].sum()
            st.write(top)

        elif widgets == "Top 3 brands with high transaction happened":
            top1=SQL_Query2.sort_values('count', ascending=False)
            top1=top1[['count','State', 'brand']]
            top1 = top1.groupby(['brand'])['brand'].count()
            st.write(top1.head(3))

        else:
            top2=SQL_Query2.sort_values('count', ascending=True)
            top2=top2[['count','State', 'brand']]
            top2 = top2.groupby('brand')['brand'].count()
            #top2 = top2.set_index('State', drop=True)
            st.dataframe(top2.head(3))




elif Option == 'map_transaction':
    tab1, tab2 = st.tabs(["📈 Map", "Complete data"])
    with tab1:
        st.write('This is the over all cumulated data of the users state wise/ district wise,  Please hover on the map to get the counts and value')
        SQL_Query['district'] = SQL_Query['district'].str.strip()
        SQL_Query.drop(['State'], axis=1, inplace=True)
        merged_df_Agg_tran = SQL_Query.set_index('district').join(district_ltlo.set_index('District'))
        merged_df_Agg_tran['district'] = merged_df_Agg_tran.index
        merged_df_Agg_tran = merged_df_Agg_tran[merged_df_Agg_tran.Latitude.notna()]
        geometry = [Point(xy) for xy in zip(merged_df_Agg_tran.Longitude, merged_df_Agg_tran.Latitude)]
        merged_df_Agg_tran = merged_df_Agg_tran.drop(['Latitude', 'Longitude'], axis=1)
        gdf_df_Agg_tran = gpd.GeoDataFrame(merged_df_Agg_tran, crs="EPSG:4326", geometry=geometry)
        fig = gdf_df_Agg_tran.explore(column='count', cmap='Set2', legend=True, tooltip=['count', 'amount', 'district', 'State'])
        html_map1 = fig._repr_html_()
        st.components.v1.html(html_map1, width=700, height=500, scrolling=True)

    with tab2:
        widgets = st.selectbox('Select option to view particular data for all the year data is available', ('Top 5 more transaction happened district', 'Top 5 less transaction happened district'))

        if widgets == 'Top 5 more transaction happened district':
            top=SQL_Query2
            top=top[['count','district','amount']]
            top = top.groupby('district').agg({'count': 'sum', 'amount': 'sum'})
            #top = top.groupby(['State', 'brand'])['count'].sum()
            #top = top.set_index('brand', drop=True)
            top=top.sort_values('count', ascending=False)
            st.write(top.head(5))

        else:
            top=SQL_Query2
            top=top[['count','amount','district']]
            #top = top.groupby(['district'])['count'].sum()
            top = top.groupby('district').agg({'count': 'sum', 'amount': 'sum'})
            top=top.sort_values('count', ascending=True)
            st.write(top.head(5))

elif Option == 'map_user':
    tab1, tab2 = st.tabs(["📈 Map", "Complete data"])
    with tab1:
        SQL_Query['district'] = SQL_Query['district'].str.strip()
        SQL_Query.drop(['State'], axis=1, inplace=True)
        merged_df_Agg_tran = SQL_Query.set_index('district').join(district_ltlo.set_index('District'))
        merged_df_Agg_tran['district'] = merged_df_Agg_tran.index
        merged_df_Agg_tran = merged_df_Agg_tran[merged_df_Agg_tran.Latitude.notna()]
        geometry = [Point(xy) for xy in zip(merged_df_Agg_tran.Longitude, merged_df_Agg_tran.Latitude)]
        merged_df_Agg_tran = merged_df_Agg_tran.drop(['Latitude', 'Longitude'], axis=1)
        gdf_df_Agg_tran = gpd.GeoDataFrame(merged_df_Agg_tran, crs="EPSG:4326", geometry=geometry)
        fig = gdf_df_Agg_tran.explore(column='registeredUsers', cmap='Set2', legend=True, tooltip=['registeredUsers', 'appOpens', 'State'])
        html_map1 = fig._repr_html_()
        st.components.v1.html(html_map1, width=700, height=500, scrolling=True)


    with tab2:
        widgets = st.selectbox('Select option to view particular data for all the year data is available', ('Top 5 district with more registered users', 'Top 5 district with less registered users'))

        if widgets == 'Top 5 district with more registered users':
            top=SQL_Query2
            top=top[['registeredUsers','district','appOpens']]
            top = top.groupby('district').agg({'registeredUsers': 'sum', 'appOpens': 'sum'})
            #top = top.groupby(['State', 'brand'])['count'].sum()
            #top = top.set_index('brand', drop=True)
            top=top.sort_values('registeredUsers', ascending=False)
            st.write(top.head(5))

        else:
            top=SQL_Query2
            top=top[['registeredUsers','district','appOpens']]
            #top = top.groupby(['district'])['count'].sum()
            top = top.groupby('district').agg({'registeredUsers': 'sum', 'appOpens': 'sum'})
            top=top.sort_values('registeredUsers', ascending=True)
            st.write(top.head(5))

elif Option == 'top_transaction':
    SQL_Query['district'] = SQL_Query['district'].str.strip()
    SQL_Query.drop(['State'], axis=1, inplace=True)
    merged_df_Agg_tran = SQL_Query.set_index('district').join(district_ltlo.set_index('District'))
    merged_df_Agg_tran['District'] = merged_df_Agg_tran.index
    merged_df_Agg_tran = merged_df_Agg_tran[merged_df_Agg_tran.Latitude.notna()]
    geometry = [Point(xy) for xy in zip(merged_df_Agg_tran.Longitude, merged_df_Agg_tran.Latitude)]
    merged_df_Agg_tran = merged_df_Agg_tran.drop(['Latitude', 'Longitude'], axis=1)
    gdf_df_Agg_tran = gpd.GeoDataFrame(merged_df_Agg_tran, crs="EPSG:4326", geometry=geometry)
    fig = gdf_df_Agg_tran.explore(column='Transacion_count', cmap='Set2', legend=True, tooltip=['Transacion_count', 'Transacion_amount', 'District', 'State'])
    html_map1 = fig._repr_html_()
    st.components.v1.html(html_map1, width=700, height=500, scrolling=True)
elif Option == 'top_user':
    SQL_Query['district'] = SQL_Query['district'].str.strip()
    SQL_Query.drop(['State'], axis=1, inplace=True)
    merged_df_Agg_tran = SQL_Query.set_index('district').join(district_ltlo.set_index('District'))
    merged_df_Agg_tran['District'] = merged_df_Agg_tran.index
    merged_df_Agg_tran = merged_df_Agg_tran[merged_df_Agg_tran.Latitude.notna()]
    geometry = [Point(xy) for xy in zip(merged_df_Agg_tran.Longitude, merged_df_Agg_tran.Latitude)]
    merged_df_Agg_tran = merged_df_Agg_tran.drop(['Latitude', 'Longitude'], axis=1)
    gdf_df_Agg_tran = gpd.GeoDataFrame(merged_df_Agg_tran, crs="EPSG:4326", geometry=geometry)
    fig = gdf_df_Agg_tran.explore(column='registeredUsers', cmap='Set2', legend=True, tooltip=['registeredUsers', 'District', 'State'])
    html_map1 = fig._repr_html_()
    st.components.v1.html(html_map1, width=700, height=500, scrolling=True)