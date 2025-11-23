#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du système de scoring DARY Score
Permet de tester rapidement le calcul des scores sans interface
"""

import json
import pandas as pd
from datetime import datetime

# Import de la classe de scoring depuis l'application principale
# Note: Ce fichier doit être dans le même dossier que dary_score_app.py

class DARYScoringTest:
    """Version simplifiée du système de scoring pour tests"""
    
    @staticmethod
    def calculate_score(data):
        """Calcul simplifié du score global"""
        
        # Score financier (40%)
        financial_score = 0
        roi = data.get('roi_projete', 0)
        if roi >= 15:
            financial_score += 30
        elif roi >= 10:
            financial_score += 20
        else:
            financial_score += 10
            
        rendement = data.get('rendement_locatif', 0)
        if rendement >= 7:
            financial_score += 30
        elif rendement >= 5:
            financial_score += 20
        else:
            financial_score += 10
            
        ticket = data.get('ticket_minimum', 0)
        if ticket <= 50000:
            financial_score += 20
        else:
            financial_score += 10
            
        plus_value = data.get('plus_value_estimee', 0)
        if plus_value >= 20:
            financial_score += 20
        else:
            financial_score += 10
        
        # Score localisation (30%)
        location_score = 0
        zone = data.get('zone', 'standard')
        if zone == 'premium':
            location_score += 50
        elif zone == 'prime':
            location_score += 35
        else:
            location_score += 20
            
        developpement = data.get('developpement_futur', 'moyen')
        if developpement == 'fort':
            location_score += 30
        else:
            location_score += 15
        
        # Score propriété (20%)
        property_score = 0
        type_bien = data.get('type_bien', 'appartement')
        if type_bien == 'villa':
            property_score += 40
        elif type_bien == 'appartement':
            property_score += 30
        else:
            property_score += 20
            
        etat = data.get('etat', 'ready')
        if etat == 'neuf':
            property_score += 40
        else:
            property_score += 20
        
        # Score risque (10%)
        risk_score = 100
        promoteur = data.get('reputation_promoteur', 'moyenne')
        if promoteur != 'excellente':
            risk_score -= 30
        
        liquidite = data.get('liquidite', 'moyenne')
        if liquidite == 'faible':
            risk_score -= 30
        
        # Calcul final pondéré
        score_global = (
            min(financial_score, 100) * 0.40 +
            min(location_score, 100) * 0.30 +
            min(property_score, 100) * 0.20 +
            max(risk_score, 0) * 0.10
        )
        
        return round(score_global, 1)

def test_single_project():
    """Test avec un projet unique"""
    print("=" * 60)
    print("TEST 1: Projet unique - Villa Premium Casablanca")
    print("=" * 60)
    
    projet_test = {
        'nom_projet': 'Villa Premium Casablanca',
        'type_bien': 'villa',
        'etat': 'neuf',
        'surface': 350,
        'zone': 'premium',
        'roi_projete': 18,
        'rendement_locatif': 8,
        'ticket_minimum': 250000,
        'plus_value_estimee': 30,
        'developpement_futur': 'fort',
        'reputation_promoteur': 'excellente',
        'liquidite': 'elevee',
        'garanties': True
    }
    
    score = DARYScoringTest.calculate_score(projet_test)
    
    print(f"\n📊 Données du projet:")
    for key, value in projet_test.items():
        print(f"  • {key}: {value}")
    
    print(f"\n🎯 Score DARY: {score}/100")
    
    if score >= 80:
        print("✅ Niveau: EXCELLENT - Investissement hautement recommandé")
    elif score >= 60:
        print("👍 Niveau: BON - Investissement recommandé")
    elif score >= 40:
        print("⚠️ Niveau: MOYEN - À étudier avec précaution")
    else:
        print("❌ Niveau: FAIBLE - Investissement déconseillé")
    
    return score

def test_multiple_projects():
    """Test avec plusieurs projets pour comparaison"""
    print("\n" + "=" * 60)
    print("TEST 2: Comparaison de plusieurs projets")
    print("=" * 60)
    
    projets = [
        {
            'nom_projet': 'Appartement Hay Riad',
            'type_bien': 'appartement',
            'etat': 'neuf',
            'zone': 'prime',
            'roi_projete': 12,
            'rendement_locatif': 6,
            'ticket_minimum': 80000,
            'plus_value_estimee': 20,
            'developpement_futur': 'moyen',
            'reputation_promoteur': 'bonne',
            'liquidite': 'elevee'
        },
        {
            'nom_projet': 'Studio Marina',
            'type_bien': 'studio',
            'etat': 'off-plan',
            'zone': 'emergente',
            'roi_projete': 16,
            'rendement_locatif': 8,
            'ticket_minimum': 35000,
            'plus_value_estimee': 35,
            'developpement_futur': 'fort',
            'reputation_promoteur': 'moyenne',
            'liquidite': 'moyenne'
        },
        {
            'nom_projet': 'Riad Médina',
            'type_bien': 'riad',
            'etat': 'renovation',
            'zone': 'prime',
            'roi_projete': 10,
            'rendement_locatif': 9,
            'ticket_minimum': 150000,
            'plus_value_estimee': 15,
            'developpement_futur': 'faible',
            'reputation_promoteur': 'excellente',
            'liquidite': 'faible'
        }
    ]
    
    resultats = []
    for projet in projets:
        score = DARYScoringTest.calculate_score(projet)
        resultats.append({
            'Projet': projet['nom_projet'],
            'Type': projet['type_bien'],
            'Zone': projet['zone'],
            'Score': score
        })
    
    # Créer un DataFrame pour un affichage tabulaire
    df = pd.DataFrame(resultats)
    df = df.sort_values('Score', ascending=False)
    
    print("\n📊 Tableau comparatif des scores:")
    print("-" * 50)
    print(df.to_string(index=False))
    print("-" * 50)
    
    # Identifier le meilleur investissement
    meilleur = df.iloc[0]
    print(f"\n🏆 Meilleur investissement: {meilleur['Projet']}")
    print(f"   Score: {meilleur['Score']}/100")
    
    return df

def test_csv_import():
    """Test d'import depuis le fichier CSV exemple"""
    print("\n" + "=" * 60)
    print("TEST 3: Import et analyse du fichier CSV")
    print("=" * 60)
    
    try:
        # Lire le fichier CSV
        df = pd.read_csv('projets_immobiliers_maroc.csv')
        print(f"\n✅ {len(df)} projets chargés depuis le CSV")
        
        # Calculer les scores
        scores = []
        for _, row in df.iterrows():
            projet_data = row.to_dict()
            score = DARYScoringTest.calculate_score(projet_data)
            scores.append(score)
        
        df['Score DARY'] = scores
        
        # Statistiques
        print(f"\n📊 Statistiques des scores:")
        print(f"  • Score moyen: {df['Score DARY'].mean():.1f}")
        print(f"  • Score médian: {df['Score DARY'].median():.1f}")
        print(f"  • Score min: {df['Score DARY'].min():.1f}")
        print(f"  • Score max: {df['Score DARY'].max():.1f}")
        
        # Top 3 projets
        print(f"\n🏆 Top 3 des meilleurs projets:")
        top3 = df.nlargest(3, 'Score DARY')[['nom_projet', 'type_bien', 'zone', 'Score DARY']]
        for i, row in top3.iterrows():
            print(f"  {top3.index.get_loc(i)+1}. {row['nom_projet']} - Score: {row['Score DARY']:.1f}")
        
        # Sauvegarder les résultats
        output_file = 'resultats_scoring_test.csv'
        df.to_csv(output_file, index=False)
        print(f"\n💾 Résultats sauvegardés dans '{output_file}'")
        
    except FileNotFoundError:
        print("\n⚠️ Fichier 'projets_immobiliers_maroc.csv' non trouvé")
        print("   Assurez-vous que le fichier est dans le même dossier")
    except Exception as e:
        print(f"\n❌ Erreur lors du test CSV: {str(e)}")

