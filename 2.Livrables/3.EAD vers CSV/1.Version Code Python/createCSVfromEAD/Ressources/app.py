import os
import sys
import pandas as pd
import configparser
from lxml import etree as et


def create_csv(dossier_irs_xml: str, dossiersortie: str):
    """Récupère le dossier des IRs, les lits et créé un fichier csv à partir de ceux-ci

    :param dossier_irs_xml: Le chemin du dossier où se trouvent les IRs
    :type dossier_irs_xml: str

    :param dossiersortie: Le chemin du dossier où le fichier CSV sera sauvegardé
    :type dossiersortie: str
    """

    # Configuration et récupération des fichiers de configuration
    colonnes_config = configparser.ConfigParser()
    colonnes_config.read('colonnes.ini', encoding='utf-8-sig')
    csv_config = configparser.ConfigParser()
    csv_config.read('config.ini', encoding='utf-8-sig')

    # Création de listes vident qui contiendra les valeurs pour la construction du CSV
    list_value = []
    colonnes = []

    # Pour chaque sections se trouvant dans le fichier colonnes.ini j'ajoute le nom des sections dans la liste colonnes
    for nom_colonne in colonnes_config.sections():
        colonnes.append(nom_colonne)

    for ir in os.listdir(dossier_irs_xml):
        # Pour chaque IRs, je lis et extrais son arbre
        tree = et.parse(os.path.join(dossier_irs_xml, ir))
        ead = tree.getroot()

        # Puis je créés un index à valeur vide dans list_value
        list_value.append('')
        list_ir_value = []

        for nom_colonne in colonnes_config.sections():
            # Pour chaque nom de colonnes dans le fichier colonnes.ini si la valeur de l'option est égale à "texte"
            # Alors il récupère la valeur de ce texte, l'ajoute à la liste list_ir_value
            if 'texte' in colonnes_config[nom_colonne]:
                list_ir_value.append(colonnes_config[nom_colonne]['texte'])
            #Si la valeur est égale à "xpath" il essaye de récupérer sa valeur
            elif 'xpath' in colonnes_config[nom_colonne]:
                texte_balise = ''
                try:
                    for element in ead.findall(colonnes_config[nom_colonne]['xpath']):
                        # Si la valeur du texte de l'élément n'est pas vide il la récupère et l'ajoute à la variable
                        # texte
                        if element.text is not None:
                            texte_balise += ' '.join(element.text.split())

                        # Si le texte se trouve dans une balise <p> ou <item> d'une list alors il récupère le
                        # caractère de séparation entre les valeurs de chaque balise défini par l'utilisateur.
                        if element.tag == 'p' or element.tag == 'item':
                            if csv_config['Configuration']['séparation des balises texte'] == 'saut':
                                texte_balise += '\n'
                            elif csv_config['Configuration']['séparation des balises texte'] == 'espace':
                                texte_balise += ' '
                            elif csv_config['Configuration']['séparation des balises texte'] == 'tabulation':
                                texte_balise += '\t'
                            else:
                                texte_balise += csv_config['Configuration']['séparation des balises texte']
                    # Enfin on ajoute ce texte récupéré à la liste des valeurs de l'IRs
                    list_ir_value.append(texte_balise)
                except SyntaxError as e:
                    print(
                        "Vous n'avez pas rentré d'Xpath valide dans la section " + nom_colonne + " du fichier colonnes.ini")
                    os.system("pause")
                    sys.exit(1)
        # Pour finir on ajoute la liste des valeurs de l'IR dans la liste des valeurs au dernier index créé (càd
        # l'IR en cours)
        list_value[-1] = list_ir_value

    # Création du tableau de données à laquelle on donne la liste des valeurs, le nom des colonnes et on définit
    # l'index comme la première colonne de la liste (sinon le module crééra une colonne Index)
    tableau_ead = pd.DataFrame(list_value, columns=colonnes).set_index(colonnes[0])

    # Transformation du tableau de données en fichier CSV avec les options choisie dans config.ini par rapport au
    # séparateur ou au nom du fichier. Pour des questions de simplification, l'encodage se fera en utf8-sig qui est
    # propre à Windows
    tableau_ead.to_csv(os.path.join(dossiersortie, csv_config['Configuration']['nom du fichier de sortie']),
                       sep=csv_config['Configuration']['séparateur'], encoding='utf-8-sig')
