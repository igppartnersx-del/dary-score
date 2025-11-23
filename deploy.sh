#!/bin/bash

# ========================================
# Script de déploiement DARY Score
# ========================================

echo "🚀 Déploiement de DARY Score"
echo "============================="

# Couleurs pour l'affichage
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier Python
log_info "Vérification de Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    log_success "Python $PYTHON_VERSION détecté"
else
    log_error "Python 3 n'est pas installé"
    exit 1
fi

# Créer l'environnement virtuel
log_info "Création de l'environnement virtuel..."
python3 -m venv venv
source venv/bin/activate
log_success "Environnement virtuel créé"

# Installer les dépendances
log_info "Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt
log_success "Dépendances installées"

# Tester l'application localement
log_info "Test de l'application..."
timeout 5 streamlit run dary_score_app.py --server.headless true --server.port 8502 &
STREAMLIT_PID=$!
sleep 3

if ps -p $STREAMLIT_PID > /dev/null; then
    log_success "Application testée avec succès"
    kill $STREAMLIT_PID
else
    log_error "Erreur lors du test de l'application"
    exit 1
fi

# Menu de déploiement
echo ""
echo "📦 Options de déploiement:"
echo "=========================="
echo "1) Streamlit Cloud (Recommandé)"
echo "2) Hugging Face Spaces"
echo "3) Render"
echo "4) Local seulement"
echo ""
read -p "Choisissez une option (1-4): " choice

case $choice in
    1)
        log_info "Préparation pour Streamlit Cloud..."
        
        # Vérifier Git
        if ! command -v git &> /dev/null; then
            log_error "Git n'est pas installé. Installez Git et réessayez."
            exit 1
        fi
        
        # Initialiser Git si nécessaire
        if [ ! -d ".git" ]; then
            git init
            log_success "Repository Git initialisé"
        fi
        
        # Créer .gitignore
        cat > .gitignore << EOF
venv/
__pycache__/
*.pyc
.env
.DS_Store
*.log
EOF
        log_success "Fichier .gitignore créé"
        
        # Ajouter les fichiers
        git add dary_score_app.py requirements.txt README.md projets_immobiliers_maroc.csv .streamlit/
        git commit -m "Initial deployment of DARY Score"
        
        log_warning "Étapes suivantes pour Streamlit Cloud:"
        echo "1. Créez un repository sur GitHub"
        echo "2. Ajoutez le remote: git remote add origin https://github.com/VOTRE-USERNAME/dary-score.git"
        echo "3. Push: git push -u origin main"
        echo "4. Allez sur https://streamlit.io/cloud"
        echo "5. Connectez votre repository GitHub"
        echo "6. Déployez l'application"
        ;;
        
    2)
        log_info "Préparation pour Hugging Face Spaces..."
        
        # Créer app.py (alias pour HF Spaces)
        cp dary_score_app.py app.py
        
        # Créer README pour HF Spaces
        cat > README_HF.md << EOF
---
title: DARY Score
emoji: 🏢
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.31.0
app_file: app.py
pinned: false
---

# DARY Score - Simulateur d'Investissement Immobilier Intelligent

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
EOF
        
        log_success "Fichiers préparés pour Hugging Face"
        log_warning "Étapes suivantes:"
        echo "1. Créez un compte sur https://huggingface.co"
        echo "2. Installez git-lfs: git lfs install"
        echo "3. Clonez votre Space: git clone https://huggingface.co/spaces/VOTRE-USERNAME/DARY-Score"
        echo "4. Copiez les fichiers et pushez"
        ;;
        
    3)
        log_info "Préparation pour Render..."
        
        # Créer render.yaml
        cat > render.yaml << EOF
services:
  - type: web
    name: dary-score
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "streamlit run dary_score_app.py --server.port \$PORT --server.address 0.0.0.0"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
EOF
        
        log_success "Fichier render.yaml créé"
        log_warning "Étapes suivantes:"
        echo "1. Créez un compte sur https://render.com"
        echo "2. Connectez votre repository GitHub"
        echo "3. Render détectera automatiquement le fichier render.yaml"
        ;;
        
    4)
        log_info "Lancement de l'application en local..."
        log_success "L'application est prête!"
        echo ""
        echo "Pour lancer l'application:"
        echo "  source venv/bin/activate"
        echo "  streamlit run dary_score_app.py"
        echo ""
        log_info "L'application sera accessible sur http://localhost:8501"
        
        # Lancer l'application
        read -p "Voulez-vous lancer l'application maintenant? (o/n): " launch
        if [ "$launch" = "o" ]; then
            streamlit run dary_score_app.py
        fi
        ;;
        
    *)
        log_error "Option invalide"
        exit 1
        ;;
esac

echo ""
log_success "Déploiement terminé avec succès!"
echo ""
echo "📚 Documentation complète disponible dans README.md"
echo "💬 Support: support@dary-score.ma"
echo ""
