# Progestion 🚀

[![Langue](https://img.shields.io/badge/langue-Français-red.svg)](#)
[![Framework](https://img.shields.io/badge/Framework-Django%205.1-green.svg)](https://www.djangoproject.com/)
[![Licence](https://img.shields.io/badge/Licence-MIT-yellow.svg)](LICENSE)

**Progestion** est une solution moderne de gestion d'entreprise, conçue spécifiquement pour les petites et moyennes entreprises (TPE/PME). Elle simplifie les tâches administratives telles que la facturation, la gestion client et le suivi fiscal grâce à une interface élégante et réactive.

[English Version (Version Anglaise)](README.md)

---

## ✨ Fonctionnalités Clés

- 📑 **Facturation & Devis** : Créez, gérez et exportez facilement des factures professionnelles (Génération PDF via WeasyPrint).
- 👥 **CRM Clients & Fournisseurs** : Centralisez vos contacts, suivez vos interactions et gérez vos relations commerciales.
- 📦 **Gestion de Stock & Produits** : Suivez vos produits, vos niveaux de stock et vos fournisseurs.
- 💰 **Suivi des Transactions** : Surveillez vos flux financiers et l'historique complet de vos transactions.
- ⚖️ **Fiscalité & Conformité** : Module dédié pour le suivi des impôts et des obligations réglementaires.
- ⚡ **Stack Moderne** : Développé avec Django 5, HTMX pour des interactions dynamiques sans rechargement, et Tailwind CSS pour un design premium.

## 🛠️ Stack Technique

- **Backend** : Python 3.10+, Django 5.x
- **Frontend** : Tailwind CSS, HTMX
- **Traitement de Données** : Pandas, OpenPyXL
- **Génération PDF** : WeasyPrint
- **Base de Données** : SQLite (par défaut), PostgreSQL (recommandé pour la production)

## 🚀 Démarrage Rapide

### Prérequis

- Python 3.10+
- Node.js (pour Tailwind CSS)
- `pip` ou `poetry`

### Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/votre-utilisateur/Progestion.git
   cd Progestion/backend
   ```

2. **Configurer l'environnement virtuel** :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirment.txt
   ```

4. **Lancer les migrations** :
   ```bash
   python src/manage.py migrate
   ```

5. **Démarrer le serveur de développement** :
   ```bash
   python src/manage.py runserver
   ```

6. **Accéder à l'application** :
   Ouvrez [http://127.0.0.1:8000](http://127.0.0.1:8000) dans votre navigateur.

---

## 🤝 Contribuer

Nous accueillons les contributions avec plaisir ! Veuillez consulter notre guide [CONTRIBUTING.fr.md](CONTRIBUTING.fr.md) pour plus de détails sur la marche à suivre.

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus d'informations.

## 🛡️ Sécurité

Si vous découvrez une faille de sécurité, veuillez vous référer à notre politique [SECURITY.fr.md](SECURITY.fr.md).
