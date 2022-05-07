#################################
# Groupe MI TD2 (groupe de projet n°3)
# Ania AOUAOUCHE
# Tiphanie DEPREAUX
# Baptiste PARIS
# https://github.com/uvsq22102500/Fourmi-de-Langton

from tkinter import *

#-------------------------------------------------------------------------------------------------------
# constantes 
#-------------------------------------------------------------------------------------------------------

# dimensions de notre canvas
LARGEUR = 640
HAUTEUR = 640

# nombre et dimensions des carrés de notre canvas
N = 71
L = LARGEUR//N   

#couleurs possibles
BLANC = 0
NOIR = 1

ORANGE = 2
ROUGE = 3
BLEU = 4

COULEUR_FLECHE = "brown"
 
#directions possibles de la fleche
NORD = 0
SUD = 1
OUEST = 2
EST = 3

#-------------------------------------------------------------------------------------------------------
# variables globales 
#-------------------------------------------------------------------------------------------------------

# listes
grille = []
grille_canvas = []

# positions de la fourmi 
position_i = N//2
position_j = N//2

# direction initiale de la fourmi 
DIRECTION = NORD

# variable qui nous permettra de mettre le bouton play en pause
mouv = True

# variables qui nous permettront de modifier la vitesse de la fourmi
normal,rapide,lent= True, True, True

# activation de la fonction couleur
couleurs = False

# compteur qui nous permettra de differencier le 1er et le 2eme mouvement a gauche et a droite
cpt_D_BLANC, cpt_D_ROUGE = 1, 1
cpt_G_ORANGE, cpt_G_BLEU  = 1, 1

# ---------------------------- creation de la fenetre principale -----------------------------------
window = Tk()
window.geometry("1000x700")
window.title("Fourmi de Langton")
window.configure(background='white')

#creation d'un canvas pour generer notre terrain
canvas = Canvas( window , height = HAUTEUR , width = LARGEUR, background='white' )

#creation de notre fleche
fleche = Canvas (window)

#creation d'une boite ou on mettra nos boutons 
frame = Frame (window, height = 320 , width = 360)

#implementer une image 
canvas_image = Canvas (window, height = 320 , width = 360)
image = PhotoImage(file='clavier.gif')
label= Label (canvas_image,image = image)

# -----------------------------------------------------------------------------------------------
# les fonctions
# -----------------------------------------------------------------------------------------------

# ----------------------------- fonctions initiles ----------------------------
def initialisation(): 
    global grille, grille_canvas
    """initialisation de la grille a 0 """
    """cette grille nous permettra plus tard de savoir de quelle couleur est notre carré """
    """pour ensuite pouvoir la modifier (en 1 ou 0 ; 1 etant le noir ; 0 etant le blanc) """
    for i in range(N):
        grille.append([0]*N)
        """cette 2eme grille nous permettra de garder les coordonnés des carrés de notre environnement"""
        grille_canvas.append([0]*N) 

def environnement():
    """ une 3eme grille a 2D pour la creation de notre environnement """ 
    for i in range(N):
        for j in range(N):
            x, y = j*L , i*L 
            carre = canvas.create_rectangle( (x,y), (x + L, y + L), fill="white")
            grille[i][j] = BLANC
            grille_canvas[i][j] = carre

#--------------------------- creation de notre fourmi "notre fleche" -----------------------------------
def fourmi():
    global fleche

    x_mil = LARGEUR//2  #milieu de notre canvas en x
    y_mil = HAUTEUR//2  #milieu de notre canvas en y

    """verifier le cas ou le nombre de carrés est pair ou impair et placer la fleche au milieu"""
    if N%2 != 0 :
        x1 = x_mil 
        y1 = y_mil+ L/2
        x2 = x_mil
        y2 = y_mil- L/2    
    else :
        x1 = x_mil + L/2
        y1 = y_mil + L
        x2 = x_mil + L/2
        y2 = y_mil 

    """creation de notre fleche initiale """    
    fleche = canvas.create_line ( (x1, y1), (x2, y2), fill = COULEUR_FLECHE, width = 5, smooth = True, arrow="last", arrowshape = (5,6,2) )
    
