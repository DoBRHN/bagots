########################################################################################################################
#                                               MODIFIER LES LIGNES 17 et 18                                           #
#                                         SI BESOIN D'UN EXPORT A UNE DATE ANTERIEURE                                  #
########################################################################################################################
import paramiko

from paramiko import AutoAddPolicy
from datetime import date, datetime
from pathlib import Path

today = date.today()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
start_time = datetime.now()

#### DATE ####
MONTH = today.strftime("%b")
YEAR = today.strftime("%Y")
#MONTH = "" #Pour un export antérieur à la date du jour, sélectionner le mois souhaité (ex: Sep, Oct, Feb) et décommenter la ligne
#YEAR = "" #Pour un export antérieur à la date du jour, sélectionner l'année souhaitée et décommenter la ligne

#### DIR ####
CURRDIR = Path("Path")
DATAFILE = CURRDIR / "data"
TEMPFILE = CURRDIR / "tmp" / "output.txt"
FINALFILE = DATAFILE / f"Bagots_{MONTH}_{YEAR}.txt"

#### DATABASE ####
LOGIN_DB = "login"
PASS_DB = "mdp"
HOST_DB = "IP"
NAME_DB = "nom_db"
HOSTNAME_REQUEST = "RequeteSQL1"
IP_REQUEST = "RequeteSQL2"

#### COMMAND ####
LOG1 = f"show log messages | match RPD_OSPF_NBRDOWN | match {YEAR} | match {MONTH} | no-more"
LOG2 = f"show log messages.0.gz | match RPD_OSPF_NBRDOWN | match {YEAR} | match {MONTH} | no-more"

#### MAIL ####
FROM = "Mail emetteur"
TO = "Mail cible"


#### BANNER ####
BANNER = """
                     _     _       _               ____             _
                    | |   (_)_ __ | | _____ _ __  |  _ \ ___  _   _| |_ ___ _ __
                    | |   | | '_ \| |/ / _ \ '__| | |_) / _ \| | | | __/ _ \ '__|
                    | |___| | | | |   <  __/ |    |  _ < (_) | |_| | | | __/ |
                    |_____|_|_| |_|_|\_\___|_|    |_| \_\___/ \__,_|\__\___|_|
                  ----------------------------------------------------------------
                   WARNING - ACCESS CONTROLLED - ANY LOGIN ATTEMPT WILL BE LOGGED
                  ----------------------------------------------------------DBR---
            """