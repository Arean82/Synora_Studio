# Portail Web SaaS et passerelle multi-locataires (v9.0)

Ce répertoire héberge le portail d'applications Web, le standard de routage de base de données, les moteurs de sandboxing de locataire dynamique et les interfaces de gestion des clients SaaS.

## Structure du répertoire
- **`app.py`** : les routes de gestion du contrôleur d'application Flask principal, les authentifications JWT, les connexions des locataires, les flux de session et les points de terminaison REST.
- **`run_web.py`** : exécuteur de script standard qui importe l'instance `app` et lance la boucle du serveur.
- **`core/`** : modules d'assistance de base SaaS (par exemple `launcher.py`, `agent_manager.py`, `config_manager.py`, `tenant_db.py`).
- **`tenant_drivers/`** : Middleware orchestrant les isolations de schéma et les migrations de bases de données cloud pour les utilisateurs multi-tenants.
- **`static/` & `templates/`** : vues frontales, feuilles de style et écrans de tableau de bord purement HTML/CSS/JS.
- **`saas_docs/`** : Directives de fonctionnement de la plateforme et instructions administratives.

## Fichiers de configuration et d'empaquetage locaux
Pour prendre en charge la compilation modulaire découplée, ce répertoire contient ses propres fichiers d'empaquetage autonomes :
- **`web.spec`** : fichier de spécifications PyInstaller spécifique au packaging du portail Web SaaS.
- **`build.py`** : script de build Python local exécutant les commandes PyInstaller ciblant `web.spec`. (L'orchestrateur global se trouve dans `scripts/build.py`).
- **`file_version_info.txt`** : métadonnées au niveau du système d'exploitation définissant la version de l'exécutable (v9.0.0.0), les droits d'auteur et les descriptions.
- **`installer_script.iss`** : configuration Local Inno Setup pour packager l'application Web SaaS compilée.

## Notes d'architecture clés
- **Zéro surcharge d'interface graphique** : strictement isolé des composants PySide6 et Qt pour fonctionner efficacement sur des serveurs de production sans tête.
- **Micro-Gateway Routing** : délègue la génération intensive et l'intégration des requêtes à la couche « serveur/ » sous-jacente.

## Compilation exécutable
Pour compiler le binaire autonome « SaaS_Web_Portal.exe » à l'aide de PyInstaller :
```bash
pyinstaller web.spec
```