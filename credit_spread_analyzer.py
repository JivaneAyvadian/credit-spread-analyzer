"""
Credit Spread Tracker & Dashboard Generator
Auteur: Jivane Ayvadian
Date: Février 2026

Description:
Outil d'analyse et de visualisation de spreads de crédit (CDS).
Import de données depuis Excel, calcul de statistiques, création de graphiques,
et génération d'un dashboard Excel automatique.

Prérequis:
- pandas
- openpyxl
- matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuration matplotlib pour des graphiques professionnels
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

class CreditSpreadAnalyzer:
    """
    Classe pour analyser les spreads de crédit et générer un dashboard.
    """
    
    def __init__(self, input_file):
        """
        Initialise l'analyseur avec le fichier de données.
        
        Args:
            input_file (str): Chemin vers le fichier Excel contenant les données CDS
        """
        self.input_file = input_file
        self.df = None
        self.stats = {}
        
    def load_data(self):
        """
        Charge les données depuis le fichier Excel.
        Attend un format avec colonnes: Date, Emetteur, Spread (bps)
        """
        print(f"📂 Chargement des données depuis {self.input_file}...")
        
        try:
            self.df = pd.read_excel(self.input_file, sheet_name='CDS_Data')
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df = self.df.sort_values('Date')
            
            print(f"✅ Données chargées: {len(self.df)} observations")
            print(f"   Période: {self.df['Date'].min().strftime('%Y-%m-%d')} à {self.df['Date'].max().strftime('%Y-%m-%d')}")
            print(f"   Émetteurs: {self.df['Emetteur'].nunique()}")
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {str(e)}")
            raise
    
    def calculate_statistics(self):
        """
        Calcule les statistiques descriptives pour chaque émetteur.
        """
        print("\n📊 Calcul des statistiques...")
        
        for emetteur in self.df['Emetteur'].unique():
            df_emetteur = self.df[self.df['Emetteur'] == emetteur].copy()
            
            # Calcul des variations
            df_emetteur['Variation'] = df_emetteur['Spread (bps)'].diff()
            df_emetteur['Variation (%)'] = df_emetteur['Spread (bps)'].pct_change() * 100
            
            self.stats[emetteur] = {
                'Spread actuel (bps)': df_emetteur['Spread (bps)'].iloc[-1],
                'Spread min (bps)': df_emetteur['Spread (bps)'].min(),
                'Spread max (bps)': df_emetteur['Spread (bps)'].max(),
                'Spread moyen (bps)': df_emetteur['Spread (bps)'].mean(),
                'Écart-type (bps)': df_emetteur['Spread (bps)'].std(),
                'Variation 1M (bps)': df_emetteur['Variation'].tail(20).sum() if len(df_emetteur) >= 20 else None,
                'Volatilité (%)': df_emetteur['Variation (%)'].std()
            }
        
        print("✅ Statistiques calculées pour tous les émetteurs")
    
    def create_visualizations(self):
        """
        Crée les graphiques de visualisation des spreads.
        """
        print("\n📈 Génération des graphiques...")
        
        # Graphique 1: Evolution des spreads
        fig, ax = plt.subplots(figsize=(14, 7))
        
        for emetteur in self.df['Emetteur'].unique():
            df_emetteur = self.df[self.df['Emetteur'] == emetteur]
            ax.plot(df_emetteur['Date'], df_emetteur['Spread (bps)'], 
                   marker='o', linewidth=2, markersize=4, label=emetteur)
        
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Spread CDS (bps)', fontsize=12, fontweight='bold')
        ax.set_title('Évolution des Spreads de Crédit (CDS 5Y)', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Format de date
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('/home/claude/spread_evolution.png', dpi=300, bbox_inches='tight')
        print("✅ Graphique 1 sauvegardé: spread_evolution.png")
        plt.close()
        
        # Graphique 2: Comparaison spreads actuels
        fig, ax = plt.subplots(figsize=(10, 6))
        
        current_spreads = []
        emetteurs = []
        
        for emetteur in self.df['Emetteur'].unique():
            df_emetteur = self.df[self.df['Emetteur'] == emetteur]
            current_spreads.append(df_emetteur['Spread (bps)'].iloc[-1])
            emetteurs.append(emetteur)
        
        colors = ['#2E86AB' if s < 150 else '#A23B72' if s < 250 else '#F18F01' 
                 for s in current_spreads]
        
        bars = ax.barh(emetteurs, current_spreads, color=colors, alpha=0.8)
        ax.set_xlabel('Spread CDS 5Y (bps)', fontsize=12, fontweight='bold')
        ax.set_title('Spreads de Crédit Actuels par Émetteur', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, axis='x', alpha=0.3)
        
        # Ajouter les valeurs sur les barres
        for i, (bar, value) in enumerate(zip(bars, current_spreads)):
            ax.text(value + 5, i, f'{value:.0f} bps', 
                   va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('/home/claude/spread_comparison.png', dpi=300, bbox_inches='tight')
        print("✅ Graphique 2 sauvegardé: spread_comparison.png")
        plt.close()
        
        # Graphique 3: Volatilité
        fig, ax = plt.subplots(figsize=(10, 6))
        
        volatilities = [self.stats[e]['Volatilité (%)'] for e in emetteurs]
        
        bars = ax.barh(emetteurs, volatilities, color='#E63946', alpha=0.7)
        ax.set_xlabel('Volatilité (%)', fontsize=12, fontweight='bold')
        ax.set_title('Volatilité des Spreads par Émetteur', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, axis='x', alpha=0.3)
        
        # Ajouter les valeurs
        for i, (bar, value) in enumerate(zip(bars, volatilities)):
            ax.text(value + 0.1, i, f'{value:.2f}%', 
                   va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('/home/claude/spread_volatility.png', dpi=300, bbox_inches='tight')
        print("✅ Graphique 3 sauvegardé: spread_volatility.png")
        plt.close()
    
    def generate_dashboard(self, output_file):
        """
        Génère un dashboard Excel avec statistiques et graphiques.
        
        Args:
            output_file (str): Chemin vers le fichier Excel de sortie
        """
        print(f"\n📋 Génération du dashboard Excel...")
        
        try:
            # Créer un writer Excel
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                
                # Onglet 1: Statistiques
                stats_df = pd.DataFrame(self.stats).T
                stats_df.index.name = 'Émetteur'
                stats_df = stats_df.round(2)
                stats_df.to_excel(writer, sheet_name='Statistiques')
                
                # Onglet 2: Données brutes
                self.df.to_excel(writer, sheet_name='Données', index=False)
                
                # Onglet 3: Analyse (graphiques seront ajoutés manuellement)
                summary_data = {
                    'Métrique': [
                        'Nombre d\'émetteurs',
                        'Période d\'analyse',
                        'Spread moyen du marché (bps)',
                        'Volatilité moyenne (%)',
                        'Date de génération'
                    ],
                    'Valeur': [
                        self.df['Emetteur'].nunique(),
                        f"{self.df['Date'].min().strftime('%Y-%m-%d')} à {self.df['Date'].max().strftime('%Y-%m-%d')}",
                        f"{self.df['Spread (bps)'].mean():.2f}",
                        f"{pd.Series([self.stats[e]['Volatilité (%)'] for e in self.stats]).mean():.2f}",
                        datetime.now().strftime('%Y-%m-%d %H:%M')
                    ]
                }
                
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Résumé', index=False)
            
            print(f"✅ Dashboard généré: {output_file}")
            
            # Instructions pour ajouter les graphiques
            print("\n📎 Pour finaliser le dashboard:")
            print("   1. Ouvrez le fichier Excel généré")
            print("   2. Les graphiques PNG sont disponibles dans le dossier")
            print("   3. Vous pouvez les insérer dans l'onglet 'Résumé'")
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {str(e)}")
            raise
    
    def run_analysis(self, output_file):
        """
        Execute l'analyse complète: charge données, calcule stats, crée graphs, génère dashboard.
        
        Args:
            output_file (str): Chemin vers le fichier Excel de sortie
        """
        print("="*60)
        print("CREDIT SPREAD ANALYZER")
        print("="*60)
        
        self.load_data()
        self.calculate_statistics()
        self.create_visualizations()
        self.generate_dashboard(output_file)
        
        print("\n" + "="*60)
        print("✅ ANALYSE TERMINÉE AVEC SUCCÈS")
        print("="*60)
        print(f"\nFichiers générés:")
        print(f"  • Dashboard Excel: {output_file}")
        print(f"  • Graphique 1: spread_evolution.png")
        print(f"  • Graphique 2: spread_comparison.png")
        print(f"  • Graphique 3: spread_volatility.png")


def main():
    """
    Fonction principale - Point d'entrée du programme.
    """
    # Configuration
    INPUT_FILE = '/home/claude/cds_data_sample.xlsx'
    OUTPUT_FILE = '/home/claude/Credit_Spread_Dashboard.xlsx'
    
    # Initialiser et exécuter l'analyse
    analyzer = CreditSpreadAnalyzer(INPUT_FILE)
    analyzer.run_analysis(OUTPUT_FILE)


if __name__ == "__main__":
    main()
