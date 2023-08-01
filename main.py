import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

st.set_page_config(page_title="Credit Risk Assessment", page_icon=":moneybag:", layout='centered', initial_sidebar_state='auto',
                       menu_items={
                                    'About': "created by Debjyotirshi Majumder"
    })

st.markdown(
    """
    <div style="
    background-color: #f0f0f0;
    border-radius: 30px;
    padding: 5px;
    position: fixed;
    right: 5px;
    bottom: 5px;
    ">

    <h5 style="
    color: #333;
    text-align: center;
    ">
    created by Debjyotirshi Majumder</h5>

    </div>
    """, 
    unsafe_allow_html=True
    )


def create_gauge_chart(risk_level, title):
    if risk_level == 'Low Risk':
        gauge_color = 'green'
    else:
        gauge_color = 'red'

    fig = go.Figure(go.Indicator(
        mode = "gauge",
        gauge = {'axis': {'range': [0, 180], 'visible': False},
                 'bar': {'color': gauge_color},
                 'steps' : [{'range': [0, 180], 'color': gauge_color}]
                },
        title = {'text': f"<b>{title}</b>", 'font': {'color': gauge_color, 'size': 35, 'family': 'Arial'}}
        ))
    
    fig.update_layout(autosize=False, width=600, height=400, margin=dict(t=50, b=50, l=50, r=50))
    return fig

def user_input_features():
    st.sidebar.markdown('## Personal Information')
    age = st.sidebar.slider('Age', 18, 100, 30)
    income = st.sidebar.number_input('Income', min_value=1000, max_value=10000000, value=50000, step=1000)
    employment_length = st.sidebar.slider('Employment Length', 0, 50, 10)

    st.sidebar.markdown('## Loan Information')
    home_ownership = st.sidebar.selectbox('Home Ownership', options=['RENT', 'MORTGAGE', 'OWN', 'OTHER'])
    loan_intent = st.sidebar.selectbox('Loan Intent', options=['PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE', 'DEBTCONSOLIDATION', 'HOMEIMPROVEMENT'])
    loan_grade = st.sidebar.selectbox('Loan Grade', options=['A', 'B', 'C', 'D', 'E', 'F', 'G'])
    loan_amount = st.sidebar.number_input('Loan Amount', min_value=500, max_value=500000, value=5000, step=500)
    loan_interest_rate = st.sidebar.number_input('Loan Interest Rate', min_value=0.0, max_value=25.0, value=5.0, step=0.1)
    loan_percent_income = loan_amount / income
    
    st.sidebar.markdown('## Credit History')
    credit_history_length = st.sidebar.slider('Credit History Length', 0, 50, 2)
    has_default_history = st.sidebar.selectbox('Has Default History', options=['Yes', 'No'])
    
    data = {
        'person_age': age,
        'person_income': income,
        'person_emp_length': employment_length,
        'loan_amnt': loan_amount,
        'loan_int_rate': loan_interest_rate,
        'loan_percent_income': loan_percent_income,
        'cb_person_cred_hist_length': credit_history_length,
        'cb_person_default_on_file': 1 if has_default_history == 'Yes' else 0,
        'person_home_ownership_MORTGAGE': 1 if home_ownership == 'MORTGAGE' else 0,
        'person_home_ownership_OWN': 1 if home_ownership == 'OWN' else 0,
        'person_home_ownership_RENT': 1 if home_ownership == 'RENT' else 0,
        'person_home_ownership_OTHER': 1 if home_ownership == 'OTHER' else 0,
        'loan_intent_EDUCATION': 1 if loan_intent == 'EDUCATION' else 0,
        'loan_intent_MEDICAL': 1 if loan_intent == 'MEDICAL' else 0,
        'loan_intent_PERSONAL': 1 if loan_intent == 'PERSONAL' else 0,
        'loan_intent_VENTURE': 1 if loan_intent == 'VENTURE' else 0,
        'loan_intent_DEBTCONSOLIDATION': 1 if loan_intent == 'DEBTCONSOLIDATION' else 0,
        'loan_intent_HOMEIMPROVEMENT': 1 if loan_intent == 'HOMEIMPROVEMENT' else 0,
        'loan_grade_A': 1 if loan_grade == 'A' else 0,
        'loan_grade_B': 1 if loan_grade == 'B' else 0,
        'loan_grade_C': 1 if loan_grade == 'C' else 0,
        'loan_grade_D': 1 if loan_grade == 'D' else 0,
        'loan_grade_E': 1 if loan_grade == 'E' else 0,
        'loan_grade_F': 1 if loan_grade == 'F' else 0,
        'loan_grade_G': 1 if loan_grade == 'G' else 0,
    }

    # The given code is written in Python and it creates a pandas DataFrame object called "features" using the pd.DataFrame() function. 
    # The DataFrame is initialized with the data provided as an argument to the function, and the index parameter is set to [0].

    # Here's a breakdown of the code:

    # 1. `features = pd.DataFrame(data, index=[0])`: This line creates a new DataFrame object named "features". 
    # The data for the DataFrame is passed as the first argument to the pd.DataFrame() function. 
    # The second argument, `index=[0]`, specifies that the DataFrame should have a single row with an index value of 0.

    # 2. `return features`: This line returns the created DataFrame object as the output of the function.

    # In summary, this code takes some data and creates a pandas DataFrame object with a single row and an index value of 0. 
    # The resulting DataFrame is then returned as the output of the function.

    features = pd.DataFrame(data, index=[0])
    return features

st.write("# Credit Risk Assessment")

st.write("Please enter your data on the left to get the credit risk prediction.")

input_df = user_input_features()

# Load column order
column_order = joblib.load(r'saved_model\column_order.pkl')

# Reorder columns in input_df according to column_order
input_df = input_df[column_order]

# Load your trained model
model = joblib.load(r'saved_model\rfc.pkl')

# Apply the model to make predictions
# Since, a binary classification task. 
# So, the `prediction` variable will hold an array with a single element 
# that is either 0 (representing "Low Risk") or 1 (representing "High Risk").
prediction = model.predict(input_df)

# Display the prediction
st.subheader('Prediction:')
if prediction[0] == 0:
    st.plotly_chart(create_gauge_chart("Low Risk", "Low Risk"))
    st.success('Congratulations! 🎉 \n\n You are predicted to have a low risk of defaulting on your loan.')
    st.balloons()
else:
    st.plotly_chart(create_gauge_chart("High Risk", "High Risk"))
    st.error('⚠️ Warning! ⚠️\n\nYou are predicted to have a high risk of defaulting on your loan.\n\nPlease proceed with caution! 🛑')