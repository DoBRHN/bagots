import argparse
import textwrap

parser = argparse.ArgumentParser(prog="Bagots script", 
                                description="Description des arguments du script", 
                                formatter_class=argparse.RawDescriptionHelpFormatter, 
                                epilog=textwrap.dedent("""
Pour lancer le script, utiliser la commande ci-dessous, à l'identique !

------------------------------------------------------------------------------------------------------------------------
                                        python3 main.py -u login
------------------------------------------------------------------------------------------------------------------------

[INFOS] :
    - Le dossier "data" comporte uniquement l'export lors de l'execution du script. 
    Après chaque envoie, l'export est déplacé dans le dossier "old".

[ATTENTION] : 
    - Il n'y a pas de guillemets pour le login
    - Ne pas toucher a l'arborescence (dossiers et fichiers)

[DEVELOPPED BY] 
BRUCHON Dorian - NXO FRANCE
   
"""))
parser.add_argument("-u", "--user", type=str, help="login", required=True)
args = parser.parse_args()