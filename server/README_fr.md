# Moteur central sans tête (serveur backend) (v9.0)

Ce répertoire héberge la logique principale du backend, l'orchestration du runtime de l'IA, les interfaces de bases de données vectorielles et les tâches en arrière-plan. Il est strictement **indépendant de l'interface utilisateur** et ne contient aucune définition d'interface utilisateur de bureau ou de route Web.

## Structure du répertoire
- **`logic/`** : routeur client LLM unifié (Google/NVIDIA/OpenAI/Custom), services d'intégration, adaptateurs de connexion à la base de données (PostgreSQL/Turso) et files d'attente de travail de discussion en arrière-plan.
- **`utils/`** : aides aux paramètres partagés, résolveurs d'informations d'identification sécurisés, configurations de chemin de stockage et constantes à l'échelle du système.
- **`workers/`** : consommateurs de tâches asynchrones exécutant des intégrations vectorielles, le suivi de l'utilisation des jetons, l'ingestion des journaux en arrière-plan et l'indexation.
- **`resources/`** : actifs de métadonnées statiques tels que le schéma des fournisseurs et les manifestes d'enregistrement de modèle.
- **`run_server.py`** : exécute l'API de routage du serveur autonome (port 5000) pour les passerelles locales hors ligne.

## Fichiers de configuration et d'empaquetage locaux
Pour prendre en charge la compilation modulaire découplée, ce répertoire contient ses propres fichiers d'empaquetage autonomes :
- **`server.spec`** : fichier de spécifications PyInstaller spécifique au packaging du serveur API.
- **`build.py`** : script de build Python local exécutant les commandes PyInstaller ciblant `server.spec`. (L'orchestrateur global se trouve dans `scripts/build.py`).
- **`file_version_info.txt`** : métadonnées au niveau du système d'exploitation définissant la version de l'exécutable (v9.0.0.0), les droits d'auteur et les descriptions.
- **`installer_script.iss`** : configuration Local Inno Setup pour empaqueter l'application serveur compilée.

## Fonctionnalités
- **Intelligent LLM Router** : Interface polymorphe résolvant les requêtes de manière dynamique.
- **RAG découplé** : mise en cache des vecteurs directement à l'aide d'utilitaires d'intégration découplés.
- **Secure Storage Gateway** : intègre le démarrage de la base de données Turso avec des basculements dynamiques.

## Compilation exécutable
Pour compiler le binaire autonome « API_Server.exe » à l'aide de PyInstaller :
```bash
serveur pyinstaller.spec
```