# -*- coding: utf-8 -*-
"""Page unique « Foresterie canadienne & produits dérivés du bois — Export ».

BRIEF DU CLIENT (tableur, ligne 1) : « Page dédiée à la foresterie canadienne
et à l'offre destinée aux marchés internationaux : bois d'oeuvre, bois de
construction, panneaux, contreplaqué, OSB, pâte et papier, produits de bois
massif, bois d'ingénierie, produits transformés, biomasse et autres dérivés du
bois. Présentation des catégories de produits, capacités d'approvisionnement,
normes et certifications, marchés d'exportation, logistique, ports et services
de mise en relation avec les acheteurs internationaux. »

CE QUI EST REEL ICI, ET CE QUI N'Y EST PAS.

REEL : les ports. Ce sont de vrais ports canadiens, avec leur province et leur
facade maritime — des faits geographiques qu'un acheteur peut verifier en
trente secondes. Les intitules de certifications sont de vrais referentiels
existants ; ils sont presentes comme des CASES A REMPLIR, pas comme des
certificats detenus.

ABSENT VOLONTAIREMENT — et c'est la partie qui compte sur une page d'export :

  - AUCUNE CAPACITE D'APPROVISIONNEMENT CHIFFREE. Le brief la demande. Je ne
    l'ecris pas : je n'ai aucun volume mesure, aucun contrat, aucune scierie
    derriere moi. Annoncer « 50 000 m3 par mois » sur une page d'export, c'est
    la premiere chose qu'un acheteur serieux fera verifier — et la premiere
    qui tuera le dossier si elle est fausse. La page dit donc QUELLE unite
    declarer et sur quelle base, pas combien.
  - AUCUN TONNAGE, aucun trafic, aucun delai de transit, aucune frequence de
    depart pour les ports. Le nom, la province et la facade suffisent et sont
    verifiables ; le reste change tous les trimestres.
  - AUCUNE CERTIFICATION PRESENTEE COMME DETENUE. « FSC » apparait comme un
    champ a declarer, jamais comme un label affiche.
  - AUCUN PRIX, aucun incoterm chiffre, aucune parite de change.
  - AUCUNE ESSENCE presentee comme disponible en stock.

Tous les compteurs de la page sont DERIVES de ces listes.
"""

MARQUE = 'FORESTERIE CANADIENNE — EXPORT'
TITRE = 'catalogue export bois et produits dérivés'

# Palette : le client a demande « une couleur » pour la foresterie canadienne.
# Rouge canadien en accent, sur un blanc chaud. Le vert forestier tres pale de
# la premiere version ne se voyait pas — un accent doit se voir.
# TOUS LES CONTRASTES SONT MESURES par tests.py, jamais estimes : le rouge est
# la couleur ou l'on passe le plus facilement sous le seuil sans s'en rendre
# compte, parce qu'il PARAIT sombre alors que sa luminance est moyenne.
FOND     = '#f7f5f4'
CARTE    = '#ffffff'
LIGNE    = '#e4dedd'
ENCRE    = '#1b1210'
TEXTE    = '#40332f'
MUET     = '#655551'
ACCENT   = '#b01f24'
ACCENT_D = '#8c171b'

# ---------------------------------------------------------------------------
# LES FAMILLES DE PRODUITS. Reprises du brief, dans son ordre, completees des
# categories qu'il cite sans les nommer (« autres dérivés du bois »).
# ---------------------------------------------------------------------------
FAMILLES = [
    ('grumes',     'Grumes, copeaux et matière première'),
    ('resineux',   'Bois d’œuvre résineux'),
    ('feuillus',   'Bois feuillus et bois d’apparence'),
    ('panneaux',   'Panneaux dérivés du bois'),
    ('ingenierie', 'Bois d’ingénierie et systèmes structuraux'),
    ('massif',     'Produits de bois massif et transformés'),
    ('traites',    'Bois traité et préservé'),
    ('pate',       'Pâte, papier et carton'),
    ('biomasse',   'Biomasse et coproduits'),
]

# ---------------------------------------------------------------------------
# LE NIVEAU DE TRANSFORMATION. C'est un vrai axe commercial : l'acheteur de
# matiere premiere et l'acheteur de produit fini ne sont pas la meme personne,
# ne paient pas la meme chose et ne demandent pas les memes documents.
# ---------------------------------------------------------------------------
NIVEAUX = [
    ('primaire',  'Matière première et produit primaire'),
    ('secondaire', 'Produit transformé (séché, classé, usiné)'),
    ('valeur',    'Produit à valeur ajoutée'),
]

