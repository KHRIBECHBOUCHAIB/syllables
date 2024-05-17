import streamlit as st
import pandas as pd
import random

# Helper functions
def count_syllables(word):
    vowels = "aeiouyAEIOUY"
    return sum(1 for char in word if char in vowels)

def remove_letters_based_on_syllables(word):
    num_syllables = count_syllables(word)
    letters_to_remove = min(num_syllables, len(word))

    indices_to_remove = random.sample(range(len(word)), letters_to_remove)

    modified_word_list = list(word)
    for idx in sorted(indices_to_remove, reverse=True):
        modified_word_list[idx] = '_'

    modified_word = ''.join(modified_word_list)

    return modified_word, word, len(word), num_syllables

def load_and_process_words(file_path):
    with open(file_path, 'r', encoding='latin1') as file:
        words = file.read().splitlines()

    processed_data = []
    for word in words:
        modified_word, answer, num_letters, num_syllables = remove_letters_based_on_syllables(word)
        processed_data.append({
            "Mot avec lettres supprimées": modified_word,
            "Réponse (le mot corrigé pour le clinicien)": answer,
            "Nombre de Lettres": num_letters,
            "Niveau (Nombre de Syllabes)": num_syllables,
            "Choisi par le Clinicien": False,  # Initial value for clinician's choice
            "Réponse Correcte du Patient": False,  # Initial value for patient's correct response
            "Nombre d'Essais": 0  # Initial value for number of attempts
        })

    return pd.DataFrame(processed_data)

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# Main app
logo_path = 'images/logo1.png'
st.image(logo_path, width=200)

st.title('Analyse des mots français avec suppression de lettres basée sur le nombre de syllabes')

file_path = './liste_francais.txt'
df_results = load_and_process_words(file_path)

level_to_view = st.selectbox('Sélectionnez le niveau (basé sur le nombre de syllabes) à afficher :', 
                             options=range(1, df_results["Niveau (Nombre de Syllabes)"].max() + 1), index=0)

df_filtered = df_results[df_results["Niveau (Nombre de Syllabes)"] == level_to_view]

# Ensure session state persistence for edited data
if 'edited_df' not in st.session_state:
    st.session_state.edited_df = df_filtered.copy()

edited_df = st.session_state.edited_df

# Use st.data_editor to make the table fully interactive and editable
st.data_editor(edited_df, use_container_width=True)

# Provide an option to download the updated DataFrame
csv = edited_df.to_csv(index=False).encode('utf-8')
st.download_button(
    "Télécharger les données filtrées et mises à jour en CSV",
    csv,
    "mots_modifies_niveau.csv",
    "text/csv"
)
