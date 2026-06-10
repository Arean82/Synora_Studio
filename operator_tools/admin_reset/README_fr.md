# Réinitialisation des informations d'identification d'administrateur universelles (v9.0)

Cet outil permet aux administrateurs de serveur de réinitialiser en toute sécurité les informations d'identification de l'administrateur principal dans tous les environnements.

## Fonctionnalités
- **Exécution bimode** :
  - **Mode GUI** : génère une boîte de dialogue d'assistant PySide6 haute fidélité pour les environnements de bureau locaux.
  - **Mode CLI/Headless** : contourne entièrement les dépendances de l'interface graphique en utilisant `--headless` ou `--cli`, ce qui le rend parfait pour les terminaux SSH distants, les scripts d'automatisation et les tâches cron.
- **Options de mot de passe dynamique** :
  - `--random-password` : génère un mot de passe alphanumérique sécurisé et aléatoire de 12 caractères.
  - `--custom-password "your_password"` : définit une chaîne de mot de passe spécifique et personnalisée.
  - La valeur par défaut est le mot de passe « admin » si aucune option n'est spécifiée.
- **Détection automatique du pilote** : lit automatiquement les informations de connexion et résout les paramètres du pilote à partir de `saas/config.ini` ou de l'environnement.

## Fichiers de configuration et d'empaquetage locaux
Pour prendre en charge la compilation modulaire découplée, ce répertoire contient ses propres fichiers d'empaquetage autonomes :
- **`reset_admin.spec`** : fichier de spécifications PyInstaller spécifique au packaging de l'outil de réinitialisation de l'administrateur.
- **`build.py`** : script de build Python local exécutant les commandes PyInstaller ciblant `reset_admin.spec`. (L'orchestrateur global se trouve dans `scripts/build.py`).
- **`file_version_info.txt`** : métadonnées au niveau du système d'exploitation définissant la version de l'exécutable (v9.0.0.0), les droits d'auteur et les descriptions.
- **`installer_script.iss`** : configuration locale d'Inno Setup pour empaqueter l'outil de réinitialisation de l'administrateur compilé.

## Exécution

### Mode CLI/sans tête :
```bash
python reset_admin.py --headless
```

### Spécifications de PyInstaller
Pour compiler le binaire autonome `Admin_Reset` à l'aide de PyInstaller :
```bash
pyinstaller reset_admin.spec
```
Cela isole la fonctionnalité de réinitialisation de mot de passe des distributions client publiques, garantissant ainsi la sécurité des clés administratives.