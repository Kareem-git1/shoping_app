
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout= 'wide', page_title= 'statistics')

st.image('65f840d316353_mobile.app.development.1920.1080.png')

df = pd.read_csv('sheat_cleand.csv', index_col= 0)

page = st.sidebar.radio('Pages', ['Home', "univariate", "Multivariate"])

if page == 'Home':
    st.subheader('Dataset Overview')
    st.dataframe(df)

    column_descriptions = {
    "income": "The user’s monthly or yearly income level.",
    "gender": "Indicates the user's gender (male, female, or unspecified).",
    "purchases": "The total number of purchases made by the user.",
    "score": "A numeric score representing user behavior, engagement, or loyalty.",
    "category": "The group or segment the user belongs to (e.g., Bronze, Silver, Gold).",
    "is_active": "Shows whether the user is currently active (1 = active, 0 = inactive).",
    "signup_year": "The year the user originally created their account.",
    "last_login_days": "How many days have passed since the user last logged into the system.",
    "target": "The prediction label (e.g., whether the user will buy, churn, subscribe, etc.).",
}

    desc_df = pd.DataFrame(list(column_descriptions.items()), columns=["Column Name", "Description"])

    st.subheader("📝 Column Descriptions")
    st.table(desc_df)

elif page == "univariate":

    tab_num,tab_cat=st.tabs(['numbers','catrgorical'])
    col_cat=tab_cat.selectbox('column',df.select_dtypes(include='object').columns)
    col_num=tab_num.selectbox('column',df.select_dtypes(include='number').columns)
    cat_counts = df[col_cat].value_counts().sort_values(ascending=False).reset_index()
    cat_counts.columns = [col_cat, 'count']
    tab_num.plotly_chart(px.histogram(data_frame=df,x=col_num))
    chart = tab_cat.selectbox('Chart', ['Histogram', 'Pie'])
    if chart == 'Pie':
        tab_cat.plotly_chart(px.pie(data_frame=df,names=col_cat))
    elif chart == 'Histogram':
        tab_cat.plotly_chart(px.bar(cat_counts,x=col_cat,y='count'))


elif page == 'Multivariate':

    st.header('Total Income per User Category')
    category_income = df.groupby('category')['income'].sum().round(2).reset_index()
    category_income = category_income.sort_values(by='income', ascending=False)
    st.plotly_chart(px.bar(category_income,x='category',y='income',labels={'category': 'User Category', 'income': 'Total Income'},text_auto=True,title='Total Income by User Category'))
    st.header('Gender vs Number of Purchases')
    st.plotly_chart(px.histogram(df,x='gender',y='purchases',color='gender',barmode='group',title='Total Purchases by Gender'))

    st.header('Impact of Activity Status on Average Score')
    activity_score = df.groupby('is_active')['score'].mean().round(2).reset_index()
    st.plotly_chart(px.bar(activity_score,x='is_active',y='score',text='score',title='Average Score by Active/Inactive Users'))

    st.header('Average Purchases by Signup Year Range')
    df['signup_group'] = pd.cut(df['signup_year'], bins=5)
    df['signup_group_str'] = df['signup_group'].astype(str)
    signup_purchases = df.groupby('signup_group_str')['purchases'].mean().reset_index()

    st.plotly_chart(px.bar(signup_purchases,x='signup_group_str',y='purchases',text='purchases',title='Average Purchases by Signup Year Range'))
