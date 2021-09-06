import json
import os
import subprocess
import sys
import zipfile


def match_sf(chemin_fichier):
    """Fonction qui utilise une commande systeme via le programme Siegfried. Cette commande va regarder dans un
    dossier donné tous les fichiers, même si ceux-ci sont dans d'autres dossiers, et va faire remonter les
    informations identifiés par Siegfried au format JSON. Ce qui pourra être facilement récupéré par Python par la
    suite.

    :param chemin_fichier: Le chemin du dossier où se trouvent les fichiers à verser.
    :type chemin_fichier: str

    :returns: La liste de tous les fichiers et de leurs informations techniques obtenue par l'identification de Siegfried
    :rtype: list
    """
    # la commande de Siegfried, comme l'utilisateur n'a probablement pas de variable d'environnement propre à
    # Siegfried j'indique dans ma commande le chemin dans lequel se trouve l'exe de Siegfried, puis je lui passe le
    # paramètre -json pour avoir une réponse en json puis le paramètre-hash pour que Siegfried calcul l'empreinte du
    # fichier, enfin j'indique le chemin du dossier où se trouvent les fichiers. (pour plus d'informations sur les
    # commandes Siegfried je vous invite à visiter le GitHub du projet : https://github.com/richardlehane/siegfried
    cmd = [".\\Ressources\\sf", "-json", "-hash", "sha512", chemin_fichier]

    # Tentative d'utilisation de la commande via le subprocess et récupération de l'output dans une variable.
    try:
        sf_json = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        print("Impossible de lancer Siegfried. Est-il dans les ressources ou le chemin indiqué pour les fichiers "
              "est-il le bon?")
        sys.exit(1)

    # Une fois les informations extraites je les intérprète via Python et le module json, puis je ne récupère que la
    # liste de tous les fichiers et leurs informations et je l'envoie vers la partie de code qui a appelée la
    # fonction. Le reste des informations sont des informations techniques proprent à Siegfried.
    sf_data = json.loads(sf_json)
    match = sf_data["files"]
    return match


def zip_creator(src, dst):
    """Fonction qui va créer un fichier .zip avec tous le contenu trouvé dans un dossier vers un chemin indiqué.

        :param src: Le chemin du dossier de l'IR où se trouve le manifest est les copie des fichiers à verser dans un
        dossier content.
        :type src: str

        :param dst: Le chemin où sera créé le .zip
        :type dst: str
        """
    zf = zipfile.ZipFile("%s.zip" % dst, "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            if '.zip' not in filename:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                zf.write(absname, arcname)
    zf.close()
