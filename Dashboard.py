
import streamlit as st 
import pandas as pd
import numpy as np 
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

st.title("Sales Streamlit Dashboard")
st.markdown("Created by Lukas")
st.write("---")  
st.text("")  
st.text("")  


def load_data(path: str):
    df = pd.read_excel(path)
    return df

def transform_data(df):
    df = df.melt(id_vars=['Account', 'business_unit', 'Currency', 'Year', 'Scenario',], value_vars=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec'],var_name="Month", value_name="Sales")
    df["Monat"] = df.Month.replace({"Jan" : "01","Feb" : "02","Mar" : "03","Apr" : "04","May" : "05","Jun" : "06","Jul" : "07","Aug" : "08","Sep" : "09","Oct" : "10","Nov" : "11","Dec" : "12"})
    df["JahrMonat"] = df["Year"].astype("str") + "-" + df["Monat"]
    return df

def line_plot(df, title):
    fig = px.line(df, x="JahrMonat", y="Sales", title= "Verkaufskurve "+ str(sel_year) + " " + str(title))
    st.plotly_chart(fig)

def bar_plot(df, title, chart_key):
    fig = px.bar(df, x="JahrMonat", y="Sales", color="Scenario", title= "Forecast vs Budget 2023 " + str(title), barmode="group")
    st.plotly_chart(fig, chart_key)

df = load_data("FinancialDataClean.xlsx")
df_trans = transform_data(df)


###---------- Filter Section Start----------###

col01, col02, col03, col04 = st.columns(4)
with col01:
    year_options = df_trans.Year.unique()
    sel_year = st.selectbox("Select Year: ", options = year_options)

###---------- Filter Section End ----------###



sales_soft_22 = round(df_trans[(df_trans["business_unit"] == "Software") & (df_trans["Account"] == "Sales") & (df_trans["Year"] == sel_year)].Sales.sum() / 1000000)
sales_hard_22 = round(df_trans[(df_trans["business_unit"] == "Hardware") & (df_trans["Account"] == "Sales") & (df_trans["Year"] == sel_year)].Sales.sum() / 1000000)
sales_ads_22 = round(df_trans[(df_trans["business_unit"] == "Advertising") & (df_trans["Account"] == "Sales") & (df_trans["Year"] == sel_year)].Sales.sum() / 1000000)


col11, col12, col13 = st.columns(3)
with col11:
    st.metric(label="Software (Mio) " + str(sel_year), value=sales_soft_22)

with col12:
    st.metric(label="Hardware (Mio) " + str(sel_year), value=sales_hard_22)

with col13:
    st.metric(label="Advertising (Mio) " + str(sel_year), value=sales_ads_22)



col21, col22, col23 = st.columns(3)
with col21:
    bar_plot(df_trans[(df_trans["Year"] == 2023) & (df_trans["Account"] == "Sales") & (df_trans["business_unit"] == "Software")], "Software", chart_key = 1)

with col22:
    bar_plot(df_trans[(df_trans["Year"] == 2023) & (df_trans["Account"] == "Sales") & (df_trans["business_unit"] == "Hardware")], "Hardware", chart_key = 2)

with col23:
    bar_plot(df_trans[(df_trans["Year"] == 2023) & (df_trans["Account"] == "Sales") & (df_trans["business_unit"] == "Advertising")], "Ads", chart_key = 3)


line_plot(df_trans[(df_trans["Year"] == sel_year) & (df_trans["Account"] == "Sales") & (df_trans["business_unit"] == "Software") & (df_trans["Scenario"] == "Actuals")], "Software",)

line_plot(df_trans[(df_trans["Year"] == sel_year) & (df_trans["Account"] == "Sales") & (df_trans["business_unit"] == "Hardware") & (df_trans["Scenario"] == "Actuals")], "Hardware")

line_plot(df_trans[(df_trans["Year"] == sel_year) & (df_trans["Account"] == "Sales") & (df_trans["business_unit"] == "Advertising") & (df_trans["Scenario"] == "Actuals")], "Ads")