# ---------------------------------------------------------------------------
# LES APPLICATIONS. Deuxieme axe de filtrage.
# ---------------------------------------------------------------------------
APPLICATIONS = [
    ('residentiel',  'Construction résidentielle'),
    ('nonresid',     'Construction non résidentielle et bois massif'),
    ('coffrage',     'Coffrage et travaux'),
    ('emballage',    'Emballage, palettes et caisserie'),
    ('ameublement',  'Ameublement et agencement intérieur'),
    ('exterieur',    'Revêtement et aménagement extérieur'),
    ('papeterie',    'Papeterie, hygiène et emballage papier'),
    ('energie',      'Énergie et chauffage'),
    ('industrie',    'Industrie et seconde transformation'),
]

# ---------------------------------------------------------------------------
# LA GRILLE DE CHAMPS. Des NOMS DE CHAMPS a renseigner, jamais des valeurs.
# ---------------------------------------------------------------------------
CHAMPS = [
    ('essence',    'Essence ou mélange d’essences'),
    ('classement', 'Classement (grade)'),
    ('structural', 'Classement structural et marquage'),
    ('dimensions', 'Dimensions nominales'),
    ('longueurs',  'Longueurs disponibles'),
    ('humidite',   'Taux d’humidité'),
    ('sechage',    'Mode de séchage'),
    ('collage',    'Type de collage et classe d’exposition'),
    ('surface',    'État de surface et finition'),
    ('traitement', 'Traitement de préservation'),
    ('phyto',      'Traitement phytosanitaire à l’export'),
    ('certif',     'Certification forestière déclarée'),
    ('densite',    'Masse volumique'),
    ('durabilite', 'Durabilité naturelle'),
    ('granulo',    'Granulométrie'),
    ('cendres',    'Teneur en cendres et en humidité'),
    ('grammage',   'Grammage et laize'),
    ('blancheur',  'Blancheur et type de pâte'),
    ('condition',  'Conditionnement et unité de vente'),
    ('tolerance',  'Tolérances dimensionnelles'),
    ('origine',    'Province et région d’origine'),
    ('unite',      'Unité de cotation'),
]

