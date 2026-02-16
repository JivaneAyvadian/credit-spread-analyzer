# Credit Spread Analyzer

**Outil d'Analyse et de Visualisation de Spreads de Crédit**

Auteur : Jivane Ayvadian  
Date : Février 2026  
Formation : Grenoble École de Management

---

## 📌 Description

Outil Python permettant d'analyser l'évolution des spreads de crédit (CDS) pour différents émetteurs. Il automatise le traitement de données, le calcul de statistiques, et la génération de visualisations professionnelles.

**Objectif** : Me familiariser avec l'analyse de données de marché crédit en vue d'un stage en structuration crédit et dérivés.

---

## ⚡ Installation Rapide

```bash
# Installer les dépendances
pip install pandas openpyxl matplotlib

# Exécuter l'analyse
python credit_spread_analyzer.py
```

---

## 📊 Fonctionnalités

- ✅ Import automatique de données CDS depuis Excel
- ✅ Calcul de statistiques (moyenne, min/max, volatilité, variations)
- ✅ Génération de 3 graphiques professionnels
- ✅ Export d'un dashboard Excel structuré
- ✅ Code modulaire et commenté

---

## 📁 Structure du Projet

```
credit-spread-analyzer/
│
├── credit_spread_analyzer.py      # Script principal
├── cds_data_sample.xlsx           # Données d'exemple
├── Credit_Spread_Dashboard.xlsx   # Dashboard généré (output)
│
├── spread_evolution.png           # Graphique 1 (output)
├── spread_comparison.png          # Graphique 2 (output)
├── spread_volatility.png          # Graphique 3 (output)
│
├── README.md                      # Ce fichier
└── Documentation.docx             # Documentation complète
```

---

## 🚀 Utilisation

### 1. Préparer les données

Le fichier Excel doit contenir un onglet `CDS_Data` avec :
- **Date** : Date de cotation (YYYY-MM-DD)
- **Emetteur** : Nom de l'entreprise
- **Spread (bps)** : Spread CDS en basis points

### 2. Lancer l'analyse

```bash
python credit_spread_analyzer.py
```

### 3. Résultats

Le script génère automatiquement :
- `Credit_Spread_Dashboard.xlsx` : Dashboard avec statistiques
- `spread_evolution.png` : Évolution temporelle des spreads
- `spread_comparison.png` : Comparaison des spreads actuels
- `spread_volatility.png` : Analyse de la volatilité

---

## 🛠️ Technologies

- **Python 3.8+**
- **pandas** : Manipulation de données
- **matplotlib** : Visualisations
- **openpyxl** : Excel automation

---

## 📈 Exemple de Résultats

Le dashboard Excel contient :

| Émetteur | Spread actuel | Spread moyen | Volatilité | Variation 1M |
|----------|---------------|--------------|------------|--------------|
| BNP Paribas | 82.5 bps | 80.3 bps | 1.24% | +2.3 bps |
| Société Générale | 98.1 bps | 95.7 bps | 1.45% | +4.8 bps |
| ... | ... | ... | ... | ... |

---

## 💡 Compétences Démontrées

- ✅ Python (POO, pandas, matplotlib)
- ✅ Data Analysis (statistiques, visualisation)
- ✅ Excel Automation (openpyxl)
- ✅ Compréhension des marchés crédit (CDS, spreads)
- ✅ Documentation technique

---

## 🔄 Évolutions Possibles

- Connexion API de données temps réel (Bloomberg, Refinitiv)
- Alertes automatiques si spread > seuil
- Calcul de corrélations entre émetteurs
- Interface graphique (Streamlit/Dash)
- Export PDF automatique

---

## 📧 Contact

**Jivane Ayvadian**  
Grenoble École de Management  
Février 2026

---

**Note** : Ce projet a été développé dans le cadre d'une démarche d'auto-apprentissage en finance de marché et programmation Python, en préparation à un stage en structuration crédit et produits dérivés.
