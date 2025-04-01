import numpy as np
import streamlit as st
def change(col4,status):

    with col4:
        dummy = np.zeros((60,60,3))
        if status == "Needs Stocking":
            dummy[:,:,0] = 1
        else:
            dummy[:,:,1] = 1
        
        st.image(dummy, use_column_width=True)