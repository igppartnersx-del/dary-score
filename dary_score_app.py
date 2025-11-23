import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURATION DE BASE ---
st.set_page_config(page_title="DARY Score App", page_icon="💎", layout="wide")

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_cahier_des_charges():
    try:
        return pd.read_csv("DARY_Scoring_Cahier_des_Charges.csv")
    except Exception as e:
        st.warning("Impossible de charger le cahier des charges : " + str(e))
        return None

def calculate_score(input_data, cahier):
    # Vérifie que les colonnes existent
    if cahier is None or input_data is None:
        return None, "Erreur de chargement des données."

    # On applique les pondérations proportionnellement
    total_weight = cahier["Pondération (%)"].sum()
    weighted_sum = 0
    for i, row in cahier.iterrows():
        critere = row["Critère"]
        poids = row["Pondération (%)"] / total_weight
        valeur = input_data.get(critere, np.nan)
        if pd.notnull(valeur):
            weighted_sum += valeur * poids
    score_final = round(weighted_sum, 2)
    return score_final, "Calcul terminé avec succès."

# --- INTERFACE UTILISATEUR ---
st.title("💎 Simulateur DARY Score")
st.markdown("Une solution complète pour évaluer vos projets immobiliers selon des critères de confiance, transparence et performance.")

cahier = load_cahier_des_charges()
if cahier is None:
    st.stop()

with st.sidebar:
    st.header("Saisie des critères")
    st.caption("Entrez vos valeurs sur une échelle de 0 à 10")
    user_inputs = {}
    for critere in cahier["Critère"]:
        user_inputs[critere] = st.slider(critere, 0.0, 10.0, 5.0, 0.1)

# --- CALCUL ---
if st.button("Calculer le Score DARY"):
    score, msg = calculate_score(user_inputs, cahier)
    st.session_state["score"] = score
    st.session_state["msg"] = msg

# --- AFFICHAGE DES RÉSULTATS ---
if "score" in st.session_state:
    with st.container():
        st.subheader("Résultat du Score DARY")
        st.metric(label="Score Global DARY", value=f"{st.session_state['score']}/10")
        if st.session_state['score'] >= 8:
            st.success("Excellent investissement : promoteur fiable et projet solide.")
        elif st.session_state['score'] >= 6:
            st.info("Bon projet : certaines améliorations possibles.")
        else:
            st.warning("Projet à risque : vérifications complémentaires recommandées.")
        st.caption(st.session_state['msg'])

st.divider()

# --- AFFICHAGE DU CAHIER DES CHARGES ---
with st.expander("Voir le détail du cahier des charges"):
    st.dataframe(cahier, use_container_width=True)

st.caption("Application DARY © 2025 - Version stable corrigée pour Streamlit Cloud")