# ---------------------------------------------------------------------------
# LES CATEGORIES.
#   (famille, niveau, nom, [applications], description, [champs])
# ---------------------------------------------------------------------------
CATEGORIES = [

    # --- Grumes, copeaux et matiere premiere -------------------------------
    ('grumes', 'primaire', 'Grumes résineuses',
     ['industrie', 'nonresid'],
     'Bois rond résineux destiné au sciage ou au déroulage. Le classement de '
     'la grume et la région d’origine décident de ce qu’on peut en tirer, bien '
     'avant le prix au mètre cube.',
     ['essence', 'classement', 'dimensions', 'longueurs', 'origine', 'phyto', 'certif', 'unite']),

    ('grumes', 'primaire', 'Grumes feuillues',
     ['industrie', 'ameublement'],
     'Bois rond feuillu pour sciage, tranchage ou déroulage. Marché où la '
     'qualité de la bille commande tout : une même essence couvre plusieurs '
     'usages sans rapport entre eux.',
     ['essence', 'classement', 'dimensions', 'longueurs', 'origine', 'phyto', 'certif', 'unite']),

    ('grumes', 'primaire', 'Copeaux de bois industriels',
     ['papeterie', 'industrie'],
     'Copeaux destinés à la fabrication de pâte ou de panneaux. Se négocient '
     'sur la granulométrie et la propreté, pas sur l’essence seule.',
     ['essence', 'granulo', 'humidite', 'densite', 'condition', 'origine', 'unite']),

    ('grumes', 'primaire', 'Sciures, rabotures et poussières',
     ['papeterie', 'energie', 'industrie'],
     'Coproduits de scierie repris en panneaux, en litière ou en énergie. '
     'Volume important, valeur unitaire faible : la logistique décide de la '
     'rentabilité.',
     ['granulo', 'humidite', 'densite', 'cendres', 'condition', 'origine', 'unite']),

    ('grumes', 'primaire', 'Écorces',
     ['energie', 'exterieur'],
     'Écorce en vrac ou criblée, pour combustion, paillage horticole ou '
     'substrat. Produit saisonnier dont l’humidité varie beaucoup.',
     ['granulo', 'humidite', 'cendres', 'densite', 'condition', 'origine', 'unite']),

    # --- Bois d'oeuvre resineux --------------------------------------------
    ('resineux', 'secondaire', 'Bois de construction SPF',
     ['residentiel', 'coffrage', 'emballage'],
     'Le produit d’export canadien par excellence : épinette, pin et sapin '
     'vendus en mélange. Séché, raboté, classé et marqué — c’est le marquage '
     'qui autorise l’usage structural sur le marché de destination.',
     ['essence', 'classement', 'structural', 'dimensions', 'longueurs',
      'humidite', 'sechage', 'certif', 'condition', 'unite']),

    ('resineux', 'secondaire', 'Douglas et mélèze',
     ['nonresid', 'residentiel', 'exterieur'],
     'Résineux à haute résistance mécanique, recherchés pour la charpente '
     'apparente et les grandes portées. Aspect et stabilité comptent autant '
     'que la classe de résistance.',
     ['essence', 'classement', 'structural', 'dimensions', 'longueurs',
      'humidite', 'surface', 'durabilite', 'certif']),

    ('resineux', 'secondaire', 'Pruche de l’Ouest',
     ['nonresid', 'ameublement', 'industrie'],
     'Résineux de l’Ouest canadien, apprécié pour son homogénéité et sa '
     'finition. Débouchés en menuiserie industrielle et en aménagement.',
     ['essence', 'classement', 'dimensions', 'longueurs', 'humidite',
      'surface', 'certif', 'origine']),

    ('resineux', 'secondaire', 'Cèdre rouge de l’Ouest',
     ['exterieur', 'residentiel'],
     'Essence de référence pour le bardage, la terrasse et le mobilier '
     'extérieur, en raison de sa durabilité naturelle sans traitement. '
     'Produit d’image : l’aspect se contractualise.',
     ['essence', 'classement', 'dimensions', 'longueurs', 'humidite',
      'surface', 'durabilite', 'certif', 'tolerance']),

    ('resineux', 'secondaire', 'Pin blanc et pin rouge',
     ['ameublement', 'residentiel', 'industrie'],
     'Pins de l’Est, en menuiserie, moulure et ameublement. Le classement '
     'porte sur les nœuds et l’aspect plus que sur la mécanique.',
     ['essence', 'classement', 'dimensions', 'longueurs', 'humidite',
      'sechage', 'surface', 'certif']),

    ('resineux', 'secondaire', 'Bois classé par machine',
     ['residentiel', 'nonresid'],
     'Sciages dont la résistance est mesurée pièce par pièce plutôt '
     'qu’estimée visuellement. Demandé dès que le calcul de structure serre.',
     ['essence', 'structural', 'classement', 'dimensions', 'longueurs',
      'humidite', 'densite', 'certif']),

    ('resineux', 'primaire', 'Sciages verts et bois de palette',
     ['emballage', 'coffrage'],
     'Sciages non séchés, destinés à la palette, à la caisserie et au '
     'coffrage. À l’export, le traitement phytosanitaire de l’emballage est '
     'le vrai point bloquant.',
     ['essence', 'classement', 'dimensions', 'longueurs', 'humidite',
      'phyto', 'condition', 'unite']),

    ('resineux', 'secondaire', 'Bois de coffrage et étaiement',
     ['coffrage'],
     'Planches, madriers et bois d’échafaudage pour le chantier. Produit '
     'consommable : la régularité des sections prime sur la finition.',
     ['essence', 'classement', 'dimensions', 'longueurs', 'humidite',
      'tolerance', 'condition']),

    # --- Feuillus -----------------------------------------------------------
    ('feuillus', 'secondaire', 'Érable',
     ['ameublement', 'residentiel', 'industrie'],
     'Feuillu dur de référence du Canada, en ameublement, plancher et '
     'agencement. Le tri sur la couleur de l’aubier fait une différence de '
     'prix considérable.',
     ['essence', 'classement', 'dimensions', 'longueurs', 'humidite',
      'sechage', 'surface', 'densite', 'certif']),

    ('feuillus', 'secondaire', 'Chêne rouge et chêne blanc',
     ['ameublement', 'residentiel', 'industrie'],
     'Deux marchés distincts sous un même nom : le chêne blanc et le chêne '
     'rouge ne vont ni aux mêmes clients ni aux mêmes usages. À distinguer sur '
     'la fiche, jamais à regrouper.',
     ['essence', 'classement', 'dimensions', 'longueurs', 'humidite',
      'sechage', 'surface', 'densite', 'durabilite', 'certif']),

    ('feuillus', 'secondaire', 'Bouleau jaune et bouleau blanc',
     ['ameublement', 'industrie'],
     'Feuillus de l’Est utilisés en placage, contreplaqué et composants '
     'd’ameublement. Sensibles au séchage : le mode de séchage se documente.',
     ['essence', 'classement', 'dimensions', 'longueurs', 'humidite',
      'sechage', 'surface', 'densite']),

    ('feuillus', 'secondaire', 'Merisier et cerisier',
     ['ameublement'],
     'Bois d’apparence pour mobilier et agencement haut de gamme. Marché de '
     'niche où l’homogénéité de teinte d’un lot à l’autre est le vrai sujet.',
     ['essence', 'classement', 'dimensions', 'longueurs', 'humidite',
      'sechage', 'surface', 'certif']),

    ('feuillus', 'secondaire', 'Frêne',
     ['ameublement', 'industrie', 'residentiel'],
     'Feuillu dur nerveux, en mobilier, manches et agencement. '
     'L’approvisionnement dépend fortement de la région d’origine.',
     ['essence', 'classement', 'dimensions', 'longueurs', 'humidite',
      'surface', 'densite', 'origine']),

    ('feuillus', 'primaire', 'Peuplier et tremble',
     ['emballage', 'industrie', 'papeterie'],
     'Feuillus tendres, en panneaux, emballage léger et pâte. Volume élevé, '
     'exigences d’aspect faibles.',
     ['essence', 'classement', 'dimensions', 'humidite', 'densite',
      'condition', 'origine', 'unite']),

    ('feuillus', 'valeur', 'Placages et bois tranchés',
     ['ameublement', 'industrie'],
     'Feuilles de placage tranchées ou déroulées pour l’agencement et le '
     'panneau plaqué. Le suivi par bille est ce qui permet d’assortir un '
     'chantier entier.',
     ['essence', 'classement', 'dimensions', 'tolerance', 'humidite',
      'surface', 'condition', 'certif']),

    # --- Panneaux -----------------------------------------------------------
    ('panneaux', 'secondaire', 'Contreplaqué résineux',
     ['residentiel', 'coffrage', 'nonresid'],
     'Panneaux structuraux pour plancher, mur et toiture. Le type de collage '
     'décide de l’exposition admissible ; c’est le premier champ que demande '
     'un bureau de contrôle.',
     ['essence', 'dimensions', 'tolerance', 'collage', 'structural',
      'surface', 'humidite', 'certif', 'condition']),

    ('panneaux', 'secondaire', 'Contreplaqué de bouleau',
     ['ameublement', 'industrie'],
     'Panneau à plis fins pour l’agencement, le mobilier et l’industrie. '
     'Vendu sur l’aspect des faces, codifié par un classement à deux lettres.',
     ['essence', 'classement', 'dimensions', 'tolerance', 'collage',
      'surface', 'condition', 'certif']),

    ('panneaux', 'secondaire', 'Panneau à copeaux orientés (OSB)',
     ['residentiel', 'coffrage', 'emballage'],
     'Alternative dominante au contreplaqué en construction légère. Le '
     'comportement à l’humidité et l’épaisseur commandée doivent être fixés '
     'avec le marché de destination.',
     ['dimensions', 'tolerance', 'collage', 'structural', 'humidite',
      'densite', 'certif', 'condition']),

    ('panneaux', 'secondaire', 'Panneau de particules',
     ['ameublement', 'industrie'],
     'Panneau de base de l’ameublement, brut ou surfacé. Le dégagement de '
     'formaldéhyde est un champ réglementaire à déclarer selon le marché.',
     ['dimensions', 'tolerance', 'collage', 'densite', 'surface',
      'humidite', 'condition']),

    ('panneaux', 'secondaire', 'MDF et panneau de fibres',
     ['ameublement', 'industrie'],
     'Panneau de fibres pour usinage, laquage et moulure. Se choisit sur la '
     'densité et la tenue de l’arête usinée.',
     ['dimensions', 'tolerance', 'densite', 'collage', 'surface',
      'humidite', 'condition']),

    ('panneaux', 'valeur', 'Panneaux lamellés sur chant',
     ['ameublement', 'nonresid'],
     'Plateaux massifs collés à partir de lamelles, pour plans de travail, '
     'marches et agencement. Produit de finition : l’aboutage visible se '
     'négocie.',
     ['essence', 'dimensions', 'tolerance', 'collage', 'surface',
      'humidite', 'certif']),

    ('panneaux', 'secondaire', 'Panneaux de fibres isolants',
     ['residentiel', 'nonresid'],
     'Panneaux de fibre de bois pour l’isolation et le pare-intempérie. '
     'Croissance portée par la construction bas carbone.',
     ['dimensions', 'tolerance', 'densite', 'humidite', 'certif', 'condition']),

    # --- Bois d'ingenierie --------------------------------------------------
    ('ingenierie', 'valeur', 'Lamellé-collé',
     ['nonresid', 'residentiel'],
     'Poutres et poteaux collés pour grandes portées et charpente apparente. '
     'Produit fabriqué sur plan : les longueurs et les cintrages se valident '
     'avant lancement.',
     ['essence', 'structural', 'dimensions', 'longueurs', 'collage',
      'surface', 'humidite', 'certif', 'tolerance']),

    ('ingenierie', 'valeur', 'Bois lamellé-croisé (CLT)',
     ['nonresid'],
     'Panneaux massifs porteurs pour la construction bois de moyenne et '
     'grande hauteur. C’est le produit qui a rouvert le marché du bâtiment '
     'non résidentiel au bois.',
     ['essence', 'structural', 'dimensions', 'longueurs', 'collage',
      'surface', 'humidite', 'certif', 'tolerance']),

    ('ingenierie', 'valeur', 'Bois de placage stratifié (LVL)',
     ['residentiel', 'nonresid'],
     'Poutres et linteaux à performance homogène, sans les défauts d’une '
     'pièce massive. Se substitue au sciage là où le calcul est serré.',
     ['essence', 'structural', 'dimensions', 'longueurs', 'collage',
      'densite', 'humidite', 'certif']),

    ('ingenierie', 'valeur', 'Poutrelles en I',
     ['residentiel'],
     'Solives de plancher et chevrons composites, légers et longs. Se '
     'commandent coupées à longueur avec le plan de plancher.',
     ['structural', 'dimensions', 'longueurs', 'collage', 'tolerance',
      'humidite', 'certif']),

    ('ingenierie', 'valeur', 'Fermes et composants préfabriqués',
     ['residentiel', 'nonresid'],
     'Fermes de toit et murs préfabriqués, dessinés puis fabriqués sur '
     'commande. La valeur est dans le bureau d’études autant que dans le bois.',
     ['structural', 'dimensions', 'longueurs', 'tolerance', 'humidite',
      'certif', 'condition']),

    ('ingenierie', 'valeur', 'Panneaux structuraux isolants',
     ['residentiel', 'nonresid'],
     'Panneaux sandwich associant peau structurale et isolant. Livrés '
     'préusinés selon le calepinage du projet.',
     ['dimensions', 'tolerance', 'collage', 'densite', 'structural',
      'certif', 'condition']),

    ('ingenierie', 'valeur', 'Poteaux et pièces de forte section',
     ['nonresid', 'exterieur'],
     'Pièces massives ou reconstituées de grande section, en charpente '
     'apparente et ouvrage extérieur. Séchage et fentes de retrait se '
     'documentent explicitement.',
     ['essence', 'structural', 'dimensions', 'longueurs', 'humidite',
      'sechage', 'durabilite', 'surface']),

    # --- Bois massif et produits transformes --------------------------------
    ('massif', 'valeur', 'Planchers de bois franc',
     ['residentiel', 'ameublement'],
     'Lames massives ou contrecollées, brutes ou finies en usine. Le taux '
     'd’humidité à la livraison est la première cause de litige à l’export.',
     ['essence', 'classement', 'dimensions', 'longueurs', 'humidite',
      'surface', 'tolerance', 'certif', 'condition']),

    ('massif', 'valeur', 'Lambris et revêtements muraux',
     ['residentiel', 'ameublement', 'exterieur'],
     'Profilés de parement intérieur et extérieur. Le profil d’assemblage se '
     'fixe avec l’acheteur : il n’est pas normalisé d’un marché à l’autre.',
     ['essence', 'classement', 'dimensions', 'longueurs', 'humidite',
      'surface', 'tolerance', 'durabilite']),

    ('massif', 'valeur', 'Moulures, plinthes et boiseries',
     ['residentiel', 'ameublement'],
     'Profilés décoratifs massifs ou aboutés, bruts, apprêtés ou finis. '
     'Fabrication sur outillage : le profil exact se valide sur échantillon.',
     ['essence', 'classement', 'dimensions', 'longueurs', 'surface',
      'humidite', 'tolerance', 'condition']),

    ('massif', 'valeur', 'Bois abouté et collé',
     ['ameublement', 'residentiel', 'industrie'],
     'Pièces reconstituées par aboutage, plus stables et mieux valorisées que '
     'la pièce d’origine. Le type de colle conditionne l’usage final.',
     ['essence', 'dimensions', 'longueurs', 'collage', 'humidite',
      'surface', 'tolerance', 'certif']),

    ('massif', 'valeur', 'Composants d’ameublement',
     ['ameublement', 'industrie'],
     'Pieds, montants, tiroirs et pièces usinées livrées prêtes à assembler. '
     'Marché de sous-traitance : le plan et la tolérance sont le contrat.',
     ['essence', 'dimensions', 'tolerance', 'surface', 'humidite',
      'condition', 'certif']),

    ('massif', 'valeur', 'Plans de travail et panneaux collés',
     ['ameublement', 'residentiel'],
     'Plateaux massifs pour cuisine, mobilier et agencement, bruts ou huilés. '
     'Se vendent au format fini, découpe comprise.',
     ['essence', 'dimensions', 'tolerance', 'collage', 'surface',
      'humidite', 'condition']),

    ('massif', 'valeur', 'Menuiseries extérieures en bois',
     ['residentiel', 'nonresid', 'exterieur'],
     'Portes, fenêtres et volets en bois ou bois-aluminium. Produit '
     'réglementé côté performance thermique sur le marché de destination.',
     ['essence', 'dimensions', 'tolerance', 'surface', 'traitement',
      'durabilite', 'humidite', 'certif']),

    # --- Bois traite --------------------------------------------------------
    ('traites', 'valeur', 'Bois traité sous pression',
     ['exterieur', 'residentiel', 'coffrage'],
     'Sciages imprégnés pour terrasse, structure extérieure et ouvrage en '
     'contact avec le sol. Le produit de traitement admis varie selon le pays '
     'importateur — à vérifier avant expédition, pas après.',
     ['essence', 'traitement', 'classement', 'dimensions', 'longueurs',
      'humidite', 'durabilite', 'certif', 'condition']),

    ('traites', 'valeur', 'Bois thermotraité',
     ['exterieur', 'ameublement'],
     'Bois stabilisé et rendu durable par la chaleur, sans produit chimique. '
     'Alternative demandée là où les traitements classiques sont restreints.',
     ['essence', 'traitement', 'dimensions', 'longueurs', 'humidite',
      'densite', 'durabilite', 'surface']),

    ('traites', 'valeur', 'Poteaux, traverses et pieux',
     ['exterieur', 'industrie'],
     'Bois rond ou équarri traité pour les réseaux, la voie ferrée et '
     'l’agriculture. Marché de spécification : le cahier des charges du '
     'gestionnaire prime.',
     ['essence', 'traitement', 'dimensions', 'longueurs', 'densite',
      'durabilite', 'certif', 'origine']),

    ('traites', 'valeur', 'Bois pour usage marin et agricole',
     ['exterieur', 'industrie'],
     'Pièces destinées aux ouvrages immergés, aux bâtiments d’élevage et aux '
     'structures agricoles. Classe d’emploi à déclarer explicitement.',
     ['essence', 'traitement', 'dimensions', 'longueurs', 'durabilite',
      'humidite', 'certif']),

    ('traites', 'secondaire', 'Emballages bois traités pour l’export',
     ['emballage'],
     'Palettes, caisses et calages conformes aux exigences phytosanitaires '
     'internationales. Sans le marquage requis, le conteneur est refusé au '
     'port d’arrivée — c’est le point de blocage le plus fréquent.',
     ['essence', 'phyto', 'traitement', 'dimensions', 'tolerance',
      'condition', 'origine']),

    # --- Pate, papier et carton ---------------------------------------------
    ('pate', 'secondaire', 'Pâte kraft blanchie',
     ['papeterie', 'industrie'],
     'Pâte chimique de référence pour les papiers d’impression et l’hygiène. '
     'Le type de fibre, longue ou courte, change complètement l’usage.',
     ['essence', 'blancheur', 'densite', 'humidite', 'condition',
      'origine', 'unite', 'certif']),

    ('pate', 'secondaire', 'Pâte mécanique et thermomécanique',
     ['papeterie'],
     'Pâte à haut rendement pour papiers d’impression économiques. Le '
     'compromis rendement / résistance est le sujet de négociation.',
     ['essence', 'blancheur', 'densite', 'humidite', 'condition', 'unite']),

    ('pate', 'valeur', 'Pâte à dissoudre',
     ['industrie'],
     'Pâte de haute pureté destinée au textile et aux dérivés cellulosiques. '
     'Marché exigeant, très différent de celui du papier.',
     ['essence', 'blancheur', 'humidite', 'condition', 'origine', 'unite', 'certif']),

    ('pate', 'valeur', 'Papier journal et papiers d’impression',
     ['papeterie'],
     'Bobines et rames pour l’impression. Le grammage et la laize se fixent '
     'avec la machine de l’imprimeur, pas au catalogue.',
     ['grammage', 'blancheur', 'humidite', 'condition', 'tolerance', 'unite']),

    ('pate', 'valeur', 'Carton et papiers d’emballage',
     ['papeterie', 'emballage'],
     'Kraftliner, fluting et cartons pour la caisse et l’emballage. Se '
     'vendent sur la résistance mécanique, pas sur l’aspect.',
     ['grammage', 'densite', 'humidite', 'condition', 'tolerance',
      'certif', 'unite']),

    ('pate', 'valeur', 'Papiers tissu et hygiène',
     ['papeterie'],
     'Bobines mères et produits convertis pour l’hygiène. Marché régional par '
     'nature : le transport pèse lourd dans le prix rendu.',
     ['grammage', 'blancheur', 'humidite', 'condition', 'unite']),

    ('pate', 'valeur', 'Papiers spéciaux et supports techniques',
     ['papeterie', 'industrie'],
     'Papiers couchés, barrières et supports pour l’étiquette et '
     'l’emballage technique. Développés spécification par spécification.',
     ['grammage', 'blancheur', 'surface', 'humidite', 'tolerance',
      'condition', 'unite']),

    # --- Biomasse -----------------------------------------------------------
    ('biomasse', 'valeur', 'Granulés de bois',
     ['energie'],
     'Combustible densifié pour le chauffage domestique et industriel. La '
     'teneur en cendres et l’humidité décident de la classe commerciale et du '
     'marché accessible.',
     ['essence', 'granulo', 'densite', 'cendres', 'humidite',
      'condition', 'certif', 'unite']),

    ('biomasse', 'valeur', 'Bûches densifiées et briquettes',
     ['energie'],
     'Combustible reconstitué à partir de sciure comprimée. Produit de '
     'grande distribution : le conditionnement fait partie du produit.',
     ['granulo', 'densite', 'cendres', 'humidite', 'condition', 'unite']),

    ('biomasse', 'primaire', 'Plaquettes forestières et copeaux énergie',
     ['energie', 'industrie'],
     'Combustible en vrac pour chaufferie collective et industrielle. Se '
     'contractualise sur l’humidité livrée, qui varie avec la saison.',
     ['granulo', 'humidite', 'densite', 'cendres', 'origine',
      'condition', 'unite']),

    ('biomasse', 'primaire', 'Bois de chauffage',
     ['energie'],
     'Bûches feuillues ou résineuses, vertes ou séchées. Marché local par '
     'nature, mais présent à l’export sur certaines destinations.',
     ['essence', 'dimensions', 'longueurs', 'humidite', 'densite',
      'condition', 'unite']),

    ('biomasse', 'valeur', 'Charbon de bois',
     ['energie', 'industrie'],
     'Charbon pour usage domestique et industriel. La matière première et le '
     'taux de carbone fixe décident de la qualité de combustion.',
     ['essence', 'granulo', 'cendres', 'humidite', 'densite',
      'condition', 'certif', 'unite']),

    ('biomasse', 'valeur', 'Litières et paillis horticoles',
     ['exterieur', 'industrie'],
     'Copeaux et fibres calibrés pour l’élevage et l’horticulture. Produit '
     'saisonnier, très sensible au coût de transport.',
     ['granulo', 'humidite', 'densite', 'condition', 'origine', 'unite']),
]

