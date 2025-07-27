import pandas as pd
import numpy as np
import joblib
import pickle
import streamlit as st

#load the model
model=joblib.load("pollution_model.pkl")
model_cols=joblib.load("model_columns.pkl")

#lets create an user interface
st.title("water pollutants predictor")
st.write("predict the water pollutants based on year and station id")

#user inputs
year_input=st.number_input("Enter year",min_value=2000,max_value=2100,value=2022)
station_id=st.text_input("Enter stationId",value='1')


#to encode and then predict
if st.button('predict'):
    if not station_id:
        st.warning('please enter stationId')
    else:
        input_df=pd.DataFrame({'year':[year_input],'id':[station_id]})
        input_encoded=pd.get_dummies(input_df,columns=['id'])

        #align with modelcols
        for col in model_cols:
            if col not in input_encoded.columns:
                input_encoded[col]=0
        input_encoded=input_encoded[model_cols]
  
          #PREDICT    
        predicted_pollutants=model.predict(input_encoded)[0]
        pollutants=['O2','NO2','NO3','SO4','PO4','CL']
        st.subheader(f"predicted pollutants level for station '{station_id}' in {year_input}:")
        predicted_values={}
        for p,val in zip(pollutants,predicted_pollutants):
             st.write(f'{p}:{val:.2f}')  