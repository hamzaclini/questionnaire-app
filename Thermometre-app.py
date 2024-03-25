import streamlit as st
import pandas as pd
import base64
import datetime
import pymongo
import os
import psutil
import time
import hmac
#from bson import ObjectId

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()

sex_mapping = {'male': 0, 'female': 1}
answers = {}

Comp = [
    "Organisation du matériel (ex. matériel rangé sur la table)",
    "Concentration sur tâches exigeantes (ex. reste sur une activité sans se distraire)",
    "Application des instructions (ex. suit une directive sans rappel)",
    "Réactivité modérée aux distractions externes (ex. ignore les bruits alentours lors d'une tâche)",
    "Fluidité dans les transitions (ex. change d'activité sans délai)",
    "Capacité à rester calme (ex. reste assis pendant une histoire)",
    "Gestion des mouvements et manipulations (ex. ne met pas d'objets à la bouche)",
    "Régulation des prises de parole (ex. parle à des moments appropriés)",
    "Adaptation sociale et émotionnelle (ex. joue sans exclure les autres)",
    "Engagement dans les jeux collectifs (ex. suit les règles du jeu)"
    ]




st.markdown(
        """<style>
        div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 20px;
                }
        </style>
                """, unsafe_allow_html=True)


st.markdown(
    """
    <style>
    .centered_button {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.write("""
# Thermometre Questionnaire
""")


st.sidebar.header('Informations')

slider_values = [1,2,3,4]
slider_strings = ["Très insuffisant", "Insuffisant", "Satisfaisant", "Très satisfaisant"]

def stringify(i:int = 0) -> str:
    return slider_strings[i-1]

#T1 = st.select_slider(
#    "Je quitte souvent ma place sans nécessité lors d'une réunion.",
#    options=slider_values,
#    value=1,
#    format_func=stringify)

#def save_and_download_csv(df):
#    csv_string = df.to_csv(index=False,sep=';')
    b64 = base64.b64encode(csv_string.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="features.csv">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)

# def custom_date_input(label, min_date=None, max_date=None):
#     if min_date is None:
#         min_date = datetime.datetime(year=1900, month=1, day=1)
#     if max_date is None:
#         max_date = datetime.datetime(year=2100, month=12, day=31)
#     year = st.number_input("Year", min_value=min_date.year, max_value=max_date.year, step=1, value=min_date.year)
#     month = st.number_input("Month", min_value=1, max_value=12, step=1, value=min_date.month)
#     day = st.number_input("Day", min_value=1, max_value=31, step=1, value=min_date.day)
#     try:
#         date_input = datetime.datetime(year=year, month=month, day=day)
#         if min_date <= date_input <= max_date:
#             return date_input
#         else:
#             st.error("Please enter a date within the specified range.")
#             return None
#     except ValueError:
#         st.error("Please enter a valid date.")
#         return None

def write_data(new_data):
    # Write new data to the database
    db = client.alphapv
    db.test.insert_one(new_data)
    


def user_input_features():
        #current_date = datetime.date.today()
        surname = st.sidebar.text_input("Nom")
        name = st.sidebar.text_input("Prénom")
        date = st.sidebar.date_input("Date de naissance", datetime.date(2010, 1, 1))
        #age = current_date.year - date.year - ((current_date.month, current_date.day) < (date.month, date.day))
        sex = st.sidebar.selectbox('Sex',('Homme','Femme'))
        study = st.sidebar.selectbox("Niveau d'etude",('CAP/BEP','Baccalauréat professionnel','Baccalauréat général', 'Bac +2 (DUT/BTS)', 'Bac +3 (Licence)',
                                                       'Bac +5 (Master)', 'Bac +7 (Doctorat, écoles supérieurs)'))
        #questionnaire = st.sidebar.selectbox('Questionnaire',('TRAQ','FAST','TRAQ+FAST'))
        for i, question in enumerate(Comp, start=1):
            slider_output = st.select_slider(
            f"{question}",
            options=slider_values,
            value=1,
            format_func=stringify
            )
            answers[f"THERM{i}"] = slider_output


        user_data = {"lastName": surname,
                     'firstName': name,
                     'birthDate': date.isoformat(),
                     'sex': sex,
                     'educationalLevel': study}
        answers_data = answers

        document = {
        #"_id": ObjectId(),  # Generate a new ObjectId
        "user": user_data,
        "answers": answers_data
        #"__v": 0
        }
                
        return document



document = user_input_features()

#if st.button('Enregisterez'):
#    write_data(document)
#save_and_download_csv(df)
#st.write(document)
# for centering the page
#input_date = custom_date_input("Select a date")
#if input_date:
#    st.write("Selected date:", input_date)
     
     
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    button = st.button('Enregisterez')
    st.image("clinicogImg.png", width=200)
    
if button:
     #write_data(document)
     # Close streamlit browser tab
     # Terminate streamlit python process
     st.write("Merci d'avoir participé(e) à ce questionnaire")
     time.sleep(1)
     pid = os.getpid()
     p = psutil.Process(pid)
     p.terminate()
     


     

