########################################################################################################################
#                                            MERCI DE NE RIEN MODIFIER ICI !                                           # 
########################################################################################################################
import getpass
import paramiko
import mariadb
import os
import glob
import smtplib

from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
from datetime import datetime
from tqdm import tqdm

from app import args
from var import ssh, start_time, today
from var import PASS_DB, TEMPFILE, FROM, TO, LOGIN_DB, PASS_DB, HOST_DB, NAME_DB, HOSTNAME_REQUEST, IP_REQUEST, BANNER, MONTH, YEAR, FINALFILE, LOG1, LOG2

class BagotsSRX:
    def __init__(self):
        os.chdir('Path')
        for file in glob.glob(f"*"):
            os.replace(file, f'/Path/{file}')
        try:
            conn = mariadb.connect(        
            user=LOGIN_DB,
            password=PASS_DB,
            host=HOST_DB,
            database=NAME_DB)
            cur = conn.cursor()
            cur.execute(HOSTNAME_REQUEST)
            dict_value = [str(f[3]) for f in cur.fetchall()] #HOSTNAME
            cur.execute(IP_REQUEST)
            dict_key = [str(f[2]) for f in cur.fetchall()] #IP
            zip_iterator = zip(dict_value, dict_key)
            self.result = dict(zip_iterator)
            self.sumhosts = len(self.result)
            print('\n' + '-'*82)
            print(f'Connection réussi - il y a actuellement {self.sumhosts} sites dans la database\n')

        except mariadb.OperationalError:
            print('Erreur - Mot de passe base de donnée incorrect')
            quit()

        except KeyboardInterrupt:
            print('\nVous avez interrompu le script')
            os.remove(FINALFILE)
            quit() 

    def cmdsrx(self, cmd=""):
        stidn, stdout, stderr = ssh.exec_command(cmd)
        cmd_result = stdout.readlines()
        with open(TEMPFILE, "w", encoding="utf-8") as f:
            f.writelines(cmd_result)

    def exec(self):
        print(f'Année et Mois en cours : {MONTH} {YEAR}')
        print(BANNER)
        username = args.user
        print(f'login: {username}')
        password = getpass.getpass()
        days = today.strftime('%b-%d-%Y')
        print(f"Date de l'export : {days}", file=open(FINALFILE, "a"))
        print(f"Analyse des bagots pour le mois : {MONTH} {YEAR}" + "\n", file=open(FINALFILE, "a"))
        print("\nLe fichier de bagots sera envoyé par mail une fois terminé :)")
        self.pbar = tqdm(total=self.sumhosts)
        for key, value in self.result.items():
            try:
                ssh.connect(value, username=username, password=password)
                a.cmdsrx(LOG1)
                with open(TEMPFILE, 'r') as f:
                    allbagots = len(f.readlines())

                if allbagots > 50:
                   a.cmdsrx(LOG2)
                   with open(TEMPFILE, 'r') as f:
                    bagots_count = len(f.readlines())

                   print(f"{key} : {allbagots + bagots_count}", file=open(FINALFILE, "a"))

                else:
                   print(f"{key} : {allbagots}", file=open(FINALFILE, "a"))

                self.pbar.update(1)

            except paramiko.SSHException:
                print("\nErreur d'authentification radius")
                quit()

            except KeyboardInterrupt:
                print('\nVous avez interrompu le script')
                os.remove(FINALFILE)
                quit()

            except:
                print(f"{key} : injoignable via {value}", file=open(FINALFILE, "a"))

        
        end_time = datetime.now()
        print("\n[INFO] - Temps d'execution du script: {}".format(end_time - start_time), file=open(FINALFILE, "a"))
        os.remove(TEMPFILE)
        a.sendmail()
    
    def sendmail(self):
        try:
            msg = MIMEMultipart() 
            msg['From'] = FROM
            msg['To'] = TO
            msg['Subject'] = "Report bagots"
            body = "Ci-joint le rapport d'analyse des bagots"
            msg.attach(MIMEText(body, 'plain'))
            os.chdir('Path')
            for file in glob.glob("*.txt"):
                filename = file
            attachment = open(filename, "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read()) 
            encoders.encode_base64(p) 
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
            msg.attach(p) 
            s = smtplib.SMTP('SMTP') 
            s.starttls() 
            text = msg.as_string() 
            s.sendmail(FROM, TO, text)
            os.replace(file, f'/Path/{file}')
            s.quit()
            self.pbar.close()
            print('\nLe rapport à été envoyé par mail :)')

        except AttributeError:
            os.replace(file, f'/Path/{file}')
            print("[ERREUR] - Le mail n'a pas pu être envoyé. Retrouver le report dans le repertoire old")

if __name__ == "__main__":
    try:
        a = BagotsSRX()
        a.exec()
        
    except KeyboardInterrupt:
        print('Vous avez interrompu le script')
        os.remove(FINALFILE)


    
    
