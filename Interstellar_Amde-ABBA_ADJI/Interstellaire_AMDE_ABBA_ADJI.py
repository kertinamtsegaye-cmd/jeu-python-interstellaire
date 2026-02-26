import random
import pygame
import time
import os


from random import randint

pygame.font.init()
pygame.init()
pygame.mixer.init()

HAUTEUR = 650
LARGEUR = 1300
TUNNEL_SEG_LARGEUR = 40
tunnel = []
HAUTEUR_MIN = 300
HAUTEUR_MAX = 400
niveau = 1
REDUCTION_TUNNEL = 0
FREQUENCE_ENNEMI = 4
VITESSE_ENNEMI_BONUS = 0


#Sons
son_laser=pygame.mixer.Sound("audio_interstellar/laser.mp3")
son_alien_tir=pygame.mixer.Sound("audio_interstellar/alien tir.mp3")
son_explosion=pygame.mixer.Sound("audio_interstellar/collision.mp3")
son_gameover=pygame.mixer.Sound("audio_interstellar/GameOver.mp3")
pygame.mixer.music.load("audio_interstellar/audio_bg.mp3")
pygame.mixer.music.play(-1)
son_collect=pygame.mixer.Sound("audio_interstellar/bouclier.mp3")
#Ecran d'acceuil

fond_ecran=pygame.image.load("images_interstellar/fond_ecran.png")
fond_ecran=pygame.transform.scale(fond_ecran,(LARGEUR,HAUTEUR))
nom_joueur=""

