import os
import shutil
from datetime import datetime
import xmlschema
from .create_data_object_package import create_data_object_package
from .create_simple_trees import *
from .technical_functions import zip_creator


def create_sip(tree_ir, output, contenu, nom_ir):
    """Créée l'arbre complet du manifest, appelle d'autres fonctions pour les différents arbres internes,
    puis créé le .zip avec le manifest et les fichiers et vérifie de la validité du SIP construit.

        :param tree_ir: l'arbre de l'IR préalablement parsé par la libraire lxml
        :type tree_ir: object ElementTree

        :param output: Le chemin du dossier où le SIP sera sauvegardé
        :type output: str

        :param contenu: Le chemin du dossier où se trouvent les fichiers à verser
        :type contenu: str

        :param nom_ir: Le nom du fichier XML de l'IR
        :type nom_ir: str
        """
    # Je créé une variable qui correspond à l'ensemble de l'arbre du fichier XML EAD à partir de la balise racine du
    # fichier (<ead>)
    print("Lecture de l'arbre XML-EAD")
    root_ead = tree_ir.getroot()

    # Je commence à définir les espaces de nom qui seront en attribut de la racine du futur manifest
    xlink_namespace = 'http://www.w3.org/1999/xlink'
    pr_namespace = 'info:lc/xmlns/premis-v2'
    xsi_namespace = "http://www.w3.org/2001/XMLSchema-instance"
    xml_namespace = "http://www.w3.org/XML/1998/namespace"
    xsi = "{%s}" % xsi_namespace
    xml = "{%s}" % xml_namespace

    nsmap = {'xlink': xlink_namespace,
             'pr': pr_namespace,
             None: 'fr:gouv:culture:archivesdefrance:seda:v2.1',
             'xsi': xsi_namespace}

    # Je créé la racine de mon futur manifest (<ArchiveTransfer>) dans laquelle je passe tous mes espaces de nom et
    # attributs
    print("*Création de la racine ArchiveTransfer")
    root_sip = et.Element("ArchiveTransfer", nsmap=nsmap)
    root_sip.set(xsi + "schemaLocation", 'fr:gouv:culture:archivesdefrance:seda:v2.1 main.xsd')
    root_sip.set(xml + "id", "ID1")

    # Je créé le sous-élément <Comment> qui dépend de la balise racine et je lui donne comme valeur textuelle la valeur
    # de la balise <titleproper> du fichier EAD
    print("**Ajout de la balise Comment")
    comment = et.SubElement(root_sip, 'Comment')
    comment.text = "SIP " + root_ead.find('.//titleproper').text

    # Je créé le sous-élément <Date> qui dépend de la balise racine et je lui donne comme valeur textuelle la valeur
    # de la date au moment de la création du SIP que je mets en forme attendu par Adamant (AAAA-MM-JJTHH-mm-ss)
    print("**Ajout de la balise Date")
    date = et.SubElement(root_sip, 'Date')
    ce_jour = datetime.now()
    date.text = ce_jour.strftime("%Y-%m-%dT%H:%M:%S.%f")

    # Je créé le sous-élément <MessageIdentifier> qui dépend de la balise racine et je lui donne comme valeur
    # textuelle "SIP" suivit de la valeur de la balise <titleproper> du fichier EAD
    print("**Ajout de la balise MessageIdentifier")
    message_identifier = et.SubElement(root_sip, 'MessageIdentifier')
    message_identifier.text = "SIP " + root_ead.find('.//titleproper').text

    # Je créé le sous-élément <ArchivalAgreement> qui dépend de la balise racine et je lui donne comme valeur textuelle
    # "ArchivalAgreement0"
    print("**Ajout de la balise ArchivalAgreement")
    archival_agreement = et.SubElement(root_sip, 'ArchivalAgreement')
    archival_agreement.text = 'ArchivalAgreement0'

    # J'appelle la fonction create_code_list_versions qui provient du fichier create_simple_trees.py et qui renvoit
    # un arbre XML ayant pour racine <CodeListVersions>, je rattache cet arbre à la racine du SIP.
    print("**Ajout du sous-arbre CodeListVersions")
    code_list_versions = create_code_list_versions()
    root_sip.append(code_list_versions)

    # Je créé un dossier content dans le dossier de sortie où sera créé le SIP s'il n'existe pas déjà. Puis j'appelle
    # la fonction create_data_object_package qui provient du fichier create_data_object_package.py et qui renvoit un
    # arbre XML ayant pour racine <DataObjectPackage>, je rattache cet arbre à la racine du SIP.
    print("**Ajout du sous-arbre DataObjectPackage")
    dossiercontent = os.path.join(output, "content")
    if not (os.path.isdir(dossiercontent)):
        os.mkdir(dossiercontent)
    data_object_package = create_data_object_package(root_ead, contenu, dossiercontent)
    root_sip.append(data_object_package)

    # Je créé le sous-élément <TransferRequestReplyIdentifier> qui dépend de la balise racine et je lui donne comme
    # valeur textuelle "Identifier3" qui est la valeur par défaut avant enrichissement par Adamant.
    print("**Ajout de la balise TranserRequestReplyIdentifier")
    transfer_request_reply_identifier = et.SubElement(root_sip, 'TransferRequestReplyIdentifier')
    transfer_request_reply_identifier.text = 'Identifier3'

    # Je créé le sous-élément <ArchivalAgency> qui dépend de la balise racine, puis sa balise enfant <Identifier> et
    # je donne à celle-ci la valeur textuelle "Identifier4" qui est la valeur par défaut avant enrichissement par
    # Adamant.
    print("**Ajout de la balise ArchivalAgency et son enfant Identifier")
    archival_agency = et.SubElement(root_sip, 'ArchivalAgency')
    archival_agency_identifier = et.SubElement(archival_agency, 'Identifier')
    archival_agency_identifier.text = 'Identifier4'

    # Je créé le sous-élément <TransferringAgency> qui dépend de la balise racine, puis sa balise enfant <Identifier> et
    # je donne à celle-ci la valeur textuelle "Identifier5" qui est la valeur par défaut avant enrichissement par
    # Adamant.
    print("**Ajout de la balise TranserringAgency et son enfant Identifier")
    transferring_agency = et.SubElement(root_sip, 'TransferringAgency')
    transferring_agency_identifier = et.SubElement(transferring_agency, 'Identifier')
    transferring_agency_identifier.text = 'Identifier5'

    # J'indente l'arbre que je viens de créer, puis je le défini comme un élément Arbre. Je définis les options de
    # sauvegarde du fichier XML (son nom et son type d'écriture) puis j'utilise une fonction propre à la librairie
    # lxml pour créér ce fichier xml avec l'arbre et les options choisies. Puis je ferme le fichier ouvert lors de
    # son écriture.
    print("Création du manifest.xml...")
    et.indent(root_sip)
    doc_xml = et.ElementTree(root_sip)
    out_file = open(os.path.join(output, 'manifest.xml'), 'wb')
    doc_xml.write(out_file, xml_declaration=True, encoding='UTF-8', pretty_print=True)
    out_file.close()

    # J'utilise une fonction de création de .zip qui se trouve dans technical_functions.py et qui va copier et zipper
    # tout le contenu du dossier au nom de l'IR dans le dossier de sortie.
    print("Création de l'archive .zip...")
    zip_creator(output, os.path.join(output, 'SIP_' + nom_ir[:-4]))

    # Je supprime le dossier content où se trouvent les copies renommés des fichiers à verser maintenant qu'ils ont
    # été zippé (mais je garde le manifest.xml pour plus de souplesse)
    print("Suppression des fichiers copiés...")
    shutil.rmtree(dossiercontent)

    # Je lis le manifest que nous venons de créer...
    test_doc = et.parse(os.path.join(output, 'manifest.xml'))

    # Puis je le fais valider par le schéma de validation SEDA 2.1 qui se trouve dans le dossier
    # Ressources/Validation/seda_v2-1
    print("Tests de la conformité aux schémas de validations SEDA 2.1 et avant enrichissement ADAMANT...\n")
    schema = xmlschema.XMLSchema('./Ressources/Validation/seda_v2-1/main.xsd')

    # Si le XML n'est pas validé j'imprime dans la console un message d'erreur et je renvoie l'erreur que nous fait
    # remonter la libraire xmlschema et je passe à la prochaine validation. Si le XML est validé je renvoie un
    # message de confirmation.
    if not schema.is_valid(test_doc):
        print("Le manifest n'est pas conforme au schéma SEDA 2.1\n")
        try:
            schema.validate(test_doc)

        except xmlschema.validators.exceptions.XMLSchemaValidationError as e:
            print(e)
            pass
    else:
        print('Le manifest est conforme au schéma SEDA 2.1\n')

    # Puis je fais valider le XML par le schéma rng du profil minimum avant enrichissement d'Adamant. Si validé
    # j'envoie un message de validation, sinon j'envoie un message pour spécifier que l'XML n'est pas valide.
    if not test_doc.relaxng(et.parse("./Ressources/Validation/profil_minimum/avant_enrichissement.rng")):
        print("Le manifest n'est pas conforme au schéma avant enrichissement dans ADAMANT")
    else:
        print('Le manifest est conforme au schéma avant enrichissement dans ADAMANT')
