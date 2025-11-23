import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import base64
from io import BytesIO
import os

# Configuration de la page
st.set_page_config(
    page_title="DARY Score - Simulateur Immobilier Intelligent",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé avec les couleurs DARY
st.markdown("""
<style>
    /* Style global */
    .stApp {
        background: linear-gradient(135deg, #0B2239 0%, #1a3555 100%);
    }
    
    /* En-tête personnalisé */
    .main-header {
        background: #0B2239;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        text-align: center;
        border: 2px solid #3CE58E;
    }
    
    .main-title {
        color: #3CE58E;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        color: white;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Cartes de métriques */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        margin-bottom: 1rem;
        border-left: 5px solid #3CE58E;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.25);
    }
    
    .score-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.2rem;
        margin: 0.5rem;
    }
    
    .score-excellent { background: #3CE58E; color: white; }
    .score-bon { background: #4CAF50; color: white; }
    .score-moyen { background: #FFC107; color: black; }
    .score-faible { background: #FF5722; color: white; }
    
    /* Boutons personnalisés */
    .stButton > button {
        background: #3CE58E;
        color: #0B2239;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(60, 229, 142, 0.3);
    }
    
    .stButton > button:hover {
        background: #2BC97A;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(60, 229, 142, 0.4);
    }
    
    /* Sections */
    .section-header {
        color: white;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 2rem 0 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3CE58E;
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(60, 229, 142, 0.1);
        border-left: 4px solid #3CE58E;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 8px;
        color: white;
    }
    
    /* Tableaux */
    .dataframe {
        background: white !important;
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Inputs */
    .stSelectbox > div > div, 
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid #3CE58E;
        border-radius: 10px;
    }
    
    /* Labels */
    label {
        color: white !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# En-tête de l'application
st.markdown("""
<div class="main-header">
    <div class="main-title">🏢 DARY Score</div>
    <div class="subtitle">Simulateur d'Investissement Immobilier Intelligent | Maroc</div>
</div>
""", unsafe_allow_html=True)

# Initialisation de l'état de session
if 'projects' not in st.session_state:
    st.session_state.projects = []
if 'current_scores' not in st.session_state:
    st.session_state.current_scores = None

# Fonctions de calcul du score
class DARYScoring:
    """Système de scoring immobilier DARY"""
    
    @staticmethod
    def calculate_financial_score(data):
        """Calcul du score financier (40% du score total)"""
        score = 0
        details = {}
        
        # ROI projeté (30 points max)
        roi = data.get('roi_projete', 0)
        if roi >= 15:
            score += 30
            details['ROI'] = "Excellent (≥15%)"
        elif roi >= 10:
            score += 20
            details['ROI'] = f"Bon ({roi}%)"
        elif roi >= 5:
            score += 10
            details['ROI'] = f"Moyen ({roi}%)"
        else:
            score += 5
            details['ROI'] = f"Faible ({roi}%)"
        
        # Ticket d'entrée (20 points max)
        ticket = data.get('ticket_minimum', 0)
        if ticket <= 10000:
            score += 20
            details['Accessibilité'] = "Très accessible"
        elif ticket <= 50000:
            score += 15
            details['Accessibilité'] = "Accessible"
        elif ticket <= 100000:
            score += 10
            details['Accessibilité'] = "Moyen"
        else:
            score += 5
            details['Accessibilité'] = "Premium"
        
        # Rendement locatif (30 points max)
        rendement = data.get('rendement_locatif', 0)
        if rendement >= 7:
            score += 30
            details['Rendement locatif'] = f"Excellent ({rendement}%)"
        elif rendement >= 5:
            score += 20
            details['Rendement locatif'] = f"Bon ({rendement}%)"
        elif rendement >= 3:
            score += 10
            details['Rendement locatif'] = f"Moyen ({rendement}%)"
        else:
            score += 5
            details['Rendement locatif'] = f"Faible ({rendement}%)"
        
        # Plus-value potentielle (20 points max)
        plus_value = data.get('plus_value_estimee', 0)
        if plus_value >= 30:
            score += 20
            details['Plus-value'] = f"Très élevée ({plus_value}%)"
        elif plus_value >= 20:
            score += 15
            details['Plus-value'] = f"Élevée ({plus_value}%)"
        elif plus_value >= 10:
            score += 10
            details['Plus-value'] = f"Modérée ({plus_value}%)"
        else:
            score += 5
            details['Plus-value'] = f"Faible ({plus_value}%)"
        
        return min(score, 100), details
    
    @staticmethod
    def calculate_location_score(data):
        """Calcul du score de localisation (30% du score total)"""
        score = 0
        details = {}
        
        # Zone géographique
        zone = data.get('zone', 'standard')
        zones_scores = {
            'premium': 40,
            'prime': 30,
            'emergente': 20,
            'standard': 10
        }
        score += zones_scores.get(zone, 10)
        details['Zone'] = zone.capitalize()
        
        # Proximité commodités
        commodites = data.get('commodites', {})
        score_commodites = 0
        if commodites.get('ecoles', 0) <= 2:
            score_commodites += 10
        if commodites.get('commerces', 0) <= 1:
            score_commodites += 10
        if commodites.get('transport', 0) <= 0.5:
            score_commodites += 10
        if commodites.get('hopitaux', 0) <= 5:
            score_commodites += 10
        
        score += score_commodites
        details['Commodités'] = f"{score_commodites}/40 points"
        
        # Développement futur
        developpement = data.get('developpement_futur', 'moyen')
        dev_scores = {'fort': 20, 'moyen': 10, 'faible': 5}
        score += dev_scores.get(developpement, 10)
        details['Potentiel développement'] = developpement.capitalize()
        
        return min(score, 100), details
    
    @staticmethod
    def calculate_property_score(data):
        """Calcul du score du bien (20% du score total)"""
        score = 0
        details = {}
        
        # Type de bien
        type_bien = data.get('type_bien', 'appartement')
        type_scores = {
            'villa': 30,
            'riad': 25,
            'appartement': 20,
            'studio': 15,
            'terrain': 10
        }
        score += type_scores.get(type_bien, 20)
        details['Type'] = type_bien.capitalize()
        
        # État du bien
        etat = data.get('etat', 'ready')
        etat_scores = {
            'neuf': 30,
            'ready': 25,
            'off-plan': 20,
            'renovation': 15
        }
        score += etat_scores.get(etat, 20)
        details['État'] = etat.capitalize()
        
        # Surface
        surface = data.get('surface', 0)
        if surface >= 150:
            score += 20
            details['Surface'] = f"Grande ({surface}m²)"
        elif surface >= 80:
            score += 15
            details['Surface'] = f"Moyenne ({surface}m²)"
        else:
            score += 10
            details['Surface'] = f"Petite ({surface}m²)"
        
        # Qualité de construction
        qualite = data.get('qualite_construction', 'standard')
        qualite_scores = {'luxe': 20, 'premium': 15, 'standard': 10}
        score += qualite_scores.get(qualite, 10)
        details['Qualité'] = qualite.capitalize()
        
        return min(score, 100), details
    
    @staticmethod
    def calculate_risk_score(data):
        """Calcul du score de risque (10% du score total)"""
        score = 100  # On part de 100 et on déduit
        details = {}
        
        # Risque promoteur
        promoteur = data.get('reputation_promoteur', 'moyenne')
        if promoteur == 'excellente':
            score -= 0
            details['Promoteur'] = "Très fiable"
        elif promoteur == 'bonne':
            score -= 10
            details['Promoteur'] = "Fiable"
        elif promoteur == 'moyenne':
            score -= 25
            details['Promoteur'] = "Standard"
        else:
            score -= 50
            details['Promoteur'] = "Risqué"
        
        # Liquidité
        liquidite = data.get('liquidite', 'moyenne')
        if liquidite == 'elevee':
            score -= 0
            details['Liquidité'] = "Très liquide"
        elif liquidite == 'moyenne':
            score -= 15
            details['Liquidité'] = "Moyenne"
        else:
            score -= 30
            details['Liquidité'] = "Faible"
        
        # Garanties
        garanties = data.get('garanties', False)
        if garanties:
            score -= 0
            details['Garanties'] = "Présentes"
        else:
            score -= 20
            details['Garanties'] = "Absentes"
        
        return max(score, 0), details
    
    @staticmethod
    def calculate_global_score(data):
        """Calcul du score global DARY"""
        # Calcul des sous-scores
        financial, financial_details = DARYScoring.calculate_financial_score(data)
        location, location_details = DARYScoring.calculate_location_score(data)
        property_score, property_details = DARYScoring.calculate_property_score(data)
        risk, risk_details = DARYScoring.calculate_risk_score(data)
        
        # Pondération
        global_score = (
            financial * 0.40 +
            location * 0.30 +
            property_score * 0.20 +
            risk * 0.10
        )
        
        # Détermination du niveau
        if global_score >= 80:
            niveau = "Excellent"
            couleur = "#3CE58E"
            recommendation = "Investissement hautement recommandé"
        elif global_score >= 60:
            niveau = "Bon"
            couleur = "#4CAF50"
            recommendation = "Investissement recommandé"
        elif global_score >= 40:
            niveau = "Moyen"
            couleur = "#FFC107"
            recommendation = "Investissement à étudier avec précaution"
        else:
            niveau = "Faible"
            couleur = "#FF5722"
            recommendation = "Investissement déconseillé"
        
        return {
            'score_global': round(global_score, 1),
            'niveau': niveau,
            'couleur': couleur,
            'recommendation': recommendation,
            'scores': {
                'Financier': {'score': financial, 'details': financial_details, 'poids': '40%'},
                'Localisation': {'score': location, 'details': location_details, 'poids': '30%'},
                'Propriété': {'score': property_score, 'details': property_details, 'poids': '20%'},
                'Risque': {'score': risk, 'details': risk_details, 'poids': '10%'}
            },
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def create_gauge_chart(score, title="Score DARY"):
    """Création d'un graphique gauge pour le score"""
    if score >= 80:
        color = "#3CE58E"
    elif score >= 60:
        color = "#4CAF50"
    elif score >= 40:
        color = "#FFC107"
    else:
        color = "#FF5722"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        title={'text': title, 'font': {'size': 24, 'color': 'white'}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "white"},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 3,
            'bordercolor': "white",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(255, 87, 34, 0.3)'},
                {'range': [40, 60], 'color': 'rgba(255, 193, 7, 0.3)'},
                {'range': [60, 80], 'color': 'rgba(76, 175, 80, 0.3)'},
                {'range': [80, 100], 'color': 'rgba(60, 229, 142, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'size': 16},
        showlegend=False,
        margin=dict(l=20, r=20, t=80, b=20)
    )
    
    return fig

def create_spider_chart(scores_dict):
    """Création d'un graphique radar pour les sous-scores"""
    categories = list(scores_dict.keys())
    values = [scores_dict[cat]['score'] for cat in categories]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(60, 229, 142, 0.3)',
        line=dict(color='#3CE58E', width=3),
        marker=dict(size=10, color='#3CE58E')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color='white'),
                gridcolor='rgba(255,255,255,0.2)'
            ),
            angularaxis=dict(
                tickfont=dict(color='white', size=14),
                gridcolor='rgba(255,255,255,0.2)'
            ),
            bgcolor='rgba(11, 34, 57, 0.5)'
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        title={
            'text': 'Analyse Multi-Critères',
            'font': {'size': 20, 'color': 'white'},
            'x': 0.5,
            'xanchor': 'center'
        },
        margin=dict(l=80, r=80, t=100, b=80)
    )
    
    return fig

