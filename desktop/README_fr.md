# Interface graphique d'administration locale et client de bureau (v9.0)

Ce répertoire héberge l'interface utilisateur graphique autonome de PySide6, fonctionnant comme le panneau « Mission Control » de l'administrateur local.

## Structure du répertoire
- **`main.py`** : point d'entrée orchestrant les paramètres de démarrage de l'application native, les gestionnaires CLI et le chargement des limites de la fenêtre.
- **`ui/`** : contrôleurs de vue de fenêtre PySide6, boucles de thread, liaisons de widgets personnalisées et gestionnaires d'événements.
- **`ui_designer/`** : schémas de description Pure XML `.ui` générés à partir de Qt Designer.
- **`headless/`** : invites de discussion CLI locales et boucles de terminal en arrière-plan.

## Fichiers de configuration et d'empaquetage locaux
Pour prendre en charge la compilation modulaire découplée, ce répertoire contient ses propres fichiers d'empaquetage autonomes :
- **`desktop.spec`** : fichier de spécifications PyInstaller spécifique au packaging du client Desktop.
- **`build.py`** : script de build Python local exécutant les commandes PyInstaller ciblant `desktop.spec`. (L'orchestrateur global se trouve dans `scripts/build.py`).
- **`file_version_info.txt`** : métadonnées au niveau du système d'exploitation définissant la version de l'exécutable (v9.0.0.0), les droits d'auteur et les descriptions.
- **`installer_script.iss`** : configuration locale d'Inno Setup pour empaqueter l'application de bureau compilée.

## Principales fonctionnalités
- **Bypass Control** : configure directement les configurations de stockage actif, les bases de données et les fournisseurs LLM localement sans s'appuyer sur la passerelle API publique.
- **SSH Tunnel Manager** : établit instantanément des connexions de transfert SSH/VPN cryptées vers des clusters cloud distants (Redis, Postgres, API Godmode).
- **Zero SaaS Packaging Bloat** : se compile proprement à l'aide de PyInstaller en ignorant strictement les actifs de routage `web/`.

## Compilation exécutable
Pour compiler le binaire autonome « Synora_Studio.exe » à l'aide de PyInstaller :
```bash
pyinstaller bureau.spec
```