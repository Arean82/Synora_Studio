# Programme d'installation du démon d'exploitation et de service Companion (v9.0)

Companion Operation est un utilitaire d'administration bimode qui facilite la migration de la plate-forme, les déplacements de données locales, les sauvegardes de bases de données, la configuration réseau/Web et la génération de démons de services système.

## Fonctionnalités
- **Relocalisation de base de données** : migre de manière autonome tous les schémas et données des environnements d'amorçage locaux (Turso/libSQL SQLite) vers les clusters d'entreprise de production (PostgreSQL).
- **Configuration réseau/Web** : mettez à jour par programme la liaison de l'hôte et les ports pour le portail Web SaaS via l'interface graphique ou la CLI.
- **Génération de services automatisée (installateur Daemon)** :
  - Génère des configurations de démon d'arrière-plan natives.
  - **Windows (NSSM)** : génère un script PowerShell (`install_<name>.ps1`) qui télécharge automatiquement NSSM, configure l'exécution, verrouille les autorisations et installe l'API en tant que service Windows.
  - **Linux (systemd)** : génère un fichier `.service` et un script bash automatisé (`install_<name>.sh`) qui configure systemd, configure les utilisateurs de service dédiés et configure le renforcement de la sécurité (tel que `PrivateTmp`, `ProtectHome` et les fonctionnalités restreintes).
- **Exécution bimode** :
  - **Mode GUI** : panneau de l'assistant étape par étape de PySide6.
  - **Mode CLI** : Assistant de terminal interactif ou actions scriptables (par exemple `--action=backup`).

## Fichiers de configuration et d'empaquetage locaux
Pour prendre en charge la compilation modulaire découplée, ce répertoire contient ses propres fichiers d'empaquetage autonomes :
- **`companion_operation.spec`** : fichier de spécifications PyInstaller spécifique au packaging de l'outil Companion Operation.
- **`build.py`** : script de build Python local exécutant les commandes PyInstaller ciblant `companion_operation.spec`. (L'orchestrateur global se trouve dans `scripts/build.py`).
- **`file_version_info.txt`** : métadonnées au niveau du système d'exploitation définissant la version de l'exécutable (v9.0.0.0), les droits d'auteur et les descriptions.
- **`installer_script.iss`** : configuration de Local Inno Setup pour empaqueter l'outil Companion Operation compilé.

## Exécution

### Mode CLI :
```bash
python compagnon_opération.py --headless
```

### Spécifications de PyInstaller
Pour compiler le binaire autonome `Companion_Operation` à l'aide de PyInstaller :
```bash
pyinstaller compagnon_opération.spec
```
Cela garantit que les outils des opérateurs privés sont compilés séparément du groupe d'utilisateurs de bureau principal.