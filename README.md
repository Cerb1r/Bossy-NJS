## Site de l'ISPM: https://ispm-edu.com/

## Nom du groupe: 
    Bossy NJS

## Les membres du groupe:
    - ANDRIANIRINA Ny Ony Tantelinantenaina , ISAIA N15
    - RAKOTOMANANA Johariniaina Manalina , ISAIA N16
    - SANTATRINIAINA Nomena tsilavina , ISAIA N25

## Desciption du projet: 
L'objectif de ce projet est de concevoir une Intelligence Artificielle capable de jouer au Morpion en combinant l'apprentissage statistique et la logique algorithmique.

## Structure du repository:

📂 Morpion-IA-Hackathon/
├── 📂 models/                 
│   ├── 📄 best_model_draw.pkl  
│   └── 📄 best_model_wins.pkl  
├── 📂 ressources/             
│   └── 📄 dataset.csv          
├── 📄 app.py                  
├── 📄 generator.py            
├── 📄 main_game.py           
├── 📄 notebook.ipynb         
└── 📄 README.md               


## Résultats ML (Baseline vs Finale)
| Modèle | Accuracy | F1-Score |
| :--- | :--- | :--- |
| **Baseline** (Logist.) | 75.46% | 0.86 |
| **Final** (Hybride) | 92.15% | 0.94 |

## Analyse
* **Case Centrale :** Identifiée comme le pivot stratégique majeur via l'EDA.
* **Baseline :** Modèle linéaire biaisé, performant sur les victoires mais incapable de prédire les matchs nuls.
* **Hybride :** Combine l'intuition du Random Forest et la rigueur d'un algorithme Minimax pour bloquer les attaques humaines et saisir les victoires tactiques.

## Conclusion
Le projet démontre qu'une approche hybride surpasse largement les modèles statistiques purs en intégrant une vérification logique immédiate.



--------------------------------
 REPONSES AUX QUESTIONS
--------------------------------

## Q1 — Analyse des coefficients

- Cases influentes : Les coefficients les plus élevés (en valeur absolue) se trouvent sur la case centrale (index 4) et les quatre coins.

- Occupation : Une valeur 1 pour c4_x augmente fortement la probabilité de victoire de X.

- Cohérence : C’est cohérent avec la stratégie humaine : le centre est la case la plus stratégique car elle permet de compléter le plus grand nombre de lignes (4 au total).
--------------------------------


## Q2 — Déséquilibre des classes

- Équilibre : Non, le dataset est fortement déséquilibré. Les victoires de X sont très fréquentes, tandis que les matchs nuls (is_draw) sont rares en jeu parfait.

- Métrique : Le F1-Score.

- Pourquoi : L'Accuracy est trompeuse sur un dataset déséquilibré. Le F1-Score permet de s'assurer que le modèle détecte réellement les matchs nuls au lieu de simplement prédire "victoire" par facilité.
--------------------------------


## Q3 — Comparaison des deux modèles

- Meilleur score : Le classificateur x_wins obtient généralement de meilleurs résultats.

- Difficulté : Le match nul est plus difficile à apprendre car il dépend de l'échec de toutes les lignes de victoire, ce qui est une relation logique plus complexe qu'un simple alignement de 3 pions.

- Erreurs : Les modèles se trompent surtout en début de partie, lorsque le plateau est vide et que les possibilités futures sont trop nombreuses pour une simple analyse statistique.
--------------------------------
## Q4 — Mode hybride

- Différence : Oui, le mode Hybride est plus "robuste". Contrairement au mode IA-ML qui peut ignorer une menace directe, l'Hybride calcule les coups forcés.

- Pièges : Le joueur hybride évite mieux les pièges car il combine la tactique immédiate (vérification de victoire/défaite par algorithme) et la stratégie long terme (évaluation par le modèle ML).

## lien du video :
    https://www.facebook.com/share/v/1CddmfPrwG/