# Foresterie canadienne & produits dérivés du bois — Export

Maquette de démonstration, page unique. Bois d'œuvre résineux et feuillus,
panneaux, contreplaqué, OSB, bois d'ingénierie, produits de bois massif, bois
traité, pâte, papier, carton, biomasse et coproduits.

En ligne :
* français — https://anirudhatalmale6-alt.github.io/forest-demo/
* English — https://anirudhatalmale6-alt.github.io/forest-demo/en/

## Bilingue, et prouvé bilingue

Les 201 chaînes du jeu de données vivent dans `src/traductions.py`, apparié
**par index** depuis `data.py` : le français n'a jamais été retapé à la main,
donc aucune clé ne peut être fausse. `build.py` lève une erreur si une chaîne
n'a pas de traduction — la page anglaise ne peut pas se construire à moitié
traduite.

Et le test le vérifie sur la page rendue : il prend les 201 chaînes françaises
et exige qu'aucune ne survive dans la page anglaise. Deux exceptions, nommées
explicitement — une traduction identique au français (« Ontario »), et les
**noms de ports**, qui sont des noms propres. « Québec » désigne la province,
traduite en « Quebec », et la ville portuaire, conservée telle quelle.

## Trois axes, pas deux

Famille de produit × application × **niveau de transformation**.

Ce troisième axe n'est pas décoratif. L'acheteur de grumes et l'acheteur de
lamellé-collé ne sont pas la même personne, ne paient pas la même chose et ne
demandent pas les mêmes documents. Séparer matière première, produit
transformé et produit à valeur ajoutée, c'est séparer trois marchés qu'une
liste à plat mélange.

Chaque carte est une **catégorie**, pas une référence en stock, et déclare les
champs qu'un acheteur international exigera avant de coter : essence,
classement, taux d'humidité, type de collage, traitement, conditionnement,
unité de cotation, et le reste.

## Ce que la page n'affiche pas, volontairement

Le brief demandait des capacités d'approvisionnement. **Il n'y en a aucune.**
Pas un volume, pas un tonnage, pas un délai, pas un prix, pas une fréquence
d'expédition, aucune certification présentée comme détenue, aucune essence
annoncée disponible.

Sur une page d'export, un volume annoncé est la première chose qu'un acheteur
fait vérifier, et la première qui tue un dossier s'il est faux. La page dit
donc **quelle unité déclarer et sur quelle base**, jamais combien.

Les référentiels sont présentés comme des cases à remplir. Le test va plus
loin qu'une relecture : **aucun sigle de référentiel n'apparaît nulle part**
dans le document, donc aucun ne peut être lu comme un label affiché.

Les ports sont réels et donnés avec leur seule province et leur seule façade
maritime — des faits vérifiables en trente secondes. Un test refuse la page
si le tableau des ports contient ne serait-ce qu'un chiffre.

## Regénérer

```
cd src
python3 build.py ../index.html fr      # refuse de construire si une donnée est incohérente
python3 build.py ../en/index.html en   # ou si une traduction manque
python3 tests.py                       # 150 contrôles, les deux langues
```

### Contrôle négatif

Une suite qui n'a jamais échoué ne prouve rien. `tests.py` accepte le chemin
d'une page truquée :

```
python3 tests.py /chemin/page-truquee.html
```

Il sort alors en erreur si la page truquée **passe** — c'est l'inverse du mode
normal — et n'écrit aucune capture, pour qu'un contrôle ne puisse jamais
écraser une image livrable. Les dix règles interdisant volumes, tonnages,
prix, délais, pourcentages et sigles de certification ont toutes été
déclenchées de cette façon.