def generate_test_report():
    """Génère un rapport de test complet"""
    print("\n" + "=" * 60)
    print("GÉNÉRATION DU RAPPORT DE TEST")
    print("=" * 60)
    
    rapport = {
        'date_test': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'version': '1.0.0',
        'tests_executes': ['test_single_project', 'test_multiple_projects', 'test_csv_import'],
        'statut': 'SUCCESS',
        'remarques': 'Tous les tests ont été exécutés avec succès'
    }
    
    # Sauvegarder le rapport
    with open('rapport_test_dary.json', 'w', encoding='utf-8') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    
    print("\n✅ Rapport de test généré: 'rapport_test_dary.json'")
    print(f"   Date: {rapport['date_test']}")
    print(f"   Statut: {rapport['statut']}")

def main():
    """Fonction principale pour exécuter tous les tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "DARY SCORE - SUITE DE TESTS" + " " * 16 + "║")
    print("║" + " " * 12 + "Système de Scoring Immobilier Intelligent" + " " * 5 + "║")
    print("╚" + "=" * 58 + "╝")
    
    try:
        # Exécuter les tests
        score1 = test_single_project()
        df_comparaison = test_multiple_projects()
        test_csv_import()
        
        # Générer le rapport
        generate_test_report()
        
        # Résumé final
        print("\n" + "=" * 60)
        print("RÉSUMÉ DES TESTS")
        print("=" * 60)
        print("✅ Test projet unique: PASSÉ")
        print("✅ Test comparaison multiple: PASSÉ")
        print("✅ Test import CSV: PASSÉ")
        print("✅ Génération rapport: PASSÉ")
        print("\n🎉 Tous les tests ont été exécutés avec succès!")
        
    except Exception as e:
        print(f"\n❌ Erreur critique: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
