# 🏢 DARY Score - Simulateur d'Investissement Immobilier Intelligent

## 📋 Description

DARY Score est une plateforme d'analyse et de scoring immobilier basée sur l'IA, conçue spécifiquement pour le marché marocain. L'application permet d'évaluer le potentiel d'investissement de projets immobiliers en analysant plusieurs dimensions clés.

## 🎯 Fonctionnalités

- **Scoring Intelligent** : Évaluation multi-critères sur une échelle de 0 à 100
- **Analyse en 4 Dimensions** :
  - 💰 **Financier** (40%) : ROI, rendement locatif, ticket d'entrée, plus-value
  - 📍 **Localisation** (30%) : Zone, proximité des commodités, potentiel de développement
  - 🏢 **Propriété** (20%) : Type, état, surface, qualité de construction
  - ⚠️ **Risque** (10%) : Réputation promoteur, liquidité, garanties

- **Import/Export de Données** : Support CSV pour analyse batch
- **Visualisations Interactives** : Graphiques gauge, radar, et historiques
- **Rapports Détaillés** : Export en JSON, HTML, et CSV
- **Interface Moderne** : Design responsive avec thème DARY (bleu nuit #0B2239, vert #3CE58E)

## 🚀 Installation Locale

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/dary-score.git
cd dary-score
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancer l'application**
```bash
streamlit run dary_score_app.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

## ☁️ Déploiement en Ligne

### Option 1: Streamlit Cloud (Recommandé)

1. **Créer un compte sur [Streamlit Cloud](https://streamlit.io/cloud)**

2. **Préparer votre repository GitHub**
   - Créez un nouveau repository sur GitHub
   - Uploadez les fichiers : `dary_score_app.py`, `requirements.txt`, `projets_immobiliers_maroc.csv`

3. **Déployer sur Streamlit Cloud**
   - Connectez-vous à Streamlit Cloud
   - Cliquez sur "New app"
   - Sélectionnez votre repository GitHub
   - Choisissez la branche (main/master)
   - Spécifiez le fichier principal : `dary_score_app.py`
   - Cliquez sur "Deploy"

4. **URL de votre application**
   ```
   https://[votre-username]-dary-score-[random].streamlit.app
   ```

### Option 2: Hugging Face Spaces

1. **Créer un compte sur [Hugging Face](https://huggingface.co)**

2. **Créer un nouveau Space**
   - Allez sur https://huggingface.co/spaces
   - Cliquez sur "Create new Space"
   - Nom : `DARY-Score`
   - SDK : Choisissez "Streamlit"
   - Visibilité : Public

3. **Uploader les fichiers**
   - Via l'interface web ou git :
   ```bash
   git clone https://huggingface.co/spaces/[votre-username]/DARY-Score
   cd DARY-Score
   # Copiez les fichiers du projet
   git add .
   git commit -m "Initial deployment"
   git push
   ```

4. **URL de votre application**
   ```
   https://huggingface.co/spaces/[votre-username]/DARY-Score
   ```

### Option 3: Render

1. **Créer un compte sur [Render](https://render.com)**

2. **Créer un fichier `render.yaml`**
```yaml
services:
  - type: web
    name: dary-score
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "streamlit run dary_score_app.py --server.port $PORT --server.address 0.0.0.0"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

3. **Déployer sur Render**
   - Connectez votre repository GitHub
   - Render détectera automatiquement le fichier `render.yaml`
   - Cliquez sur "Create Web Service"

## 📊 Format des Données CSV

Le fichier CSV doit contenir les colonnes suivantes :

| Colonne | Type | Description |
|---------|------|-------------|
| nom_projet | String | Nom du projet immobilier |
| type_bien | String | appartement, villa, riad, studio, terrain |
| etat | String | neuf, ready, off-plan, renovation |
| surface | Float | Surface en m² |
| qualite_construction | String | standard, premium, luxe |
| zone | String | standard, emergente, prime, premium |
| dist_ecoles | Float | Distance aux écoles (km) |
| dist_commerces | Float | Distance aux commerces (km) |
| dist_transport | Float | Distance aux transports (km) |
| dist_hopitaux | Float | Distance aux hôpitaux (km) |
| developpement_futur | String | faible, moyen, fort |
| ticket_minimum | Float | Ticket d'entrée minimum (MAD) |
| roi_projete | Float | ROI projeté (%) |
| rendement_locatif | Float | Rendement locatif (%) |
| plus_value_estimee | Float | Plus-value estimée (%) |
| reputation_promoteur | String | faible, moyenne, bonne, excellente |
| liquidite | String | faible, moyenne, elevee |
| garanties | Boolean | True/False |

## 🔧 Configuration Avancée

### Personnalisation des Seuils de Scoring

Modifiez les seuils dans la classe `DARYScoring` du fichier `dary_score_app.py` :

```python
# Exemple : Modifier les seuils de ROI
if roi >= 15:  # Excellent
    score += 30
elif roi >= 10:  # Bon
    score += 20
# ...
```

### Personnalisation des Couleurs

Modifiez les couleurs dans la section CSS du fichier principal :

```python
st.markdown("""
<style>
    .main-header {
        background: #0B2239;  # Couleur de fond
        border: 2px solid #3CE58E;  # Couleur d'accent
    }
</style>
""", unsafe_allow_html=True)
```

## 📈 Utilisation de l'Application

### 1. Calcul Manuel
- Remplissez le formulaire dans l'onglet "Nouveau Calcul"
- Cliquez sur "Calculer le Score DARY"
- Visualisez les résultats et exportez les rapports

### 2. Import Batch
- Préparez votre fichier CSV avec les colonnes requises
- Uploadez le fichier dans l'onglet "Import CSV"
- Cliquez sur "Analyser tous les projets"
- Exportez les résultats consolidés

### 3. Analyse Comparative
- Consultez l'onglet "Historique" pour voir l'évolution des scores
- Comparez plusieurs projets sur le graphique temporel
- Exportez l'historique complet

## 🔐 Sécurité et Conformité

- Les données sont traitées localement dans le navigateur
- Aucune donnée n'est stockée sur des serveurs externes
- Conforme aux réglementations marocaines sur la protection des données
- Chiffrement des exports sensibles recommandé

## 📞 Support

Pour toute question ou assistance :
- 📧 Email : support@dary-score.ma
- 📱 WhatsApp : +212 XXX XXX XXX
- 🌐 Site web : www.dary-score.ma

## 📄 Licence

© 2024 DARY Score - Tous droits réservés

---

**Note** : Cette application est un outil d'aide à la décision. Les scores générés sont indicatifs et ne constituent pas un conseil d'investissement professionnel. Consultez toujours un expert immobilier avant toute décision d'investissement.
