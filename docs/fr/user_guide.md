# 🖥️ Guide Utilisateur et Manuel Opérateur

Procédure pas à pas pour l'exploitation de l'interface graphique de **SFusion Mapper**.

⬅️ [Hub de Documentation](README.md) | 🏛️ [Architecture](architecture.md) | 🔄 [Flux de Travail](system_workflow.md)

---

## 1. Utilisation Pas à Pas

1. **Ouvrir la Carte** : Charger le réseau SUMO via le bouton **Ouvrir Carte** (`Ctrl+M`).
2. **Ajouter une Source** : Sélectionner un dossier contenant des fichiers de capteurs.
3. **Associer** : Lier la source en cliquant sur une voie de la carte (les deux sens sont automatiquement appariés) ou définir comme Global.
4. **Valider le Schéma** : Contrôler les colonnes détectées par l'IA dans le panneau latéral droit et attribuer un nom de rue usuel.
5. **Générer le Dataset** : Cliquer sur **Générer Dataset** pour exporter le fichier `.parquet`.
6. **Sauvegarder le Projet** : Enregistrer la session sous `.sfm.json` pour la recharger ultérieurement.

---

## 🔗 Liens Utiles
* [Hub de Documentation](README.md)
* [Flux de Travail](system_workflow.md)
* [Modèles de Données](data_models.md)