def generate_pdf_report(data, scores):
    """Génération d'un rapport PDF (simulé avec HTML)"""
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial; padding: 20px; }}
            h1 {{ color: #0B2239; }}
            h2 {{ color: #3CE58E; }}
            .score {{ font-size: 48px; font-weight: bold; color: {scores['couleur']}; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
            th {{ background: #0B2239; color: white; }}
        </style>
    </head>
    <body>
        <h1>Rapport DARY Score</h1>
        <p>Date: {scores['timestamp']}</p>
        <h2>Score Global: <span class="score">{scores['score_global']}/100</span></h2>
        <p>Niveau: {scores['niveau']}</p>
        <p>Recommandation: {scores['recommendation']}</p>
        
        <h2>Analyse Détaillée</h2>
        <table>
            <tr>
                <th>Critère</th>
                <th>Score</th>
                <th>Poids</th>
                <th>Détails</th>
            </tr>
    """
    
    for categorie, info in scores['scores'].items():
        details_str = ', '.join([f"{k}: {v}" for k, v in info['details'].items()])
        html_content += f"""
            <tr>
                <td>{categorie}</td>
                <td>{info['score']}/100</td>
                <td>{info['poids']}</td>
                <td>{details_str}</td>
            </tr>
        """
    
    html_content += """
        </table>
        <p style="margin-top: 50px; font-size: 12px; color: #666;">
            © 2024 DARY Score - Simulateur d'Investissement Immobilier Intelligent
        </p>
    </body>
    </html>
    """
    
    return html_content

def download_button(data, filename, label):
    """Créer un bouton de téléchargement"""
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="{filename}" style="display: inline-block; padding: 0.75rem 2rem; background: #3CE58E; color: #0B2239; text-decoration: none; border-radius: 25px; font-weight: bold; margin-top: 1rem;">{label}</a>'
    return href

# Interface principale
tab1, tab2, tab3, tab4 = st.tabs(["📊 Nouveau Calcul", "📈 Historique", "📁 Import CSV", "📖 Documentation"])

with tab1:
    st.markdown('<div class="section-header">📊 Calcul du Score DARY</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="metric-card"><h3>🏢 Informations du Projet</h3>', unsafe_allow_html=True)
        nom_projet = st.text_input("Nom du projet", "Résidence Les Jardins", key="nom")
        type_bien = st.selectbox("Type de bien", ['appartement', 'villa', 'riad', 'studio', 'terrain'], key="type")
        etat = st.selectbox("État du bien", ['neuf', 'ready', 'off-plan', 'renovation'], key="etat")
        surface = st.number_input("Surface (m²)", 10, 1000, 80, key="surface")
        qualite_construction = st.selectbox("Qualité de construction", ['standard', 'premium', 'luxe'], key="qualite")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card"><h3>📍 Localisation</h3>', unsafe_allow_html=True)
        zone = st.selectbox("Zone", ['standard', 'emergente', 'prime', 'premium'], key="zone")
        
        st.markdown("**Proximité des commodités (km):**")
        col_a, col_b = st.columns(2)
        with col_a:
            dist_ecoles = st.number_input("Écoles", 0.0, 20.0, 2.0, 0.5, key="ecoles")
            dist_commerces = st.number_input("Commerces", 0.0, 20.0, 1.0, 0.5, key="commerces")
        with col_b:
            dist_transport = st.number_input("Transport", 0.0, 20.0, 0.5, 0.5, key="transport")
            dist_hopitaux = st.number_input("Hôpitaux", 0.0, 20.0, 3.0, 0.5, key="hopitaux")
        
        developpement_futur = st.selectbox("Potentiel de développement", ['faible', 'moyen', 'fort'], key="dev")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card"><h3>💰 Données Financières</h3>', unsafe_allow_html=True)
        ticket_minimum = st.number_input("Ticket minimum (MAD)", 1000, 10000000, 50000, 1000, key="ticket")
        roi_projete = st.slider("ROI projeté (%)", 0.0, 30.0, 10.0, 0.5, key="roi")
        rendement_locatif = st.slider("Rendement locatif (%)", 0.0, 15.0, 5.0, 0.5, key="rendement")
        plus_value_estimee = st.slider("Plus-value estimée (%)", 0.0, 50.0, 15.0, 1.0, key="plus_value")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card"><h3>⚠️ Gestion des Risques</h3>', unsafe_allow_html=True)
        reputation_promoteur = st.selectbox("Réputation du promoteur", ['faible', 'moyenne', 'bonne', 'excellente'], key="promoteur")
        liquidite = st.selectbox("Liquidité du marché", ['faible', 'moyenne', 'elevee'], key="liquidite")
        garanties = st.checkbox("Garanties disponibles", key="garanties")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Bouton de calcul
    col_button = st.columns([1, 2, 1])[1]
    with col_button:
        if st.button("🚀 Calculer le Score DARY", type="primary", use_container_width=True):
            # Préparation des données
            data = {
                'nom_projet': nom_projet,
                'type_bien': type_bien,
                'etat': etat,
                'surface': surface,
                'qualite_construction': qualite_construction,
                'zone': zone,
                'commodites': {
                    'ecoles': dist_ecoles,
                    'commerces': dist_commerces,
                    'transport': dist_transport,
                    'hopitaux': dist_hopitaux
                },
                'developpement_futur': developpement_futur,
                'ticket_minimum': ticket_minimum,
                'roi_projete': roi_projete,
                'rendement_locatif': rendement_locatif,
                'plus_value_estimee': plus_value_estimee,
                'reputation_promoteur': reputation_promoteur,
                'liquidite': liquidite,
                'garanties': garanties
            }
            
            # Calcul du score
            with st.spinner('Analyse en cours...'):
                scores = DARYScoring.calculate_global_score(data)
                st.session_state.current_scores = scores
                st.session_state.projects.append({
                    'nom': nom_projet,
                    'date': scores['timestamp'],
                    'score': scores['score_global'],
                    'niveau': scores['niveau'],
                    'data': data,
                    'scores': scores
                })
            
            # Affichage des résultats
            st.success("✅ Analyse terminée!")
            
            # Score principal avec gauge
            st.markdown('<div class="section-header">🎯 Résultats de l\'Analyse</div>', unsafe_allow_html=True)
            
            col_score1, col_score2 = st.columns([2, 1])
            
            with col_score1:
                fig_gauge = create_gauge_chart(scores['score_global'])
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            with col_score2:
                st.markdown(f"""
                <div class="metric-card" style="text-align: center; padding: 2rem;">
                    <h2 style="color: #0B2239;">Score Global</h2>
                    <div style="font-size: 4rem; font-weight: bold; color: {scores['couleur']};">
                        {scores['score_global']}/100
                    </div>
                    <div class="score-badge score-{scores['niveau'].lower()}" style="margin-top: 1rem;">
                        {scores['niveau']}
                    </div>
                    <p style="margin-top: 1rem; color: #555;">
                        {scores['recommendation']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Graphique radar
            st.markdown('<div class="section-header">📊 Analyse Multi-Critères</div>', unsafe_allow_html=True)
            fig_spider = create_spider_chart(scores['scores'])
            st.plotly_chart(fig_spider, use_container_width=True)
            
            # Tableau détaillé
            st.markdown('<div class="section-header">📋 Détails par Catégorie</div>', unsafe_allow_html=True)
            
            details_data = []
            for categorie, info in scores['scores'].items():
                for critere, valeur in info['details'].items():
                    details_data.append({
                        'Catégorie': categorie,
                        'Critère': critere,
                        'Évaluation': valeur,
                        'Score': f"{info['score']}/100",
                        'Poids': info['poids']
                    })
            
            df_details = pd.DataFrame(details_data)
            st.dataframe(df_details, use_container_width=True, hide_index=True)
            
            # Export des résultats
            st.markdown('<div class="section-header">💾 Export des Résultats</div>', unsafe_allow_html=True)
            
            col_export1, col_export2, col_export3 = st.columns(3)
            
            with col_export1:
                # Export JSON
                json_data = json.dumps(scores, indent=2)
                b64_json = base64.b64encode(json_data.encode()).decode()
                st.markdown(
                    f'<a href="data:application/json;base64,{b64_json}" '
                    f'download="dary_score_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json" '
                    f'style="display: inline-block; padding: 0.75rem 2rem; background: #3CE58E; '
                    f'color: #0B2239; text-decoration: none; border-radius: 25px; font-weight: bold;">📄 Télécharger JSON</a>',
                    unsafe_allow_html=True
                )
            
            with col_export2:
                # Export HTML (rapport)
                html_report = generate_pdf_report(data, scores)
                st.markdown(
                    download_button(html_report, 
                                  f"rapport_dary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                                  "📊 Télécharger Rapport"),
                    unsafe_allow_html=True
                )
            
            with col_export3:
                # Export CSV
                csv_data = pd.DataFrame([{
                    'Projet': nom_projet,
                    'Date': scores['timestamp'],
                    'Score Global': scores['score_global'],
                    'Niveau': scores['niveau'],
                    'Score Financier': scores['scores']['Financier']['score'],
                    'Score Localisation': scores['scores']['Localisation']['score'],
                    'Score Propriété': scores['scores']['Propriété']['score'],
                    'Score Risque': scores['scores']['Risque']['score']
                }]).to_csv(index=False)
                
                b64_csv = base64.b64encode(csv_data.encode()).decode()
                st.markdown(
                    f'<a href="data:text/csv;base64,{b64_csv}" '
                    f'download="export_dary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv" '
                    f'style="display: inline-block; padding: 0.75rem 2rem; background: #3CE58E; '
                    f'color: #0B2239; text-decoration: none; border-radius: 25px; font-weight: bold;">📑 Télécharger CSV</a>',
                    unsafe_allow_html=True
                )

with tab2:
    st.markdown('<div class="section-header">📈 Historique des Analyses</div>', unsafe_allow_html=True)
    
    if st.session_state.projects:
        # Graphique d'évolution
        df_history = pd.DataFrame(st.session_state.projects)
        
        fig_history = px.line(df_history, x='date', y='score', 
                              title='Évolution des Scores DARY',
                              markers=True, hover_data=['nom', 'niveau'])
        fig_history.update_traces(line_color='#3CE58E', marker_size=10)
        fig_history.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis_title='Date',
            yaxis_title='Score',
            height=400
        )
        st.plotly_chart(fig_history, use_container_width=True)
        
        # Tableau historique
        st.markdown('<div class="section-header">📊 Projets Analysés</div>', unsafe_allow_html=True)
        
        for idx, projet in enumerate(reversed(st.session_state.projects)):
            with st.expander(f"🏢 {projet['nom']} - Score: {projet['score']} ({projet['niveau']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Score Global", f"{projet['score']}/100", projet['niveau'])
                    st.write(f"Date: {projet['date']}")
                with col2:
                    sous_scores = projet['scores']['scores']
                    for cat, info in sous_scores.items():
                        st.metric(cat, f"{info['score']}/100", info['poids'])
    else:
        st.info("📝 Aucune analyse effectuée pour le moment. Commencez par calculer un score dans l'onglet 'Nouveau Calcul'.")

with tab3:
    st.markdown('<div class="section-header">📁 Import de Données CSV</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>Format CSV requis:</strong><br>
        Le fichier doit contenir les colonnes suivantes: nom_projet, type_bien, etat, surface, 
        zone, roi_projete, rendement_locatif, ticket_minimum, plus_value_estimee
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choisir un fichier CSV", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ {len(df)} projets chargés avec succès!")
            
            st.dataframe(df, use_container_width=True)
            
            if st.button("🔄 Analyser tous les projets", type="primary"):
                results = []
                progress_bar = st.progress(0)
                
                for idx, row in df.iterrows():
                    # Conversion des données CSV en format attendu
                    data = {
                        'nom_projet': row.get('nom_projet', f'Projet {idx+1}'),
                        'type_bien': row.get('type_bien', 'appartement'),
                        'etat': row.get('etat', 'ready'),
                        'surface': row.get('surface', 80),
                        'qualite_construction': row.get('qualite_construction', 'standard'),
                        'zone': row.get('zone', 'standard'),
                        'commodites': {
                            'ecoles': row.get('dist_ecoles', 2),
                            'commerces': row.get('dist_commerces', 1),
                            'transport': row.get('dist_transport', 0.5),
                            'hopitaux': row.get('dist_hopitaux', 3)
                        },
                        'developpement_futur': row.get('developpement_futur', 'moyen'),
                        'ticket_minimum': row.get('ticket_minimum', 50000),
                        'roi_projete': row.get('roi_projete', 10),
                        'rendement_locatif': row.get('rendement_locatif', 5),
                        'plus_value_estimee': row.get('plus_value_estimee', 15),
                        'reputation_promoteur': row.get('reputation_promoteur', 'moyenne'),
                        'liquidite': row.get('liquidite', 'moyenne'),
                        'garanties': row.get('garanties', False)
                    }
                    
                    scores = DARYScoring.calculate_global_score(data)
                    results.append({
                        'Projet': data['nom_projet'],
                        'Score': scores['score_global'],
                        'Niveau': scores['niveau'],
                        'Recommandation': scores['recommendation']
                    })
                    
                    progress_bar.progress((idx + 1) / len(df))
                
                # Affichage des résultats
                df_results = pd.DataFrame(results)
                st.markdown('<div class="section-header">📊 Résultats de l\'Analyse Batch</div>', unsafe_allow_html=True)
                st.dataframe(df_results, use_container_width=True)
                
                # Export des résultats
                csv_export = df_results.to_csv(index=False)
                b64 = base64.b64encode(csv_export.encode()).decode()
                st.markdown(
                    f'<a href="data:text/csv;base64,{b64}" '
                    f'download="resultats_batch_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv" '
                    f'style="display: inline-block; padding: 0.75rem 2rem; background: #3CE58E; '
                    f'color: #0B2239; text-decoration: none; border-radius: 25px; font-weight: bold; margin-top: 1rem;">💾 Exporter les résultats</a>',
                    unsafe_allow_html=True
                )
                
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement du fichier: {str(e)}")

with tab4:
    st.markdown('<div class="section-header">📖 Guide d\'Utilisation</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <h3>🎯 Qu'est-ce que le DARY Score ?</h3>
        <p>Le DARY Score est un système de notation intelligent qui évalue le potentiel d'investissement 
        immobilier sur une échelle de 0 à 100. Il analyse quatre dimensions clés:</p>
        <ul>
            <li><strong>Financier (40%)</strong>: ROI, rendement locatif, ticket d'entrée, plus-value</li>
            <li><strong>Localisation (30%)</strong>: Zone, proximité des commodités, potentiel de développement</li>
            <li><strong>Propriété (20%)</strong>: Type, état, surface, qualité de construction</li>
            <li><strong>Risque (10%)</strong>: Réputation promoteur, liquidité, garanties</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <h3>📊 Interprétation des Scores</h3>
        <table style="width: 100%; margin-top: 1rem;">
            <tr>
                <th style="background: #3CE58E; color: white; padding: 10px;">Score</th>
                <th style="background: #3CE58E; color: white; padding: 10px;">Niveau</th>
                <th style="background: #3CE58E; color: white; padding: 10px;">Recommandation</th>
            </tr>
            <tr>
                <td style="padding: 10px;">80-100</td>
                <td style="padding: 10px;"><span class="score-badge score-excellent">Excellent</span></td>
                <td style="padding: 10px;">Investissement hautement recommandé</td>
            </tr>
            <tr>
                <td style="padding: 10px;">60-79</td>
                <td style="padding: 10px;"><span class="score-badge score-bon">Bon</span></td>
                <td style="padding: 10px;">Investissement recommandé</td>
            </tr>
            <tr>
                <td style="padding: 10px;">40-59</td>
                <td style="padding: 10px;"><span class="score-badge score-moyen">Moyen</span></td>
                <td style="padding: 10px;">À étudier avec précaution</td>
            </tr>
            <tr>
                <td style="padding: 10px;">0-39</td>
                <td style="padding: 10px;"><span class="score-badge score-faible">Faible</span></td>
                <td style="padding: 10px;">Investissement déconseillé</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <h3>💡 Conseils d'Utilisation</h3>
        <ol>
            <li><strong>Saisie manuelle</strong>: Remplissez le formulaire dans l'onglet "Nouveau Calcul"</li>
            <li><strong>Import CSV</strong>: Importez plusieurs projets simultanément</li>
            <li><strong>Analyse comparative</strong>: Consultez l'historique pour comparer les projets</li>
            <li><strong>Export</strong>: Téléchargez les rapports en JSON, HTML ou CSV</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Exemple de CSV
    st.markdown("""
    <div class="metric-card">
        <h3>📁 Exemple de fichier CSV</h3>
    </div>
    """, unsafe_allow_html=True)
    
    example_data = pd.DataFrame([
        {
            'nom_projet': 'Résidence Palmiers',
            'type_bien': 'appartement',
            'etat': 'neuf',
            'surface': 120,
            'zone': 'premium',
            'roi_projete': 12,
            'rendement_locatif': 6,
            'ticket_minimum': 75000,
            'plus_value_estimee': 25
        },
        {
            'nom_projet': 'Villa Océan',
            'type_bien': 'villa',
            'etat': 'ready',
            'surface': 250,
            'zone': 'prime',
            'roi_projete': 15,
            'rendement_locatif': 7,
            'ticket_minimum': 150000,
            'plus_value_estimee': 30
        }
    ])
    
    st.dataframe(example_data, use_container_width=True)
    
    # Télécharger l'exemple
    csv_example = example_data.to_csv(index=False)
    b64 = base64.b64encode(csv_example.encode()).decode()
    st.markdown(
        f'<a href="data:text/csv;base64,{b64}" '
        f'download="exemple_dary_score.csv" '
        f'style="display: inline-block; padding: 0.75rem 2rem; background: #3CE58E; '
        f'color: #0B2239; text-decoration: none; border-radius: 25px; font-weight: bold; margin-top: 1rem;">📥 Télécharger l\'exemple CSV</a>',
        unsafe_allow_html=True
    )

# Footer
st.markdown("""
<div style="margin-top: 3rem; padding: 2rem; background: rgba(11, 34, 57, 0.8); border-radius: 15px; text-align: center; border: 1px solid #3CE58E;">
    <p style="color: white; margin: 0;">
        🏢 <strong>DARY Score</strong> - Simulateur d'Investissement Immobilier Intelligent<br>
        <span style="color: #3CE58E;">Propulsé par l'IA pour des décisions d'investissement éclairées</span><br>
        <span style="font-size: 0.9rem; opacity: 0.8;">© 2024 - Version 1.0 | Marché Marocain</span>
    </p>
</div>
""", unsafe_allow_html=True)
