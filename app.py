import streamlit as st
import pandas as pd
import random

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
            "Niveau (Nombre de Syllabes)": num_syllables
        })

    return pd.DataFrame(processed_data)

# Add logo
logo_path = 'images/logo1.png'
st.image(logo_path, width=200)

st.title('Analyse des mots français avec suppression de lettres basée sur le nombre de syllabes')

file_path = './liste_francais.txt'

df_results = load_and_process_words(file_path)

level_to_view = st.selectbox('Sélectionnez le niveau (basé sur le nombre de syllabes) à afficher :', options=range(1, df_results["Niveau (Nombre de Syllabes)"].max() + 1), index=0)

df_filtered = df_results[df_results["Niveau (Nombre de Syllabes)"] == level_to_view]

st.dataframe(df_filtered[['Mot avec lettres supprimées', 'Réponse (le mot corrigé pour le clinicien)', 'Nombre de Lettres', 'Niveau (Nombre de Syllabes)']])

csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    "Télécharger les données filtrées en CSV",
    csv,
    "mots_modifies_niveau.csv",
    "text/csv"
)
