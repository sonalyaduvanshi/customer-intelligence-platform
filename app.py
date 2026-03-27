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
    .main {
        background-color: #0e1117;
        color: white;
    }

    .hero {
        padding: 30px;
        border-radius: 20px;
        background: linear-gradient(135deg, #00ADB5, #393E46);
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        text-align: center;
        color: white;
        margin-bottom: 20px;
        transition: 0.3s;
    }

    .hero:hover {
        transform: scale(1.02);
    }

    .hero h1 {
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 18px;
        opacity: 0.9;
    }

    .name-tag {
        margin-top: 10px;
        font-size: 16px;
        color: #eeeeee;
    }

    h2, h3 {
        color: #00ADB5;
    }

    .stButton>button {
        background-color: #00ADB5;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero">
    <h1> Customer Intelligence Platform</h1>
    <p>Predict Customer Churn using Machine Learning & Data Analytics</p>
    <div class="name-tag"> Developed by <b>Sonal Yaduvanshi</b></div>
</div>
""", unsafe_allow_html=True)


with st.spinner(" Loading AI Model..."):
    model = joblib.load("churn_model.pkl")
    columns = joblib.load("columns.pkl")
    df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

st.success(" App Loaded Successfully!")


st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to", ["Dashboard", "Data", "Prediction"])

if option == "Dashboard":
    st.header(" Business Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", len(df))
    col2.metric("Churned Customers", df[df['Churn']=='Yes'].shape[0])
    col3.metric("Churn Rate", str(round(df[df['Churn']=='Yes'].shape[0]/len(df)*100,2)) + "%")

    st.markdown("---")

    st.subheader("Churn Distribution")
    st.bar_chart(df['Churn'].value_counts())

    st.subheader("Churn by Contract Type")
    contract = df.groupby('Contract')['Churn'].value_counts().unstack()
    st.bar_chart(contract)

    st.subheader("Monthly Charges Distribution")
    st.line_chart(df['MonthlyCharges'])

    st.markdown("---")

    st.subheader("Key Insights")
    st.info("""
    • Month-to-month customers churn more  
    • Higher monthly charges increase churn risk  
    • Fiber optic users show higher churn  
    """)

elif option == "Data":
    st.header("Dataset Preview")

    st.write("Shape of Dataset:", df.shape)
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

    st.info(" Fill details below to predict customer churn")

    col1, col2 = st.columns(2)

    with col1:
        tenure = st.slider("Tenure (Months)", 0, 72)

    with col2:
        monthly = st.number_input("Monthly Charges", 0)

    if st.button("Predict Churn"):
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
            st.success("Safe: Customer will stay")

        st.markdown("### Model Performance")
        st.write("Accuracy: ~85%")


st.markdown("---")

st.markdown("""
**Developed by Sonal Yaduvanshi**  
B.Tech CSE, PSIT Kanpur  

Email: sonalyaduvanshi.2k25@gmail.com  
GitHub: https://github.com/sonalyaduvanshi  
LinkedIn: https://www.linkedin.com/in/sonal2311
""")
