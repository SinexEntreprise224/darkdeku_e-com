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

## Installation locale

1. Cloner le dépôt.
2. Créer et activer un environnement virtuel.
3. Installer les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

4. Créer un fichier `.env` à la racine du projet avec :

   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost

   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. Appliquer les migrations :

   ```bash
   python manage.py migrate
   ```

6. Créer un superutilisateur (optionnel mais recommandé) :

   ```bash
   python manage.py createsuperuser
   ```

7. Lancer le serveur :

   ```bash
   python manage.py runserver
   ```

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