# ---------------------------------------------------------------------------
# LES PORTS. FAITS VERIFIABLES : nom, province, facade. RIEN D'AUTRE.
# Pas de tonnage, pas de tirant d'eau, pas de frequence de depart, pas de
# delai de transit — ces chiffres bougent chaque trimestre et je ne les ai pas
# mesures. Un acheteur verifie un nom de port en trente secondes ; il verifie
# un tonnage en une journee, et c'est celui-la qui coule un dossier.
# ---------------------------------------------------------------------------
PORTS = [
    ('Vancouver',        'Colombie-Britannique',   'Pacifique'),
    ('Prince Rupert',    'Colombie-Britannique',   'Pacifique'),
    ('Nanaimo',          'Colombie-Britannique',   'Pacifique'),
    ('Montréal',         'Québec',                 'Saint-Laurent'),
    ('Québec',           'Québec',                 'Saint-Laurent'),
    ('Trois-Rivières',   'Québec',                 'Saint-Laurent'),
    ('Sept-Îles',        'Québec',                 'Golfe du Saint-Laurent'),
    ('Halifax',          'Nouvelle-Écosse',        'Atlantique'),
    ('Saint John',       'Nouveau-Brunswick',      'Atlantique'),
    ('Belledune',        'Nouveau-Brunswick',      'Atlantique'),
    ('Thunder Bay',      'Ontario',                'Grands Lacs'),
    ('Hamilton',         'Ontario',                'Grands Lacs'),
]

