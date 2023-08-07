import streamlit as st
import os
import glob
import pandas as pd
import re 


st.title("Product Recommendations")

# find the latest file of the recommendation time
def get_latest_file(subdir, rec_type='cross-sell'):
    all_paths = glob.glob(subdir+'*')
    shortlist = [i for i in all_paths if re.search(rec_type, i)]
    path = max(shortlist, key=os.path.getctime)
    return path

# load the data
@st.cache_data
def load_recommendations(rec_type='cross-sell', data_path='/../data/'):

    if(rec_type in ["cross-sell", "up-sell"]):
    # get the latest file
        df = pd.read_csv( get_latest_file(subdir=os.getcwd()+data_path, rec_type=rec_type) )

        df = df[["product_name", "recommendations"]]
        df["recommendations"] = df["recommendations"].apply(lambda x: [re.split("[{]", i)[-1] for i in re.split("[=]", x)])
        return df

# df filtering function
def filter_dataframe(df):
    modify = st.checkbox("Add filters")
    
    left, right = st.columns((1, 20))

    if not modify:
        return df

    search_string = right.text_input(
        f"Substring or regex in product_variant_id"
    )
    if search_string:
        df = df[df["product_name"].str.contains(search_string)]
    
    return df

rec_type = st.selectbox(label="Recommendation Type",
                        options=["cross-sell", "up-sell"])

recommendations = load_recommendations(rec_type=rec_type)

# load the recommendations as a dataframe
st.dataframe(filter_dataframe(recommendations))
