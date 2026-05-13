import urllib.request 
import random
import re
import os

def decolor(a):
    return re.sub(r'\033\[[0-9;]*m', '', a) # Décolore la lettre donné

def color(a,b): # Colorer l'alphabet
    var=0
    while decolor((alph[var]).lower()) != a: # Chercher la bonne lettre 
        var += 1
    if b=="V":
        alph[var]="\033[32m"+decolor(alph[var])+"\033[0m"
    if b=="J":
        if not "\033[32m" in alph[var]:
            alph[var]="\033[33m"+alph[var]+"\033[0m"
    if b=="R":
        if not "\033[32m" in alph[var] and not "\033[33m" in alph[var]:    
            alph[var]="\033[31m"+alph[var]+"\033[0m"

def ra(a,b):
    return(random.randint(a,b)) # Ce sera pour prendre un mot aléatoire de la liste

def wordel(jsp,ess,lan): # La longueur des mots est égale à jsp
    LANGUES = {
        "anglais":     ("words_en.txt",  "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt", "utf-8"),
        "francais":    ("words_fr.txt",  "https://raw.githubusercontent.com/Thecoolsim/French-Scrabble-ODS8/main/French%20ODS%20dictionary.txt", "utf-8"),
        "espagnol":    ("words_es.txt",  "https://raw.githubusercontent.com/kkrypt0nn/wordlists/main/wordlists/languages/spanish.txt", "utf-8"),
        "italien":     ("words_it.txt",  "https://raw.githubusercontent.com/kkrypt0nn/wordlists/main/wordlists/languages/italian.txt", "utf-8"),
        "allemand":    ("words_de.txt",  "https://raw.githubusercontent.com/kkrypt0nn/wordlists/main/wordlists/languages/german.txt", "utf-8"),
        "portugais":   ("words_pt.txt",  "https://raw.githubusercontent.com/kkrypt0nn/wordlists/main/wordlists/languages/portuguese.txt", "utf-8"),
        "neerlandais": ("words_nl.txt",  "https://raw.githubusercontent.com/kkrypt0nn/wordlists/main/wordlists/languages/dutch.txt", "utf-8"),
        "polonais":    ("words_pl.txt",  "https://raw.githubusercontent.com/kkrypt0nn/wordlists/main/wordlists/languages/polish.txt", "utf-8"),
        "suedois":     ("words_sv.txt",  "https://raw.githubusercontent.com/kkrypt0nn/wordlists/main/wordlists/languages/swedish.txt", "utf-8"),
        "norvegien":   ("words_no.txt",  "https://raw.githubusercontent.com/kkrypt0nn/wordlists/main/wordlists/languages/norwegian.txt", "utf-8"),
    }
    fichier, url, enc = LANGUES[lan]
    if not os.path.exists(fichier):
        print(f"Téléchargement du dictionnaire {lan}...")
        urllib.request.urlretrieve(url, fichier)
    with open(fichier, "r", encoding=enc) as f:
        liste = [mot.lower() for mot in f.read().splitlines()]  
    mat=[]
    for i in range(2,50): # Je créer une matrice contenant une liste pour chaque longueur de mots
        souma=[]
        for o in range(len(liste)):
            if len(liste[o])==i:
                souma.append(liste[o]) # J'ajoute les mots de la bonne longueur
        if i==5 and lan=="anglais":
            souma.append("pesto") # On oublie pas le pesto
        mat.append(souma) 
    dif=jsp-2
    vert = "\U0001F7E2"
    jaune = "\U0001F7E1"
    rouge = "\U0001F534"
    print(rouge+":pas cette lettre "+jaune+":mauvais endroit "+vert+":bien placé") # Consigne
    print("C'est des mots de ",str(jsp)," lettres") # Préciser la longueur des mots
    s=0 # Compteur
    rep="" 
    lis=mat[dif] # Prendre la bonne liste dans la matrice
    mad=lis[ra(0,len(lis)-1)] # Mot aléatoire de la liste
    for i in range(ess): # Nombre d'essais permis
        s+=1 # Augmenter le compteur
        rep = (str(input(""))).lower() # Proposition du joueur
        while not rep in lis or len(rep) != jsp: # On vérifie que le mot est valide
            if len(rep) != jsp: # S'il n'a pas la bonne longueur
                print("Le mot n'est pas de la bonne longueur")
            else: # Si la proposition du joueur n'existe pas 
                print("Ce mot n'existe pas")
            rep = (str(input(""))).lower() # On redemande un mot au joueur
        if rep == mad: # Si le mot a été deviné
            print("T'as réussi en "+str(s)+" essais !")
            if input("Tu veux rejouer ? (yes/no)") == "yes": # Si le joueur veut rejouer 
                wordel(jsp,ess,lan)
            return("")
        else:
            coul=[] # Liste vide pour définir les couleurs
            for f in range(len(mad)):
                coul.append("R") # Liste rempli de rouge
            cop=list(mad) # Copie du mot à deviner
            coprep=list(rep) # Copie du mot proposé
            for o in range(len(mad)): 
                if rep[o] == mad[o]:
                    coul[o]="V" # Les lettres bien placées sont enregistrées en vert
                    cop[o]=0 
                    coprep[o]=1 # Les lettres bien placées sont indisponibles dans les copies 
                    color(rep[o],"V")
            for o in range(len(mad)): 
                if coprep[o] in cop: # S'il y a la même lettre dans les copies du mot à deviner et de la proposition
                    coul[o]="J" # Enregistrer les lettres concernées en jaune
                    color(rep[o],"J")
                    compteur=0
                    while not coprep[o] == cop[compteur]: # Trouver et rendre indisponible la lettre utilisée 
                        compteur+=1
                    cop[compteur]=0
                    coul[o]="J" # Trouver et rendre indisponible la lettre utilisée
            for o in range(len(mad)):
                if not rep[o] in mad:
                    color(rep[o],"R")
        cop2=list(rep)
        prop=[]
        for o in range(len(coul)): # Changer les couleurs de la proposition et mettre en majuscule
            if coul[o]=="V":
                prop.append("\033[32m"+cop2[o].upper()+"\033[0m")
            elif coul[o]=="J":
                prop.append("\033[33m"+cop2[o].upper()+"\033[0m")
            else:
                prop.append("\033[31m"+cop2[o].upper()+"\033[0m")
        print("".join(prop)+"     "+str(" ".join(alph))) # Lier la proposition colorée
    print("Désolé, t'as plus d'essais, c'était "+mad) # Si le joueur tombe à cours d'essais
    if input("Tu veux rejouer ? (yes/no)") == "yes": # Si le joueur veut rejouer 
                wordel(jsp,ess,lan)
    return("")


alph=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z "] # Alphabet
for i in range(len(alph)):
    alph[i]=decolor(alph[i]) # Décolorer l'alphabet à chaque début de jeu

wordel(5,10,"francais") # Changer la difficulté et la langue du jeu










