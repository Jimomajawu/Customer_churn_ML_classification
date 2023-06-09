import streamlit as st
import pandas as pd
import pickle
import numpy as np
import sklearn
model4 = pickle.load(open('LR_model.pkl', 'rb'))
scaler = pickle.load(open('scal_class.pkl', 'rb'))
encoder = pickle.load(open('enc_class.pkl', 'rb'))

df = st.file_uploader('Upload a CSV')
#df1 = pd.read_csv(df)

                      
if df is not None:
#read CSV file into a dtaframe
   df = pd.read_csv(df)
else:
    st.stop()
                      
def prep(df):
    
    df['TotalCharges'] = df['TotalCharges'].replace(' ',np.nan)
    df['TotalCharges'] = df['TotalCharges'].astype(float)
    df.drop_duplicates(keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.dropna(inplace=True)
    df.reset_index(drop=True,inplace=True)
    cust = df['customerID']
    df.drop(['customerID'], axis=1, inplace=True)

    cat1 = ['gender','Partner','Dependents','PhoneService','MultipleLines','InternetService','OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport','StreamingTV','StreamingMovies','Contract','PaperlessBilling','PaymentMethod']
    
    
    enc_data = pd.DataFrame(encoder.transform(df[cat1]).toarray())
    enc_data.columns = encoder.get_feature_names_out()
    df = df.join(enc_data)
    df.drop(cat1,axis=1,inplace=True)
    coll = df.columns
    df = scaler.transform(df)
    df = pd.DataFrame(df,columns=coll)
    
    return cust, df

cust,c_data = prep(df)
prep = model4.predict(c_data)
results = pd.DataFrame({'Cust_ID':cust,"Churn_pred":prep})
targ_cust=results[results['Churn_pred'] =='Yes'].reset_index(drop=True)['Cust_ID']
c1,c2 = st.columns(2) 
                      
with c1:
    if st.button("Prediction"):
        st.dataframe(results)
        csv1 = results.to_csv(index=False)
        st.download_button("Download Predictions",csv1,file_name='predictions.csv')
with c2:
    if st.button('Churn Customers'):
        st.dataframe(targ_cust)
        csv2 = targ_cust.to_csv(index=False)
        st.download_button('Download Target customer list',csv2,file_name='churn_cust.csv')
