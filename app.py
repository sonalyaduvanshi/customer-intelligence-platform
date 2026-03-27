import streamlit as st
import pandas as pd
import joblib


st.set_page_config(
    page_title="Customer Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>


.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}


.hero {
    padding: 40px;
    border-radius: 20px;
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                url('https://images.unsplash.com/photo-1551288049-bebda4e38f71');
    background-size: cover;
    background-position: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.7);
    text-align: center;
    color: white;
    margin-bottom: 25px;
    transition: 0.3s;
}

.hero:hover {
    transform: scale(1.02);
}

.hero h1 {
    font-size: 42px;
    font-weight: bold;
}

.hero p {
    font-size: 18px;
    opacity: 0.9;
}

.name-tag {
    margin-top: 10px;
    font-size: 16px;
    color: #00e6e6;
}


.block-container {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}

.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    border: none;
}


h2, h3 {
    color: #00e6e6;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero">
    <h1>Customer Intelligence Platform</h1>
    <p>Predict Customer Churn using AI & Data Analytics</p>
    <div class="name-tag"> Developed by <b>Sonal Yaduvanshi</b></div>
</div>
""", unsafe_allow_html=True)

with st.spinner("Loading AI Model..."):
    model = joblib.load("churn_model.pkl")
    columns = joblib.load("columns.pkl")
    df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

st.success("App Loaded Successfully!")


st.sidebar.markdown("## Navigation")
option = st.sidebar.radio("", ["Dashboard", "Data", "Prediction"])

if option == "Dashboard":
    st.header("Business Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", len(df))
    col2.metric("Churned Customers", df[df['Churn']=='Yes'].shape[0])
    col3.metric("Churn Rate", str(round(df[df['Churn']=='Yes'].shape[0]/len(df)*100,2)) + "%")

    st.markdown("---")

    st.subheader("Churn Distribution")
    st.bar_chart(df['Churn'].value_counts())

    st.subheader(" Churn by Contract Type")
    contract = df.groupby('Contract')['Churn'].value_counts().unstack()
    st.bar_chart(contract)

    st.subheader("Monthly Charges Trend")
    st.line_chart(df['MonthlyCharges'])

    st.markdown("---")

    st.subheader("Key Insights")
    st.info("""
    • Month-to-month customers churn more  
    • Higher monthly charges increase churn risk  
    • Fiber optic users show higher churn  
    """)

elif option == "Data":
    st.header(" Dataset Preview")

    st.write("Shape:", df.shape)
    st.dataframe(df.head(50))

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Dataset",
        data=csv,
        file_name="customer_data.csv",
        mime='text/csv'
    )


elif option == "Prediction":
    st.header("Customer Churn Prediction")

    st.info("Enter customer details")

    col1, col2 = st.columns(2)

    with col1:
        tenure = st.slider("Tenure (Months)", 0, 72)

    with col2:
        monthly = st.number_input("Monthly Charges", 0)

    if st.button(" Predict"):
        input_df = pd.DataFrame({
            "tenure": [tenure],
            "MonthlyCharges": [monthly]
        })

        input_df = pd.get_dummies(input_df)
        input_df = input_df.reindex(columns=columns, fill_value=0)

        pred = model.predict(input_df)

        if pred[0] == 1:
            st.error("High Risk: Customer will churn")
        else:
            st.success(" Safe: Customer will stay")

        st.markdown("###  Model Accuracy")
        st.write("~85%")


st.markdown("---")

st.markdown("""
 **Developed by Sonal Yaduvanshi**  
 B.Tech CSE, PSIT Kanpur  

 sonalyaduvanshi.2k25@gmail.com  
 https://github.com/sonalyaduvanshi  
https://www.linkedin.com/in/sonal2311
""")