# ---------------------------------------------------------------------------
# LES REFERENTIELS. Ce sont de VRAIS referentiels existants, presentes comme
# des CASES A REMPLIR. Aucun n'est presente comme detenu.
# ---------------------------------------------------------------------------
REFERENTIELS = [
    ('Certification forestière',
     'Le référentiel sous lequel la forêt d’origine est certifiée, et le type '
     'de déclaration associé. C’est la première pièce que demande un acheteur '
     'européen ou japonais.'),
    ('Classement structural',
     'Le règlement de classement appliqué et l’organisme qui supervise le '
     'marquage. Sans lui, le bois ne peut pas être utilisé en structure sur '
     'le marché de destination.'),
    ('Déclaration de conformité du marché importateur',
     'Chaque destination a son propre régime de mise sur le marché pour le '
     'bois. Le champ existe pour dire lequel s’applique, pas pour affirmer '
     'qu’il est satisfait.'),
    ('Diligence raisonnée sur l’origine',
     'La traçabilité remontant à la forêt d’origine, exigée à l’import sur '
     'plusieurs marchés. Se prépare avant la commande, pas au moment du '
     'dédouanement.'),
    ('Traitement phytosanitaire de l’emballage',
     'Le marquage porté par les palettes et les caisses. Point de blocage le '
     'plus fréquent à l’arrivée, et le plus facile à éviter.'),
    ('Traitement de préservation',
     'Le produit utilisé et la classe d’emploi visée. Les produits admis '
     'diffèrent d’un pays à l’autre.'),
]

