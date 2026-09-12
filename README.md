# darkdeku_e-com

Application e-commerce développée avec Django.

## Fonctionnalités

- Authentification (inscription, connexion, déconnexion) avec utilisateur personnalisé basé sur l’email.
- Catalogue produits avec catégories, marques (make) et tags.
- Fiches produit avec slug, image, prix, stock et statut actif/inactif.
- Panier utilisateur (ajout, suppression d’articles, vidage du panier).
- Gestion des commandes.
- Espace administrateur avec gestion des produits, catégories, marques, tags et utilisateurs.

## Stack technique

- Python 3
- Django 6
- PostgreSQL
- django-crispy-forms + crispy-bootstrap5

## Installation locale (détaillée)

### 1) Pré-requis

Avant de commencer, assurez-vous d’avoir :

- Python 3 installé
- `pip` disponible
- PostgreSQL installé et démarré

### 2) Récupérer le projet

```bash
git clone <url-du-repo>
cd darkdeku_e-com
```

### 3) Créer et activer un environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate
```

Sur Windows (PowerShell) :

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4) Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### 5) Préparer la base PostgreSQL

Créez une base de données PostgreSQL et un utilisateur ayant les droits sur cette base.

Exemple de valeurs à prévoir :

- nom de la base : `darkdeku_db`
- utilisateur : `darkdeku_user`
- mot de passe : `mot_de_passe`

### 6) Créer le fichier d’environnement `.env`

À la racine du projet, créez un fichier `.env` :

```env
SECRET_KEY=votre-cle-secrete-django
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=darkdeku_db
DB_USER=darkdeku_user
DB_PASSWORD=mot_de_passe
DB_HOST=localhost
DB_PORT=5432
```

### 7) Appliquer les migrations

```bash
python manage.py migrate
```

### 8) Créer un compte administrateur (recommandé)

```bash
python manage.py createsuperuser
```

### 9) Lancer le serveur de développement

```bash
python manage.py runserver
```

Puis ouvrez : `http://127.0.0.1:8000/`

## Routes principales

- `/` : accueil boutique
- `/register/`, `/login/`, `/logout/` : authentification
- `/cart/` : panier
- `/product/all/` : liste des produits
- `/dashboard/index` : tableau de bord administrateur

## Structure du projet

- `/E_com` : configuration Django (settings, urls, wsgi, asgi)
- `/store` : logique métier (modèles, formulaires, vues)
- `/templates` : templates HTML
- `/staticfiles` : assets statiques collectés

## Commandes utiles

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