#Ecran fin
fond_fin=pygame.image.load("images_interstellar/Game OVER.jpg")
def ecran_acceuil():
    nom=""
    attente= True
    clic_actif=False

    nom_rect=pygame.Rect(0 ,0,300,50)
    nom_rect.center=(LARGEUR//2,300)

    pygame.mixer.music.stop()
    pygame.mixer.music.load("audio_interstellar/debut.mp3")
    pygame.mixer.music.play(-1)

    while attente:
        fen.blit(fond_ecran,(0,0))
        couleur_boite = (100, 149, 237) if clic_actif else (70, 70, 70)
        titre= FONT.render("INTERSTELLAR",1,(0,255,255))
        texte_Instructions = FONT.render("Tapez votre nom :",1,(255,215,0))
        texte_nom= FONT.render(nom,1,(255,255,255))
        texte_entrer= FONT.render("Cliquez ICI pour jouer :",1,(0,255,0))


        fen.blit(titre, titre.get_rect(center=(LARGEUR // 2, 100)))
        fen.blit(texte_Instructions, texte_Instructions.get_rect(center=(LARGEUR // 2 , 250)))
        bouton_jouer_rect = texte_entrer.get_rect(center=(LARGEUR // 2, 450))

        pygame.draw.rect(fen, (25, 25, 25), nom_rect)
        pygame.draw.rect(fen, couleur_boite, nom_rect, 3)
        fen.blit(texte_nom, texte_nom.get_rect(center=nom_rect.center))

        pygame.draw.rect(fen, (20, 20, 20), bouton_jouer_rect.inflate(20,10))  # Fond du bouton
        pygame.draw.rect(fen, (34, 139, 34), bouton_jouer_rect.inflate(20,10), 3)  # Bordure
        fen.blit(texte_entrer, bouton_jouer_rect)


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Pour bien arrêter le script

            if event.type == pygame.MOUSEBUTTONDOWN:
                if nom_rect.collidepoint(event.pos):
                    clic_actif=True
                elif bouton_jouer_rect.collidepoint(event.pos) and len(nom) > 0:
                    attente = False
                else:
                    clic_actif=False
            if event.type == pygame.KEYDOWN:
                if clic_actif:
                    if event.key == pygame.K_BACKSPACE:
                        nom = nom[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(nom) > 0:
                            attente = False
                    elif event.unicode.isprintable():
                        if len(nom) < 15:
                            nom += event.unicode
    pygame.mixer.music.stop()
    return nom


FONT = pygame.font.SysFont("Times New Roman", 30)
#pour charger la fenetre
fen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Interstellar")

# Fond étoilé
fond = pygame.image.load("images_interstellar/starbg.png")
fond = pygame.transform.scale(fond, (LARGEUR, HAUTEUR))

# Images
joueur_img = pygame.image.load("images_interstellar/spaceRocket.png")
#les images dans le jeu
laser_img = pygame.image.load("images_interstellar/Laser.png")
laser_img = pygame.transform.scale(laser_img, (40, 10))
alien = pygame.image.load("images_interstellar/alien.png")
alien2= pygame.image.load("images_interstellar/alien2.png")
tunnel_img = pygame.image.load("images_interstellar/tunnel.png")
asteroid50= pygame.image.load("images_interstellar/asteroid50.png")
asteroide100=pygame.image.load("images_interstellar/asteroid100.png")
asteroide150=pygame.image.load("images_interstellar/asteroid150.png")
bouclier_img=pygame.image.load("images_interstellar/Bouclier.png")
bouclier_img=pygame.transform.scale(bouclier_img, (60, 60))
diament_img=pygame.image.load("images_interstellar/Diament.png")
diament_img=pygame.transform.scale(diament_img, (60, 60))
tunnel_largeur=tunnel_img.get_width()

# Variables de départ corrigées pour la jouabilité
joueur_x = LARGEUR // 2
joueur_y = HAUTEUR // 2
vitesse_vaisseau = 8
ennemis=[]
laser_vitesse = 10
lasers = []
#ajouter plus tard vitesse de laser differentes par niveau

def init_tunnel():
    y_haut = (HAUTEUR - 400) // 2
    y_bas = y_haut + 400
    for i in range(LARGEUR // TUNNEL_SEG_LARGEUR + 2):# creer assez de segment de tunnel  pour couvrir l'ecran
        tunnel.append([y_haut, y_bas])


def update_tunnel(reduction,mouvements):
    tunnel.pop(0) # pour faire defiler le tunnel
    y_haut, y_bas = tunnel[-1]
    y_haut += random.randint(-mouvements, mouvements)# pour rendre le tunnel plus mouvementé dependant le niveau
    y_bas += random.randint(-mouvements, mouvements)
    min_taille = HAUTEUR_MIN - reduction
    if min_taille < 100:
        min_taille = 100
    taille= y_bas-y_haut
    if taille<min_taille:
        taille = min_taille
    if taille>HAUTEUR_MAX:
        taille = HAUTEUR_MAX
    if y_haut<20:
        y_haut = 20
    limite_basse=HAUTEUR-taille-100 # pour avoir assez de place pour le vaisseau
    if y_haut> limite_basse:
        y_haut = limite_basse
    y_bas = y_haut + taille
    tunnel.append([y_haut, y_bas])


def draw_tunnel():
    x = 0
    for y_haut, y_bas in tunnel:
        hauteur_segment = y_bas - y_haut
        zone_de_coupe = pygame.Rect(0, 0, TUNNEL_SEG_LARGEUR, hauteur_segment)
        fen.blit(tunnel_img, (x, y_haut), zone_de_coupe)
        x += TUNNEL_SEG_LARGEUR


def creer_ennemi(vitesse_bonus):
    type_ennemi = random.choice(["alien", "alien2","asteroid50", "asteroid100", "asteroid150"])
    if type_ennemi == "alien":
        img = alien
        vitesse = random.randint(3, 5)
    elif type_ennemi =="alien2":
        img= alien2
        vitesse = random.randint(3, 5)
    elif type_ennemi == "asteroid50":
        img = asteroid50
        vitesse = random.randint(6, 8)
    elif type_ennemi == "asteroid100":
        img = asteroide100
        vitesse = random.randint(5, 7)
    else:
        img = asteroide150
        vitesse = random.randint(3, 5)

    ennemi = {"img": img, "x": LARGEUR, "y": random.randint(60, HAUTEUR - 60), "v": vitesse + vitesse_bonus,"type":type_ennemi,"timer_tir":0,"est_en_morceau":False,"dans_tunnel": False}
    return ennemi


def collision_tunnel(jx, jy):
    rect_vaisseau = pygame.Rect(jx, jy, joueur_img.get_width(), joueur_img.get_height())
    x = 0

    for y_haut, y_bas in tunnel:
        rect_plafond = pygame.Rect(x, 0, TUNNEL_SEG_LARGEUR, y_haut)
        rect_sol = pygame.Rect(x, y_bas, TUNNEL_SEG_LARGEUR, HAUTEUR - y_bas)
        if rect_vaisseau.colliderect(rect_plafond) or rect_vaisseau.colliderect(rect_sol):
            return True
        x += TUNNEL_SEG_LARGEUR
    return False

def collision_laser_ennemi(laser,ennemi):
    laser_rect=pygame.Rect(laser[0],laser[1],laser_img.get_width(),laser_img.get_height())
    ennemi_rect=pygame.Rect(ennemi["x"],ennemi["y"],ennemi["img"].get_width(),ennemi["img"].get_height())
    return laser_rect.colliderect(ennemi_rect)

def collision_vaisseau_ennemi(jx,jy,ennemis,vies):
    vaisseau_rect=pygame.Rect(jx,jy,joueur_img.get_width(),joueur_img.get_height())
    for e in ennemis:
        ennemi_rect = pygame.Rect(e["x"], e["y"], e["img"].get_width(), e["img"].get_height())
        if vaisseau_rect.colliderect(ennemi_rect):
            ennemis.remove(e)
            vies-=1
            vie_progressive = 1.0
            etat_batterie=0
            print(f"Vies Restantes: {vies}")
    return vies

def afficher_batteries(vies):
    largeur = 30
    hauteur = 12
    espace = 8
    x_depart = 30
    y = 70
    nombre_batteries_pleines = int(vies)
    for i in range(nombre_batteries_pleines):
        pygame.draw.rect(fen, (0, 255, 0), (x_depart + i * (largeur + espace), y, largeur, hauteur),
                         border_radius=3)
    reste = vies - nombre_batteries_pleines

    if reste > 0.6:
        couleur = (0, 255, 0)
    elif reste > 0.3:
        couleur = (255, 165, 0)
    else:
        couleur = (255, 0, 0)

    pos_x = x_depart + nombre_batteries_pleines * (largeur + espace)
    pygame.draw.rect(fen, couleur, (pos_x, y, largeur, hauteur), border_radius=3)



def niveau_jeu(niveau):
    if niveau == 1:
        vitesse_bonus = 0
        reduction_tunnel = 50
        frequence_ennemi = 80
        mouv_tunnel=25
    elif niveau == 2:
        vitesse_bonus = 3
        reduction_tunnel = 120
        frequence_ennemi = 70
        mouv_tunnel=40

    else:
        vitesse_bonus = 4
        reduction_tunnel = 150
        frequence_ennemi =20
        mouv_tunnel=40

    return frequence_ennemi, vitesse_bonus, reduction_tunnel,mouv_tunnel


def dessiner_bouclier_anime(x_joueur, y_joueur, temps_jeu):
    pulsation = (pygame.time.get_ticks() // 100) % 10  # Oscille entre 0 et 10
    taille = 140 + pulsation * 2

    # On centre le bouclier sur le vaisseau
    centre_x = x_joueur + joueur_img.get_width() // 2
    centre_y = y_joueur + joueur_img.get_height() // 2

    surf_bouclier = pygame.transform.scale(bouclier_img, (int(taille), int(taille)))

    # Optionnel : Faire tourner un peu le bouclier pour l'effet "énergie"
    angle = (pygame.time.get_ticks() // 20) % 360
    surf_bouclier = pygame.transform.rotate(surf_bouclier, angle)

    # On gère la transparence (effet de scintillement)
    opacite = 150 + pulsation * 10
    surf_bouclier.set_alpha(opacite)

    # On affiche au centre
    rect = surf_bouclier.get_rect(center=(centre_x, centre_y))
    fen.blit(surf_bouclier, rect.topleft)

def charger_scores():
    liste_scores=[]
    if os.path.exists('scores.txt'):
        sauvegarde=open('scores.txt','r')
        for ligne in sauvegarde:
            separer=ligne.split(":")
            score=round(float(separer[0]))
            nom_score=separer[1].strip()
            liste_scores.append([score,nom_score])
        sauvegarde.close() # sinon le fichier ne se ferme pas
    return liste_scores
def sauvegarde_score(nouveau_score,nom_joueur):
    score=charger_scores()
    score.append([nouveau_score,nom_joueur])
    score.sort(reverse=True)

    with open('scores.txt','w') as sauvegarde:
        for i in range(len(score)):
            if i<3:
                sauvegarde.write(f"{score[i][0]}:{score[i][1]}\n")


def  ecran_fin(score_final):
    son_gameover.play()
    top_scores=charger_scores()
    image_fin=pygame.transform.scale(fond_fin,(LARGEUR,HAUTEUR))
    attente= True
    while attente:
        fen.blit(image_fin,(0,0))
        texte_score=FONT.render(f"Score Final: {round(score_final)}", 1, (25,25,12))
        fen.blit(texte_score, texte_score.get_rect(center=(LARGEUR//2,150)))

        #Affichage TOP 3
        meilleurs_joueurs=FONT.render(" LES MEILLEURS JOUEURS :",1,(0,53,71))
        fen.blit(meilleurs_joueurs,meilleurs_joueurs.get_rect(center=(LARGEUR//2,350)))

        y_pos=400
        for i in range(len(top_scores)):
            if i < 3:
                nom_joueur=top_scores[i][1]
                score=top_scores[i][0]

                ligne=FONT.render(f"{nom_joueur}:{score} pts",1,(16,16,16))
                fen.blit(ligne,ligne.get_rect(center=(LARGEUR//2,y_pos)))
                y_pos+=50

        texte_retour=FONT.render("Tapez entrer pour quitter",1,(0,49,83))
        fen.blit(texte_retour, texte_retour.get_rect(center=(LARGEUR//2,600)))


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        attente = False





def main(joueur_x, joueur_y,nom_joueur):
    init_tunnel()
    clock = pygame.time.Clock()
    temps_debut = time.time()
    VIES_MAX=20
    vies = VIES_MAX
    vie_progressive=1.0
    niveau = 1
    FREQUENCE_ENNEMI, VITESSE_ENNEMI_BONUS, REDUCTION_TUNNEL, MOUVEMENTS = niveau_jeu(niveau)
    cpt_ennemi = 0
    pause=False
    joue = True
    cpt_tunnel=0
    vitesse_defilement=3#plus nbr grand plus le tunnel est lent
    score_final=0
    lasers_ennemis=[]
    bouclier_actif=False
    etat_batterie=0#0=normal,1=abimé 2=Critique
    boucliers_stock=0
    boucliers=[]
    diaments=[]
    joueur_actif=True


    pygame.mixer.music.load("audio_interstellar/audio_bg.mp3")
    pygame.mixer.music.play(-1)

    while joue:
        clock.tick(35)
        temps_ecoule = time.time() - temps_debut

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                joue = False

        # --- MOUVEMENTS ---
        touches = pygame.key.get_pressed()
        ancien_y=joueur_y
        ancien_x=joueur_x
        bouclier_actif=False
        if touches[pygame.K_UP] and joueur_y - vitesse_vaisseau > 0:
            joueur_y -= vitesse_vaisseau
        if touches[pygame.K_DOWN] and joueur_y + joueur_img.get_height() < HAUTEUR:
            joueur_y += vitesse_vaisseau
        # Déplacement horizontal
        if touches[pygame.K_LEFT] and joueur_x - vitesse_vaisseau > 0:
            joueur_x -= vitesse_vaisseau
        if touches[pygame.K_RIGHT] and joueur_x + joueur_img.get_width() < LARGEUR:
            joueur_x += vitesse_vaisseau
        # Tir
        if touches[pygame.K_SPACE]:
            laser_x = joueur_x + joueur_img.get_width()
            laser_y = joueur_y + joueur_img.get_height() // 2 - laser_img.get_height() // 2
            lasers.append([laser_x, laser_y])
            son_laser.play()
        #Pause
        if touches[pygame.K_RETURN]:
            if pause==False:
                pause=True
            else:
                pause=False

        if touches[pygame.K_RSHIFT] and boucliers_stock > 0:
            bouclier_actif = True
        else:
            bouclier_actif = False



        if not pause:

            idx = int(joueur_x // TUNNEL_SEG_LARGEUR)
            if 0 <= idx < len(tunnel):
                y_haut = tunnel[idx][0]
                y_bas = tunnel[idx][1]

                if joueur_y < y_haut:
                    joueur_y = y_haut
                    vies -= 0.05
                if joueur_y + joueur_img.get_height() > y_bas:
                    joueur_y = y_bas - joueur_img.get_height()
                    vies -= 0.05
            #pour ralentir le tunnel
            cpt_tunnel+=1
            if cpt_tunnel>=vitesse_defilement:
                update_tunnel(REDUCTION_TUNNEL, MOUVEMENTS)
                cpt_tunnel=0
            # --- LOGIQUE LASERS
            for l in lasers:
                l[0] += 15
                detruire_laser = False
                if l[0] > LARGEUR:
                    lasers.remove(l)
                    detruire_laser = True
                for e in ennemis:
                    if detruire_laser == False:
                        rect_laser = pygame.Rect(l[0], l[1], 20, 10)
                        rect_ennemi = pygame.Rect(e["x"], e["y"], e["img"].get_width(), e["img"].get_height())
                        if rect_laser.colliderect(rect_ennemi):
                            if "asteroid" in e["type"] and not e["est_en_morceau"]:
                                son_explosion.play()
                                for i in range(3):
                                    morceau={"img":pygame.transform.scale(e["img"],(15,15)), "x":e["x"], "y":e["y"],"v":e["v"]+ random.randint(1,3),"v_y":random.randint(-5,5),"type":"morceau","est_en_morceau":True, "timer_tir":0,"dans_tunnel":True} #e["v"] : vitesse horzontale de ennemi "v_y" vitesse verticale pour e morceau
                                    ennemis.append(morceau)
                            ennemis.remove(e)
                            lasers.remove(l)
                            detruire_laser = True


            # --- ENNEMIS ---
            cpt_ennemi += 1
            if cpt_ennemi > FREQUENCE_ENNEMI:
                ennemis.append(creer_ennemi(VITESSE_ENNEMI_BONUS))
                cpt_ennemi = 0

            for e in ennemis:
                e["x"] -= e["v"] #l'ennemi avance vers le joueur

                if e["est_en_morceau"]:
                    e["y"] += e["v_y"]


                if e["type"]=="alien" or e["type"]=="alien2" and niveau>=2:
                    e["timer_tir"]+=1
                    if e["timer_tir"]> 50:
                        lasers_ennemis.append([e["x"],e["y"]+20])
                        e["timer_tir"]=0


                abscisse = int(e["x"] // TUNNEL_SEG_LARGEUR)
                if 0 < abscisse < len(tunnel):
                    y_haut, y_bas = tunnel[abscisse]
                    centre_tunnel = (y_haut + y_bas) // 2
                    if not e["dans_tunnel"]:
                        if e["y"] < centre_tunnel:
                            e["y"] += 2
                        elif e["y"] > centre_tunnel:
                            e["y"] -= 2
                    else:
                        y_haut < e["y"] < y_bas - e["img"].get_height()


                if e["x"] < -e["img"].get_width(): # si le point le plus a droite a disparu l'ennemi est hors ecran
                    ennemis.remove(e)
                if e["y"] < y_haut:
                    e["y"] = y_haut
                    if e["est_en_morceau"]: e["v_y"] *= -1  # Inversion de direction pour rebondir

                if e["y"] + e["img"].get_height() > y_bas:
                    e["y"] = y_bas - e["img"].get_height()
                    if e["est_en_morceau"]: e["v_y"] *= -1
            if random.randint(0, 300) == 0:
                boucliers.append({"x": LARGEUR,"y": random.randint(y_haut,  y_bas),"v": 3})
            if random.randint(0, 400) == 0:
                diaments.append({"x": LARGEUR,"y": random.randint(y_haut,  y_bas),"v": 3})

            # --- BOUCLIERS ---
            for b in boucliers:
                b["x"] -= b["v"] # vers gauche

                rect_b = pygame.Rect(b["x"], b["y"], 40, 40)
                rect_j = pygame.Rect(joueur_x, joueur_y,joueur_img.get_width(),joueur_img.get_height())

                if rect_b.colliderect(rect_j):
                    boucliers_stock += 1
                    son_collect.play()
                    boucliers.remove(b)

                elif b["x"] < -40:
                    boucliers.remove(b)
            for d in diaments:
                # Déplacement
                d["x"] -= d["v"]

                # Rectangles pour collision
                rect_d = pygame.Rect(d["x"], d["y"], diament_img.get_width(), diament_img.get_height())
                rect_j = pygame.Rect(joueur_x, joueur_y, joueur_img.get_width(), joueur_img.get_height())

                # Collision avec le joueur
                if rect_d.colliderect(rect_j):
                    if vies < VIES_MAX:
                        vies += 1  # augmente les vies directement
                    diaments.remove(d)

                # Sortie de l'écran
                elif d["x"] < -diament_img.get_width():
                    diaments.remove(d)

            vies = collision_vaisseau_ennemi(joueur_x, joueur_y, ennemis, vies)
            if vies <= 0:
                son_gameover.play()
                pygame.display.update()
                pygame.time.delay(1000)
                print("Vous avez perdu ! ")
                joue = False

            for l in lasers_ennemis:
                l[0] -= 10
                rect_l=pygame.Rect(l[0], l[1], 35, 15)
                rect_j=pygame.Rect(joueur_x, joueur_y, joueur_img.get_width(), joueur_img.get_height())

                if rect_l.colliderect(rect_j):
                    if bouclier_actif and boucliers_stock > 0:
                        boucliers_stock -= 1
                    else:
                        vies -= 1
                    son_alien_tir.play()
                    lasers_ennemis.remove(l)

            if temps_ecoule > 30 and niveau == 1:
                niveau = 2
                FREQUENCE_ENNEMI, VITESSE_ENNEMI_BONUS, REDUCTION_TUNNEL, MOUVEMENTS= niveau_jeu(niveau)
            if temps_ecoule > 60 and niveau == 2:
                niveau = 3
                FREQUENCE_ENNEMI, VITESSE_ENNEMI_BONUS, REDUCTION_TUNNEL, MOUVEMENTS = niveau_jeu(niveau)

            # AFFICHAGE
            fen.blit(fond, (0, 0))  # Fond étoilé fixe
            draw_tunnel()
            for b in boucliers:
                fen.blit(bouclier_img, (b["x"], b["y"]))

            fen.blit(joueur_img, (joueur_x, joueur_y))
            if bouclier_actif:
                dessiner_bouclier_anime(joueur_x, joueur_y, temps_ecoule)


            for d in diaments:
                fen.blit(diament_img, (d["x"], d["y"]))

            for e in ennemis:
                fen.blit(e["img"], (e["x"], e["y"]))

            # Affichage des lasers
            for l in lasers:
                fen.blit(laser_img, (l[0], l[1]))
            for l in lasers_ennemis:
                pygame.draw.rect(fen,(255,0,0),rect_l)


            # Texte info
            texte_temps = FONT.render(f"Temps:{round(temps_ecoule)}", 1, (255, 255, 255))
            texte_niveau = FONT.render(f"Niveau:{niveau}", 1, (255, 255, 255))
            afficher_batteries(vies)
            texte_bouclier = FONT.render(f"Bouclier : {boucliers_stock}", 1, (0, 200, 255))
            fen.blit(texte_bouclier, (30, 90))

            fen.blit(texte_temps, (30, 30))
            fen.blit(texte_niveau, (LARGEUR - texte_niveau.get_width() - 10, 10))

            score=float(time.time() - temps_debut)
            score_final=score

        else:
            texte_pause=FONT.render("Pause (Appuyez sur Entrer pour Continuer ", 1, (255, 255, 255))
            fen.blit(texte_pause, (300, 200))
        pygame.display.update()
    pygame.mixer.music.stop()

    sauvegarde_score(score_final,nom_joueur)
    return score_final
NOM=ecran_acceuil()
score_FIN=main(joueur_x, joueur_y,NOM)
ecran_fin(score_FIN)
pygame.quit()

