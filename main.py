import streamlit as st
import pandas as pd

from streamlit_scroll_to_top import scroll_to_here


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

region1_input = st.text_input(label='Region1', placeholder='The wine growing area in a province or state (ie Napa)')

region2_input = st.text_input(label='Region2', placeholder='Sometimes there are more specific regions specified within a wine growing area')

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
    if not region1_input:
        errors.append("Region1 is required.")
    if not region2_input:
        errors.append("Region2 is required.")
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
            'region_1': region1_input,
            'region_2': region2_input,
            'taster_name': taster_input,
            'title': title_input,
            'variety': variety_input,
            'winery': winery_input,
        }

        input_df = pd.DataFrame([input_data])

        predicted_points = 90 

        wine_points_placeholder.markdown(f"# Wine points is: **{predicted_points}**")