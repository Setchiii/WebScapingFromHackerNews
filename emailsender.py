# crée une fonction qui permet d'envoyer un email depuis une adresse gmail vers une autre adresse email. Le contenu de l'email est le résultat de la fonction extract_links intégré au template email_template.html.
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from email.mime.base import MIMEBase
from datetime import date
from bs4 import BeautifulSoup


def read_personaldata_file(file_path):
    env_dict = {}
    with open(file_path, 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            env_dict[key] = value
    print(f"...{len(env_dict)} personal data lues...")
    return env_dict


def send_email(personaldata_dict, subject, body, attachment=None):
    # Création de l'objet MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = personaldata_dict["EMAIL_SOURCE"]
    msg['To'] = personaldata_dict['EMAIL_DEST']
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    # Ajout de la pièce jointe
    if attachment:
        with open(attachment, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            f'attachment; filename= {attachment}')
            msg.attach(part)

    # Envoi de l'email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(personaldata_dict['EMAIL_SOURCE'],
                 personaldata_dict['EMAIL_PASSWORD'])
    server.sendmail(personaldata_dict['EMAIL_SOURCE'],
                    personaldata_dict['EMAIL_DEST'], msg.as_string())
    server.quit()
    print("...email envoyé...")

# Fonction qui prend en paramètre le nom du fichier template html et les données à insérer dans le template. Elle retourne le contenu du template avec les données insérées.
# les données à insérer sont passées en paramètre sous forme d'un tableau dont les éléments sont des tableaux de 3 éléments : le nom, le lien et le score.
# La balise {{title}} est remplacée par "News de Hacker News du" + la date du jour
# Les balises {{content1}} à content 5 sont à remplacer par le contenu des 5 premiers éléments du tableau de données.
# Chaque content doit être structuré comme suit: nom + ": " + lien + "( " + score + " points)"


def create_email_content(template_file, data):
    with open(template_file, 'r') as f:
        template = f.read()
    soup = BeautifulSoup(template, 'html.parser')
    title = soup.find('h1')
    title.string = "News de Hacker News du " + str(date.today())
    content = soup.find_all('p')
    for i in range(5):
        content[i].string = data[i][0] + ": " + \
            data[i][1] + "( " + str(data[i][2]) + " points)"
    print("...email content généré...")
    return str(soup)