#---------------------fonction qui permet de changer les coordonnés de la fleche ,"sa position"-----------------
def fourmi_update():
    global fleche, position_i, position_j, id_after, normal,rapide,lent, x1, x2, y1, y2

    if DIRECTION == NORD:
        x1 = position_j * L + L/2   
        y1 = position_i *L + L
        x2 = position_j * L + L/2
        y2 = position_i *L 
        canvas.coords ( fleche , x1, y1, x2, y2 )
    elif DIRECTION == SUD:
        x2 = position_j * L + L/2   
        y2 = position_i *L + L
        x1 = position_j * L + L/2
        y1 = position_i *L 
        canvas.coords ( fleche , x1, y1, x2, y2 )  
    elif DIRECTION == EST:
        x1 = position_j * L 
        y1 = position_i *L + L/2
        x2 = position_j * L + L 
        y2 = position_i *L + L/2
        canvas.coords ( fleche , x1, y1, x2, y2 )
    elif DIRECTION == OUEST:
        x2 = position_j * L  
        y2= position_i *L + L/2
        x1 = position_j * L + L
        y1 = position_i *L + L/2
        canvas.coords ( fleche , x1, y1, x2, y2 )

    """normal se remet a True quand on appuie sur play, lent et rapide se mettent a False"""
    """rapide se met en True quand on appuie sur la touche demandé, normal et lent se mettent en False"""
    """lent se met en True quand on appuie sur la touche demandé, normal et rapide se mettent en False"""
    if normal == True :
        id_after = canvas.after(100, play)
    elif rapide == True :
        id_after = canvas.after(25, play)
    elif lent == True :
        id_after = canvas.after(500, play)
    if couleurs == True :
        id_after = canvas.after(25,couleur)
    
    
#-----------------fonction qui permet de changer la couleur d'un carré et de changer la direction de la fleche-----------
def play ():
    global position_i, position_j , DIRECTION, grille , grille_canvas
    
    """verification de la couleur de notre carre"""
    if grille[position_i][position_j] == BLANC :
        grille[position_i][position_j] = NOIR 
        canvas.itemconfigure( grille_canvas[position_i][position_j] ,  fill = "black")

        """changement de direction si la couleur du carré est blanc"""
        if DIRECTION == NORD:
            DIRECTION = EST
            position_j = (position_j+1)%N
        elif DIRECTION == SUD:
            DIRECTION = OUEST
            position_j = (position_j-1)%N
        elif DIRECTION == EST:
            DIRECTION = SUD
            position_i = (position_i+1)%N
        elif DIRECTION == OUEST:
            DIRECTION = NORD
            position_i = (position_i-1)%N 
    else :
        grille[position_i][position_j] = BLANC 
        canvas.itemconfigure(grille_canvas[position_i][position_j], fill = "white")

        """changement de direction si la couleur du carré est noir"""
        if DIRECTION == NORD:
            position_j = (position_j-1)%N
            DIRECTION = OUEST   
        elif DIRECTION == SUD:
            position_j = (position_j+1)%N     
            DIRECTION = EST
        elif DIRECTION == EST:
            position_i = (position_i-1)%N
            DIRECTION = NORD
        elif DIRECTION == OUEST:
            position_i = (position_i+1)%N
            DIRECTION = SUD
    
    fourmi_update()

#--------------fonction qui change le bouton "play" en bouton "pause",et active la fonction play-------------
def demarrer ():
    global mouv, id_after, normal,rapide,lent
    if mouv:
        button_play.config(text="Pause")
        normal = True
        rapide, lent = False, False
        play()
    else:
        canvas.after_cancel(id_after)
        button_play.config(text="Play")

    mouv = not mouv    

#------------------ fonction qui permet d'enregistrer une sequence dans un fichier -------------------------
def enregistre():
    """Ecrit la taille de la grille et les valeurs de la liste grille dans le fichier enregistrement.txt"""
    fic = open("enregistrement.txt", "w")
    fic.write(str(N) + "\n")
    fic.write(str(position_i)+ "\n")
    fic.write(str(position_j)+ "\n")
    fic.write(str(DIRECTION)+ "\n")
    fic.write(str(x1) + "\n")
    fic.write(str(y1) + "\n")
    fic.write(str(x2) + "\n")
    fic.write(str(y2) + "\n")
    for i in range(N):
        for j in range(N):
            fic.write(str(grille[i][j])+ "\n")
    fic.close()

