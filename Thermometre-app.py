import streamlit as st
import pandas as pd
import base64
import pickle
import xgboost
import datetime

sex_mapping = {'male': 0, 'female': 1}
outputs = []

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




st.write("""
# Clinicog Questionnaire
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

def save_and_download_csv(df):
    csv_string = df.to_csv(index=False,sep=';')
    b64 = base64.b64encode(csv_string.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="features.csv">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)

def get_prob(features):
    params_filename = './traq_class.pkl'
    with open(params_filename, 'rb') as f:
        bst = pickle.load(f)
    y_pred_proba = bst.predict_proba(features)
    return y_pred_proba

def plot(prob):
    comp_x = ["TDAH"]
    comp_y1 = [prob[0,0]]
    comp_y2 = [prob[0,1]]
    


def user_input_features():
        current_date = datetime.date.today()
        surname = st.sidebar.text_input("Nom")
        name = st.sidebar.text_input("Prénom")
        date = st.sidebar.date_input("Date de naissance")
        age = current_date.year - date.year - ((current_date.month, current_date.day) < (date.month, date.day))
        sex = st.sidebar.selectbox('Sex',('male','female'))
        sex_encoded = sex_mapping[sex]
        study = st.sidebar.selectbox("Niveau d'etude",('CAP/BEP','Baccalauréat professionnel','Baccalauréat général', 'Bac +2 (DUT/BTS)', 'Bac +3 (Licence)',
                                                       'Bac +5 (Master)', 'Bac +7 (Doctorat, écoles supérieurs)'))
        questionnaire = st.sidebar.selectbox('Questionnaire',('TRAQ','FAST','TRAQ+FAST'))
        for i, question in enumerate(Comp, start=1):
            slider_output = st.select_slider(
            f"{question}",
            options=slider_values,
            value=1,
            format_func=stringify
            )
            outputs.append(slider_output)


        data = {"surname": [surname],
                'name': [name],
                'age': [age],
                'sex': [sex_encoded],
                'study': [study],
                'test': [questionnaire],
                'answers': [outputs]}
        features = [sex_encoded,age,outputs]
        df = pd.DataFrame(data)
        return features, df



features, df = user_input_features()
save_and_download_csv(df)

# for centering the page
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("clinicogImg.png", width=200)


     

