from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

app = Flask(__name__)

def url_valide(url):
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])

def compter_occurences(mot_cle, url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        texte = soup.get_text().lower()
        return texte.count(mot_cle.lower())
    except Exception as e:
        print(f"Erreur pour {url} : {e}")
        return -1

@app.route('/', methods=['GET', 'POST'])
def index():
    resultat = None
    mot_cle = ''
    url = ''
    erreur = False
    erreur_url = False

    if request.method == 'POST':
        mot_cle = request.form.get('mot_cle', '').strip()
        url = request.form.get('url', '').strip()

        if not url_valide(url):
            erreur_url = True
        else:
            resultat = compter_occurences(mot_cle, url)
            if resultat == -1:
                erreur = True

    return render_template('index.html', mot_cle=mot_cle, url=url,
                           resultat=resultat, erreur=erreur, erreur_url=erreur_url)

if __name__ == '__main__':
    app.run(debug=True)
