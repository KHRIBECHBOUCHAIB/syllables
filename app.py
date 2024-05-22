import streamlit as st
import pandas as pd
import random
import io

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
st.sidebar.image('images/logo1.png', width=200)

st.title('Analyse des mots français avec suppression de lettres basée sur le nombre de syllabes')

file_path = './liste_francais.txt'
df_results = load_and_process_words(file_path)


# Filter by number of syllables
syllable_options = list(range(1, df_results["Niveau (Nombre de Syllabes)"].max() + 1))
level_to_view = st.sidebar.selectbox('Sélectionnez le niveau (basé sur le nombre de syllabes) à afficher :', 
                                     options=syllable_options, index=0)

# Filter by number of letters
letter_options = list(range(1, df_results["Nombre de Lettres"].max() + 1))
letters_to_view = st.sidebar.selectbox('Sélectionnez le nombre de lettres à afficher :', 
                                       options=letter_options, index=0)

# Button to apply filters and load the filtered data
if st.sidebar.button("Charger la liste filtrée"):
    df_filtered = df_results[(df_results["Niveau (Nombre de Syllabes)"] == level_to_view) & 
                             (df_results["Nombre de Lettres"] == letters_to_view)]
    st.session_state.filtered_df = df_filtered.copy()

# Load filtered data from session state
if 'filtered_df' in st.session_state:
    edited_df = st.session_state.filtered_df
    st.write("### Liste filtrée des mots")

    # Use st.data_editor to make the table fully interactive and editable
    edited_df = st.data_editor(edited_df, use_container_width=True, num_rows="dynamic")
    
    st.session_state.edited_df = edited_df

    # Button to download the updated DataFrame
    chosen_words = edited_df[edited_df['Choisi par le Clinicien'] == True]

    # Save chosen words to an Excel file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        chosen_words.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()

    st.sidebar.download_button(
        label="Télécharger les mots choisis et leurs réponses en Excel",
        data=processed_data,
        file_name="mots_choisis_reponses.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