#------------------ fonction qui permet de lire le fichier et affiche dans le canvas la grille lu ----------------
def charge_grille():
    global N, position_i, position_j, mouv, DIRECTION, x1, x2, y1, y2, fleche
    """Lit le fichier enregistrement.txt, affiche dans le canvas la grille lu dans le fichier,
    replace la fourmi à l'état dans lequel elle se trouvait lors de l'enregistrement"""

    fic = open("enregistrement.txt", "r")

    # Récupérer le nombre de lignes et de colonnes de la grille
    taille = fic.readline()
    # Recuperer la position ,l'orientation et les coordonnés de la fleche
    position1 = fic.readline()
    position2 = fic.readline()
    orientation = fic.readline()
    coords1 = fic.readline()
    coords2 = fic.readline()
    coords3 =fic.readline()
    coords4 = fic.readline()
    
    # on recupère ensuite toutes les valeurs enregistrer dans les variables correspondantes
    N = int(taille)
    position_i = int(position1)
    position_j = int(position2)
    DIRECTION = int(orientation)
    x1 = coords1
    y1 = coords2
    x2 = coords3
    y2 = coords4

    canvas.delete() # on veut créer une nouvelle grille donc, on détruit la première
    # on initialise un nouveau canevas
    environnement()
    i, j = 0, 0
    # on met à jour la liste grille qui contient la couleur de chaque carré de l'enregistrement
    for ligne in fic:
        grille[i][j] = int(ligne)
        j += 1
        if j == N:
            j = 0
            i += 1
    # on associe les données de "grille" aux carrés en les modifiants avec la couleur correspondantes (noir ou blanc)       
    for i in range(N):
        for j in range(N):
            if grille[i][j] == 0:
                canvas.itemconfigure(grille_canvas[i][j], fill = "white")
            elif grille[i][j] ==1:  
                canvas.itemconfigure(grille_canvas[i][j], fill = "black")
    # on recrée un fleche avec les coordonnées sauvegardés             
    fleche = canvas.create_line ( (x1, y1), (x2, y2), fill = COULEUR_FLECHE, width = 5, smooth = True, arrow="last", arrowshape = (5,6,2) )
    mouv = not mouv # pour avoir le choix de redémarrer ou non l'automate avec les boutons play ou next
    demarrer()
    fic.close()

#fonction qui permet d'accelerer le mouvement de la fourmi------------------------------------------------
def rightKey (event):
    global normal,rapide,lent
    normal, lent = False, False
    rapide = True
    fourmi_update

#---------------------------fonction qui permet de ralentir le mouvement de la fourmi---------------------
def leftKey (event):
    global normal,rapide,lent
    normal, rapide = False, False
    lent = True
    fourmi_update   
   
window.bind ('<Right>', rightKey)
window.bind ('<Left>', leftKey)

# ------------------fonction qui permet de faire avancer la fourmi d'un mouvement ----------------------------
def next ():
    global mouv, id_after, normal,rapide,lent
    normal,rapide,lent = False, False , False
    play()
    
# ---------- fonction qui permet de revenir en arriere d'un mouvement -----------------------------------
def retour ():
    global DIRECTION, grille,position_i, position_j, normal,rapide,lent
    normal,rapide,lent = False, False , False
    if DIRECTION == NORD :
        if grille[position_i+1][position_j] == BLANC :
            grille[position_i+1][position_j] = NOIR
            canvas.itemconfigure( grille_canvas[position_i+1][position_j] ,  fill = "black")
            position_i = (position_i+1)%N
            DIRECTION = EST
        else :
            grille[position_i+1][position_j] = BLANC
            canvas.itemconfigure( grille_canvas[position_i+1][position_j] ,  fill = "white")
            position_i = (position_i+1)%N
            DIRECTION = OUEST

    elif DIRECTION == SUD :
        if grille[position_i-1][position_j] == BLANC :
            grille[position_i-1][position_j] = NOIR
            canvas.itemconfigure( grille_canvas[position_i-1][position_j] ,  fill = "black")
            position_i = (position_i-1)%N
            DIRECTION = OUEST
        else :
            grille[position_i-1][position_j] = BLANC
            canvas.itemconfigure( grille_canvas[position_i-1][position_j] ,  fill = "white")
            position_i = (position_i-1)%N
            DIRECTION = EST
            
    elif DIRECTION == EST :
        if grille[position_i][position_j-1] == BLANC :
            grille[position_i][position_j-1] = NOIR
            canvas.itemconfigure( grille_canvas[position_i][position_j-1] ,  fill = "black")
            position_j = (position_j-1)%N
            DIRECTION = SUD
        else :
            grille[position_i][position_j-1] = BLANC
            canvas.itemconfigure( grille_canvas[position_i][position_j-1] ,  fill = "white")
            position_j = (position_j-1)%N
            DIRECTION = NORD

    elif DIRECTION == OUEST :
        if grille[position_i][position_j+1] == BLANC :
            grille[position_i][position_j+1] = NOIR
            canvas.itemconfigure( grille_canvas[position_i][position_j+1] ,  fill = "black")
            position_j = (position_j+1)%N
            DIRECTION = NORD
        else :
            grille[position_i][position_j+1] = BLANC
            canvas.itemconfigure( grille_canvas[position_i][position_j+1] ,  fill = "white")
            position_j = (position_j+1)%N
            DIRECTION = SUD
    
    fourmi_update()

