# bagots
-- 
> CONTEXT

Au sein d'un environnement d'exploitation comprenant +200 liaisons WAN composé de Juniper SRX, nous voulions chaque fin de mois, avoir un export automatisé permettant de recenser le nombre de bagots du mois en cours.

> FONCTIONNEMENT

- Lors de l'exécution de script, une connexion à notre base de données s'établie et je récupère les informations nécessaires afin de créer un dictionnaire comprenant l'intégralité des nos hôtes, type :

    - {'HOSTNAME': 'IP'}
 
- Ensuite, je boucle sur le dictionnaire afin d'exécuter la commande permettant de récupérer les bagots du mois en cours (lors de l'éxecution je récupère la date du jour).

    - show log messages | match RPD_OSPF_NBRDOWN | match {YEAR} | match {MONTH} | no-more

    - En cas de nombreux bagots, j'exécute la même commande mais sur un fichier de logs plus ancien (messages.0.gz)

- Je recupère les outputs dans un fichier temporaire, je comptes les lignes et je les importes dans mon fichier final afin d'avoir le résultat pour chaque hôtes :

    - 'HOSTNAME' : 'NB BAGOTS'

- Dès la boucle terminé, le fichier est automatiquement envoyé par mail 


> INFOS 

- Il faut compter 10 minutes d'exécution pour l'export de +200 équipements
- Version 3.10 de Python. Réflexion pour passer sur la 2.7 et exploiter des modules de threading

