#coding:utf-8

import requests
import getopt
import sys
import time
import json

timeout = 1
opt, a = getopt.getopt(sys.argv[1:], "", ["proxies=", "save=", "timeout=", "help"])

for o in opt:
    if "--help" == o[0]:
        print(
""" Help:
     --help : commande d'aide
     --proxies=<nom_du_fichier> : chemin vers le fichier contenant la liste de proxies
     --save=<nom_du_fichier> : fichier avec les proxies valide sauvegardé (pas obligatoire)
     --timeout=<temps> : temps max en seconde pour la réponse du proxy 
        Exemple : 0.5 = 500ms donc la réponse du proxy doit mettre max 500ms
        ce qui vaut environ 0.5*2=1s max pour envoyer est recevoir la réponse du proxy
""")
        exit(0)
    elif "--proxies" == o[0]:
        fichierProxiesATester=o[1]
    elif "--save" == o[0]:
        fichierSauvegardeProxies=o[1]
    elif "--timeout" == o[0]:
        timeout=float(o[1])

with open(fichierProxiesATester) as f:
    lecture=f.read().split()

proxiesValide = 0
proxiesInvalide = 0
listeProxiesQuiMarche = []
for i in lecture:
    try:
        debTemps = time.time()
        r=requests.get("https://api.myip.com", proxies={"https":"https://"+i}, timeout=timeout)

        if r.status_code == 200:
            finTemps = time.time()
            dicoApiMyIp = json.loads(r.text)

            print(
f"""[+] Proxy {i} valide | time = {round((finTemps-debTemps)*1000)}ms | what's ip => {dicoApiMyIp.get('ip')}; pays => {dicoApiMyIp.get('country')}"""
            )
            listeProxiesQuiMarche.append(i)
            proxiesValide+=1
        else:
            proxiesInvalide+=1

    except (requests.exceptions.ConnectionError, requests.exceptions.ProxyError, requests.exceptions.SSLError, 
    requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
        proxiesInvalide+=1

print(f"[i'] Proxies valide => {proxiesValide} | Proxies invalide ou réponse > 1000ms => {proxiesInvalide}")

try:
    with open(fichierSauvegardeProxies, "a") as f:
        for i in listeProxiesQuiMarche:
            f.write(i+"\n")
except IndexError:
    pass