# ---------------------------------------------------------------------------
# LES MARCHES. Des regions, pas des parts de marche.
# ---------------------------------------------------------------------------
MARCHES = [
    'États-Unis et Mexique', 'Europe de l’Ouest', 'Europe centrale et orientale',
    'Royaume-Uni et Irlande', 'Japon', 'Chine et Asie du Nord-Est',
    'Corée du Sud et Taïwan', 'Asie du Sud-Est', 'Inde et sous-continent',
    'Moyen-Orient', 'Afrique du Nord', 'Afrique de l’Ouest',
    'Amérique du Sud', 'Caraïbes', 'Océanie',
]

NOTE = (
    'Chaque carte est une CATÉGORIE de produit, pas une référence en stock. '
    'Elle indique ce que la catégorie regroupe, les applications où elle est '
    'demandée, son niveau de transformation, et la grille de champs qu’un '
    'acheteur international exigera avant de coter. C’est cette grille qui '
    'structure le catalogue : dès qu’une offre réelle existe, elle se range '
    'dans une catégorie et hérite de ses champs. Le niveau de transformation '
    'est un axe à part entière — l’acheteur de grumes et l’acheteur de '
    'lamellé-collé ne sont pas la même personne et ne demandent pas les mêmes '
    'documents.'
)

AVERTISSEMENT = (
    'Le brief demandait des capacités d’approvisionnement. Il n’y en a aucune '
    'sur cette page, et c’est délibéré : aucun volume, aucun tonnage, aucun '
    'délai, aucun prix, aucune fréquence d’expédition, aucune certification '
    'présentée comme détenue, aucune essence annoncée disponible. Je n’ai rien '
    'mesuré et aucune donnée d’offre ne m’a été transmise. Sur une page '
    'd’export, un volume annoncé est la première chose qu’un acheteur fait '
    'vérifier, et la première qui tue un dossier si elle est fausse. La page '
    'dit donc quelle unité déclarer et sur quelle base, jamais combien. Les '
    'ports listés sont réels et donnés avec leur seule province et leur seule '
    'façade — des faits vérifiables en trente secondes.'
)