# ----------------------fonction qui genere 4 couleurs---------------------------------------
def couleur():
    global position_i, position_j , DIRECTION, grille , grille_canvas, cpt_D_ROUGE,cpt_G_ORANGE,cpt_D_BLANC,cpt_G_BLEU,normal,rapide,lent,couleurs
    
    """si on est sur du blanc ou du rouge on tourne a 90 a droite et on change la couleur en orange la 1ere fois et en bleu la 2eme fois"""
    """si on est sur du orange ou du bleu on tourne a 90 a gauche et on change la couleur en rouge la 1ere fois et en blanc la 2eme fois"""
    
    if grille[position_i][position_j] == BLANC or grille[position_i][position_j] == ROUGE :

        if grille[position_i][position_j] == ROUGE :
            if cpt_D_ROUGE == 1 :
                grille[position_i][position_j] = ORANGE
                canvas.itemconfigure( grille_canvas[position_i][position_j] ,  fill = "orange")
                cpt_D_ROUGE += 1
            else :
                grille[position_i][position_j] = BLEU
                canvas.itemconfigure( grille_canvas[position_i][position_j] ,  fill = "blue")
                cpt_D_ROUGE -= 1

        elif grille[position_i][position_j] == BLANC :
            if cpt_D_BLANC == 1 : 
                grille[position_i][position_j] = ORANGE
                canvas.itemconfigure( grille_canvas[position_i][position_j] ,  fill = "orange")
                cpt_D_BLANC += 1
            else :
                grille[position_i][position_j] = BLEU
                canvas.itemconfigure( grille_canvas[position_i][position_j] ,  fill = "blue")
                cpt_D_BLANC -= 1
        #le premier a gauche de la case blanche est donc orange et le deuxieme bleu

        if DIRECTION == NORD:
            DIRECTION = EST
            position_j = (position_j+1)%N
        elif DIRECTION == SUD:
            DIRECTION = OUEST
            position_j = (position_j-1)%N
        elif DIRECTION == EST:
            DIRECTION = SUD
            position_i = (position_i+1)%N
        elif DIRECTION == OUEST:
            DIRECTION = NORD
            position_i = (position_i-1)%N        
    
    elif grille[position_i][position_j] == BLEU or grille[position_i][position_j] == ORANGE :
        if grille[position_i][position_j] == ORANGE :
            if cpt_G_ORANGE == 1 :
                grille[position_i][position_j] = ROUGE
                canvas.itemconfigure( grille_canvas[position_i][position_j] ,  fill = "red")
                cpt_G_ORANGE += 1
            else :
                grille[position_i][position_j] = BLANC
                canvas.itemconfigure( grille_canvas[position_i][position_j] ,  fill = "white")
                cpt_G_ORANGE -= 1

        elif grille[position_i][position_j] == BLEU :
            if cpt_G_BLEU == 1 :
                grille[position_i][position_j] = ROUGE
                canvas.itemconfigure( grille_canvas[position_i][position_j] ,  fill = "red")
                cpt_G_BLEU += 1
            else :
                grille[position_i][position_j] = BLANC
                canvas.itemconfigure( grille_canvas[position_i][position_j] ,  fill = "white")
                cpt_G_BLEU -= 1
            #le premier a gauche de la case bleu est donc rouge et le deuxieme blanc

        if DIRECTION == NORD:
            position_j = (position_j-1)%N
            DIRECTION = OUEST   
        elif DIRECTION == SUD:
            position_j = (position_j+1)%N     
            DIRECTION = EST
        elif DIRECTION == EST:
            position_i = (position_i-1)%N
            DIRECTION = NORD
        elif DIRECTION == OUEST:
            position_i = (position_i+1)%N
            DIRECTION = SUD           

    normal,rapide,lent = False,False,False    
    couleurs = True  

    fourmi_update()


# les boutons --------------------------------------------------------------------------
button_play = Button (frame , text = ' Play  ', command = demarrer ) 
button_play.pack(padx= 10 , pady=10 )
Button (frame , text = ' Prochain ', command = next).pack(padx= 10 , pady=10 )
Button (frame , text = 'Retour', command = retour).pack(padx= 10 , pady=10 )
Button(frame, text="Enregistrer", command=enregistre).pack(padx= 10 , pady=10 )
Button(frame, text="Charger grille", command=charge_grille).pack(padx= 10 , pady=10 )
Button(frame, text="couleurs", command=couleur).pack(padx= 10 , pady=10 )


# affichage------------------------------------------------------------------------------
canvas.pack (side = RIGHT)
frame.place (x = 120 , y = 50)
canvas_image.place(x = 30 , y= 350)
label.pack()

initialisation()
environnement()
fourmi()

window.mainloop()