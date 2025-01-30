import streamlit as st
import pandas as pd
import numpy as np
import pickle
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import xgboost
from xgboost import XGBRegressor


from streamlit_scroll_to_top import scroll_to_here


def predict_points(input_data):
    new_df = pd.DataFrame([input_data])

    regressor = pickle.load(open("trained_model.pkl", "rb"))
    cv = pickle.load(open("vectorizer.pkl", "rb"))
    ct = pickle.load(open("transformer.pkl", "rb"))

    corpus2 = []
    description2 = re.sub('[^a-zA-Z]', ' ', new_df['description'][0])
    description2 = description2.lower().split()
    ps = PorterStemmer()
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')
    description2 = [ps.stem(word) for word in description2 if word not in set(all_stopwords)]
    description2 = ' '.join(description2)
    corpus2.append(description2)

    words_array2 = cv.transform(corpus2).toarray()
    words_df2 = pd.DataFrame(words_array2)

    X2 = pd.concat([words_df2.reset_index(drop=True), new_df.reset_index(drop=True)], axis=1)
    X_new2 = X2.drop(["description", "designation", "title", "winery"], axis=1)
    X_new2 = X_new2.fillna(0)

    X_new2.columns = pd.DataFrame(X_new2).columns.astype(str)
    X_new2_transformed = np.array(ct.transform(X_new2))

    predicted_score = regressor.predict(X_new2_transformed)

    return predicted_score[0]


if 'scroll_to_top' not in st.session_state:
    st.session_state.scroll_to_top = False

if st.session_state.scroll_to_top:
    scroll_to_here(0, key='top')
    st.session_state.scroll_to_top = False

def scroll_to_top():
    st.session_state.scroll_to_top = True


df = pd.read_csv("dataset/winemag-data-130k-v2.csv")

st.title("Wine Review Prediction")

wine_points_placeholder = st.empty()

country_options = list(df['country'].dropna().unique())
country_options.sort()

country_input = st.selectbox("The country that the wine is from", (country_options))

desc_input = st.text_area(label='Description', placeholder='Wine description')

desig_input = st.text_input(label='Designation', placeholder='The vineyard within the winery where the grapes that made the wine are from')

price_input = st.number_input(label='Price', step=1., format='%.2f', placeholder='The cost for a bottle of the wine')

province_input = st.text_input(label='Province', placeholder='The province or state that the wine is from')

taster_input = st.text_input(label='Taster name')

title_input = st.text_input(label='Title', placeholder='The title of the wine review, which often contains the vintage')

variety_input = st.text_input(label='Variety', placeholder='The type of grapes used to make the wine (ie Pinot Noir)')

winery_input = st.text_input(label='Winery', placeholder='The winery that made the wine')


if st.button("Submit", on_click=scroll_to_top):

    errors = []

    if not country_input:
        errors.append("Country is required.")
    if not desc_input:
        errors.append("Description is required.")
    if not desig_input:
        errors.append("Designation is required.")
    if price_input <= 0:
        errors.append("Price must be greater than 0.")
    if not province_input:
        errors.append("Province is required.")
    if not taster_input:
        errors.append("Taster is required.")
    if not title_input:
        errors.append("Title is required.")
    if not variety_input:
        errors.append("Variety is required.")
    if not winery_input:
        errors.append("Winery is required.")

    if errors:
        wine_points_placeholder.error("\n".join(errors))
    else:

        input_data = {
            'country': country_input,
            'description': desc_input,
            'designation': desig_input,
            'price': price_input,
            'province': province_input,
            'taster_name': taster_input,
            'title': title_input,
            'variety': variety_input,
            'winery': winery_input,
        }

        predicted_points = predict_points(input_data)

        wine_points_placeholder.markdown(f"# Wine points is: **{predicted_points:.1f}**")