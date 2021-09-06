import os
import sys
from lxml import etree as et
import Ressources.app as app

if __name__ == '__main__':
    try:
        # Pour chaque dossier créé par l'utilisateur se trouvant dans Ressources/EAD, je créés une variable ir et
        # dossier_fichiers vide
        for dossierir in os.listdir("./Ressources/EAD"):
            ir = ""
            dossier_fichers = ""

            # Pour tout ce qui est contenu dans le dossier créé par l'utilisateur d'un IR, si son contenu est un
            # fichier c'est que c'est l'XML EAD donc je mets son nom dans la variable ir. Si c'est un dossier,
            # c'est que c'est le fichier de dossier et transfert son nom dans la variable dossier_fichiers.
            for contenu in os.listdir(os.path.join("./Ressources/EAD", dossierir)):
                if os.path.isfile(os.path.join("./Ressources/EAD", dossierir, contenu)):
                    ir = contenu
                elif os.path.isdir(os.path.join("./Ressources/EAD", dossierir, contenu)):
                    dossier_ir = contenu

            # Si il existe un fichier avec un dossier dans le dossier créé par l'utilisateur pour chaque IR : Alors
            # je récupère l'arbre XML du fichier ; Je créé le chemin du futur dossier de sortie (en l'appelant du nom
            # de l'IR moins son extension) ; et je récupère le chemin du dossier des fichiers fournis par l'utilisateur.
            if ir and dossier_ir:
                print('**********Traitement du fichier ' + ir + '**********')
                treeIR = et.parse(os.path.join("./Ressources/EAD", dossierir, ir))
                chemin_dossier_sortie = os.path.join("./Ressources/Out", ir)[:-4]
                chemin_content = os.path.join("./Ressources/EAD", dossierir, dossier_ir)

                # Si il n'existe pas déjà de dossier de sortie avec le nom que j'ai récupéré de l'XML, alors je créé
                # ce dossier
                if not (os.path.isdir(chemin_dossier_sortie)):
                    os.mkdir(chemin_dossier_sortie)

                # Puis j'appelle la fonction create_sip du fichier app.py et je lui passe l'arbre XML de l'IR,
                # le chemin du dossier de sortie, le chemin du dossier où se trouvent les fichiers et le nom du
                # fichier de l'IR. S'il n'y a pas eu d'erreur lors de la création du SIP je renvoie un message de
                # validation
                app.create_sip(treeIR, chemin_dossier_sortie, chemin_content, ir)
                print("\nL'opération s'est terminée avec succès, votre SIP se trouve dans Ressources/Out/" + ir[:-4])

            # Si dans le dossier fourni par l'utilisateur il n'y a pas d'IR ou pas de dossier contenu je renvoie un
            # message indiquant le problème sur l'invite de commande
            elif not ir:
                print("Il n'y a pas d'instruments de recherche dans le dossier " + dossierir)
            elif not dossier_ir:
                print("Il n'y a pas de dossier content dans le dossier " + dossierir)

    # try, except et finally gèrent le traitement des erreurs du programme.
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    finally:
        os.system("pause")
