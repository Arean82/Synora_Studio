# Moteur CLI de chat et de terminal sans tête

Ce répertoire implémente la boucle de discussion et la gestion des informations d'identification de l'interface de ligne de commande interactive (CLI), permettant aux développeurs d'interagir avec les fournisseurs LLM directement depuis le terminal.

## Structure du fichier
- **`auth.py`** : gère les entrées de clé API et les sessions d'authentification pour les clients CLI.
- **`engine.py`** : Le contexte d'exécution exécutant la boucle texte uniquement.
- **`models.py`** : Logique pour afficher et échanger les modèles actifs dans la CLI.
- **`worker.py`** : orchestre les morceaux de génération de streaming et le formatage d'impression.

## Utilisation
Exécutez la commande suivante à partir du répertoire racine pour accéder à la console CLI :
```bash
python bureau/main.py --cli
```
Remarque : Ce module est strictement exclu des environnements de déploiement de serveurs distants afin de minimiser les packages d'hébergement de production.