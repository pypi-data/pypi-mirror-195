import imp
import streamlit as st
import pandas as pd 
from src.gpt import Gpt



# Load some stuff up
#### 
gpt = Gpt()



# File preference 
#######################################################
st.set_page_config(layout='wide', 
                   page_title='ChatPyGPT',
                   page_icon='🤖')
for x in range(20): 
    st.write(' ')
    
    
st.title('ChatPyGPT')



col1, col2, col3, col4 = st.columns(4)
with col1: 
# Add input box for user input
    user_input = st.text_input("Talk to chat")

    res = gpt.request(user_input).json()['choices'][0]['message']['content']
    st.write(res)