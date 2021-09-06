import shutil

from lxml import etree as et

from Ressources.create_simple_trees import create_management_metadata
from Ressources.technical_functions import match_sf


def create_data_object_package(arbre_ead, dossier_source, dossier_copie):
    """Créée le sous-arbre DataObjectPackage, celui-ci ayant beaucoup de traitement vis-à-vis des fichiers et au
    niveau de la création de nombreuses balises, il m'a semblé plus clair de placer sa création dans une fonction
    dédiée, et de mettre cette fonction dans son propre fichier python. Elle appelle les fonctions de création de la
    balise DescriptiveMetadata et ManagementMetadata, ainsi que la fonction qui gère la lecture des métadonnées
    techniques via le programme Siegfried.

    :param arbre_ead: Le chemin du dossier où se trouvent les IRs
    :type arbre_ead: object ElementTree

    :param dossier_source: Le chemin du dossier où se trouvent les fichiers à verser.
    :type dossier_source: str

    :param dossier_copie: Le chemin du dossier où seront copier les fichiers à verser
    :type dossier_copie: str

    :returns: l'arbre XML ayant pour racine <DataObjectPackage>
    :rtype: object ElementTree
    """
    # Je créé l'élément racine <DataObjectPackage>
    arbre_data_object_package = et.Element("DataObjectPackage")

    # Je récupère des données formées en JSON qui correspondent à la liste des fichiers. Ce fichier nous ait envoyé
    # via la fonction match_sf qui se sert de Siegfried
    print("Identification des fichiers par Siegfried...")
    liste_fichiers = match_sf(dossier_source)

    # J'appelle la fonction de création du sous-arbre DescriptiveMetadata, et je sauvegarde ses valeurs de retour
    # dans deux variables qui récupèrent le dernier n° ID d'ArchiveUnit créé par la fonction et l'arbre ayant pour
    # racine <DescriptiveMetadata>
    noid, arbre_descriptive_metadata = create_descriptive_metadata(arbre_ead, liste_fichiers)

    print('Copie des fichiers versés dans le dossier content...')
    # Pour chaque fichiers traités dans la liste reçu de Siegfried...
    for fichier in liste_fichiers:
        # Si ce fichier Thumbs.db, je ne le traite pas.
        if 'Thumbs.db' not in fichier['filename']:
            # Sinon je récupère le nom du fichier (qui chez Siegfried correspond au chemin du fichier jusqu'à son
            # nom+extension. Je découpe cette chaîne de caractère au niveau des "\" et je ne récupère que la
            # dernière valeur découpée (qui correspond donc au nom du fichier).
            nom_fichier = fichier['filename'].split('\\')[-1]

            # Je créé une balise <DataObjectGroup>, j'ajoute +1 au n°ID récupéré, puis je met ce numéro ID en attribut
            # de la balise précédé de "ID".
            data_object_group = et.Element("DataObjectGroup")
            noid += 1
            data_object_group.attrib['id'] = 'ID' + str(noid)

            # Comme ce numéro ID est référencé dans les ArchiveUnit de niveau Item, ma solution a été de rechercher
            # dans l'arbre Descriptive metadata un élément qui s'appelle Title et pour valeur le nom du fichier.
            # Ayant récupéré cet objet je remonte ses parents jusqu'à avoir l'ArchiveUnit correspondante.
            copie_id = arbre_descriptive_metadata.xpath(('.//Title[text()="' + nom_fichier + '"]'))
            au_descript = copie_id[0].getparent().getparent()

            # Puis je rajoute à cette ArchiveUnit ma référence à l'ID du DataObjectGroup ici traité, symbolisé par
            # les balises <DataObjectReference> et <DataObjectGroupReferenceId> qui a pour valeur le numéro ID.
            data_object_reference = et.SubElement(au_descript, 'DataObjectReference')
            data_object_group_reference_id = et.SubElement(data_object_reference, 'DataObjectGroupReferenceId')
            data_object_group_reference_id.text = 'ID' + str(noid)

            # Je créé une balise <BinaryDataObject>, enfant de <DataObjectGroup>, j'ajoute +1 au n°ID, puis je met ce
            # numéro ID en attribut de la balise précédé de "ID".
            binary_data_object = et.SubElement(data_object_group, 'BinaryDataObject')
            noid += 1
            binary_data_object.attrib['id'] = 'ID' + str(noid)

            # Je créé une balise <DataObjectVersion>, enfant de <BinaryDataObject> qui aura pour valeur textuelle
            # "BinaryMaster_1"
            data_object_version = et.SubElement(binary_data_object, 'DataObjectVersion')
            data_object_version.text = 'BinaryMaster_1'

            # Je créé une balise <Uri>, enfant de <BinaryDataObject> qui aura pour valeur textuelle le chemin du
            # futur fichier copier dans content et qui se trouvera dans le SIP, le nom de ce fichier sera modifié
            # pour avoir le n° d'ID de l'objet.
            uri = et.SubElement(binary_data_object, 'Uri')
            uri.text = 'content/ID' + str(noid) + "." + fichier['filename'].split('.')[-1]

            # Je créé une balise <MessageDigest>, enfant de <BinaryDataObject> qui aura pour valeur textuelle la
            # valeur de l'empreinte calculée par le hash obtenu de Siegfried. Elle aura aussi pour attribut "SHA-512"
            # qui correspond au type de hash utilisé.
            message_digest = et.SubElement(binary_data_object, 'MessageDigest')
            message_digest.attrib['algorithm'] = 'SHA-512'
            message_digest.text = fichier['sha512']

            # Je créé une balise <Size>, enfant de <BinaryDataObject> qui aura pour valeur textuelle la taille du
            # fichier calculé par Siegfried.
            size = et.SubElement(binary_data_object, 'Size')
            size.text = str(fichier['filesize'])

            # Je créé une balise <FormatIdentification>, enfant de <BinaryDataObject>
            format_identification = et.SubElement(binary_data_object, 'FormatIdentification')

            # Et je lui rattache 3 balises, FormatLittéral, MimeType et FormatId, et qui auront pour valeur le nom du
            # format, le type Mime et le PUID, respectivement. Toutes ses valeurs sont obtenus par l'identification
            # du fichier par Siegfried.
            format_litteral = et.SubElement(format_identification, 'FormatLitteral')
            format_litteral.text = fichier['matches'][0]['format']

            mime_type = et.SubElement(format_identification, 'MimeType')
            mime_type.text = fichier['matches'][0]['mime']

            format_id = et.SubElement(format_identification, 'FormatId')
            format_id.text = fichier['matches'][0]['id']

            # Je créé une balise <FileInfo>, enfant de <BinaryDataObject>
            file_info = et.SubElement(binary_data_object, 'FileInfo')

            # Et je lui rattache deux balises, Filename et LastModified, et qui auront pour valeur le nom du fichier
            # que nous avions déjà mis en forme auparavant, la date de dernière modification obtenue par Siegfried.
            filename = et.SubElement(file_info, 'Filename')
            filename.text = nom_fichier

            last_modified = et.SubElement(file_info, 'LastModified')
            last_modified.text = fichier['modified'].split('+')[0]

            # Je prépare le nom du fichier qui sera copié, je lui donne comme nom ID+n°ID, puis je lui ajoute le nom
            # de l'extension obtenu via le nom du fichier original.
            nom_copie = 'ID' + str(noid) + "." + fichier['filename'].split('.')[-1]

            # Puis je procède à la copie, je vais chercher le fichier dans son chemin obtenu et je lui donne comme
            # chemin de copie le dossier content de l'IR traité + le nom que je viens de forger (la fonction de copy
            # créée le fichier si l'emplacement indiqué est vide ou le remplacera s'il existe déjà).
            shutil.copy(fichier['filename'], dossier_copie + '\\' + nom_copie)

            # Enfin une fois <DataObjectGroup> créé, je le rattache au noeud DataObjectGroupPackage.
            arbre_data_object_package.append(data_object_group)

    # Une fois tous les traitements sur les autres arbres terminés je rattache aussi au noeud
    # <DataObjectGroupPackage> <DescriptiveMetadata> et <ManagementMetadata>
    arbre_data_object_package.append(arbre_descriptive_metadata)
    arbre_data_object_package.append(create_management_metadata())

    # Enfin je retourne cette arbre vers la partie du code qui a appelée la fonction (a priori dans la création du
    # SIP dans app.py)
    return arbre_data_object_package


def create_descriptive_metadata(arbre_ead, liste_fichiers):
    """Créée le sous-arbre DescriptiveMetadata, j'ai préféré placé sa création proche de DataObjectPackage pour avoir
    les deux plus grosse fonctions ensembles dans un même fichier car les deux fonctions interagissent beaucoup
    ensemble, ceci permettant d'identifier plus rapidement les éventuels problèmes dans le code. Cette fonction fait
    un gros usage de la lecture de l'arbre XML en Ead pour copier son arborescence.

       :param arbre_ead: Le chemin du dossier où se trouvent les IRs
       :type arbre_ead: object ElementTree

       :param liste_fichiers: la liste des valeurs de chaque fichiers identifiés par Siegfried
       :type liste_fichiers: list

       :returns: l'arbre XML ayant pour racine <DescriptiveMetadata>
       :rtype: object ElementTree
    """
    # la variable portant le n°ID est créée à partir du n°10 comme ce qu'il se passe dans Resip. Puis je créé la
    # balise DescriptiveMetadata à laquelle je rattache l'ArchiveUnit qui sera l'UA racine. A cette UA racine
    # je donne l'attribut du n°ID créé précédement. Pour finir je créé une balise Content que je rattache à
    # cette UA racine.
    noid = 10
    arbre_descriptive_metadata = et.Element("DescriptiveMetadata")
    au_racine = et.SubElement(arbre_descriptive_metadata, 'ArchiveUnit')
    au_racine.attrib['id'] = 'ID' + str(noid)
    content_racine = et.SubElement(au_racine, 'Content')

    # Je créé et rattache une balise DescriptionLevel à Content qui a pour valeur "RecordGrp"
    lvl_racine = et.SubElement(content_racine, 'DescriptionLevel')
    lvl_racine.text = 'RecordGrp'

    # Puis un Title qui a pour valeur l'unittitle du did de l'archdesc du fichier EAD et qui correspond à l'UA racine.
    title_racine = et.SubElement(content_racine, 'Title')
    title_racine.text = arbre_ead.find('.//archdesc/did/unittitle').text

    # Je récupète tous le texte de scopecontent et de ses descendants de l'archdesc, si les balises existent et ont
    # du texte je créé une balise Description sous content avec les valeurs de ce texte, par contre j'enlève tout
    # type de mise en forme de ce texte. C'est a dire que le texte n'aura plus de tabulation ni de sauts de ligne ou
    # toute forme de caractère d'espacement multiple.
    scopetext = ''
    for element in arbre_ead.findall('.//archdesc/scopecontent//*'):
        if element.text is not None:
            scopetext += element.text
        scopetext += ' '
    # Si on a besoin de concaténer deux balises EAD on copie la boucle avec la même variable et on change juste le
    # chemin xpath en fonction de ce que l'on a besoin

    scopetext = ' '.join(scopetext.split())
    if scopetext:
        description_racine = et.SubElement(content_racine, 'Description')
        description_racine.text = scopetext

    # Je fais la même chose que la balise précédente mais avec custodhist et son équivalent SEDA :
    # CustodialHistory/CustodialHistoryItem
    custodtext = ''
    for element in arbre_ead.findall('.//archdesc/custodhist//*'):
        if element.text is not None:
            custodtext += element.text
        custodtext += ' '
    custodtext.join(custodtext.split())
    if custodtext:
        custod_racine = et.SubElement(content_racine, 'CustodialHistory')
        custoditem_racine = et.SubElement(custod_racine, 'CustodialHistoryItem')
        custoditem_racine.text = custodtext

    # J'ajoute à Content la référence au numéro FRAN_IR de l'instrument de recherche en le récupérant via la
    # balise eadid, dans les balise correspondante RelatedObjectReference/References/ExternalReference
    related_object_reference_racine = et.SubElement(content_racine, 'RelatedObjectReference')
    references_racine = et.SubElement(related_object_reference_racine, 'References')
    external_reference_racine = et.SubElement(references_racine, 'ExternalReference')
    external_reference_racine.text = arbre_ead.find('.//eadid').text

    # Pour finir j'ajoute au Content les dates extrêmes symbolisé par StartDate et EndDate, pour ce faire je récupère
    # la valeur de l'attribut 'normal' de unitdate dont la forme sera toujours homogène dans les IRs. Je découpe
    # la valeur de cette date au niveau du / pour récupérer la partie gauche qui correspond au StarDate et la partie
    # droite à l'EndDate. Puis je la met au format attendu par Adamant.
    start_date_racine = et.SubElement(content_racine, 'StartDate')
    end_date_racine = et.SubElement(content_racine, 'EndDate')
    date_extremes = arbre_ead.find('.//archdesc/did/unitdate').get('normal')
    date_extremes = date_extremes.replace(' ', '').split('/')
    start_date_racine.text = date_extremes[0] + 'T00:00:00'
    end_date_racine.text = date_extremes[1] + 'T23:59:00'

    # Je cherche la balise dsc et je récupère ses enfants. Pour chacun de ces enfants je les rattache eux
    # et leur arborescence à l'UA Racine.
    for child in arbre_ead.find('.//dsc').getchildren():
        au_racine.append(child)

    # Pour chacune des balises <c> copié de l'xml EAD que je trouve sous l'UA racine je change son nom en
    # ArchiveUnit.
    for c in au_racine.findall('.//c'):
        c.tag = "ArchiveUnit"

        # Je lui ajoute une balise Content avec la valeur RecordGrp dans DescriptionLevel qui est rattaché au
        # Content créé.
        content = et.Element('Content')
        c.insert(0, content)
        lvl = et.SubElement(content, 'DescriptionLevel')
        lvl.text = 'RecordGrp'

        # Je récupère le titre de l'unittitle propre au c copié. Que je copie dans une balise Title.
        title = et.SubElement(content, 'Title')
        title_text = ''
        for text in c.xpath('./did/unittitle/descendant-or-self::*/text()'):
            title_text += text
        title.text = ' '.join(title_text.split())

        # J'y ajoute son éventuel scopecontent dans une balise Description.
        scopetext = ''
        for element in c.findall('./scopecontent//*'):
            if element.text is not None:
                scopetext += element.text
            scopetext += ' '
        scopetext = ' '.join(scopetext.split())
        if scopetext:
            description = et.SubElement(content, 'Description')
            description.text = scopetext

        # Je récupère aussi les dates extrêmes de la balise unitdate et fais le même traitement que pour l'UA
        # Racine.
        start_date = et.SubElement(content, 'StartDate')
        end_date = et.SubElement(content, 'EndDate')
        date_extremes = c.find('./did/unitdate').get('normal')
        if '/' in date_extremes:
            date_extremes = date_extremes.replace(' ', '').split('/')
            start_date.text = date_extremes[0] + 'T00:00:00'
            end_date.text = date_extremes[1] + 'T23:59:00'
        else:
            start_date.text = date_extremes + 'T00:00:00'
            end_date.text = date_extremes + 'T23:59:00'

        # Enfin je supprime les attributs hérités des c copiés : id et level.
        c.attrib.pop("id", None)
        c.attrib.pop("level", None)

        # Je récupère l'unitid que je découpe au niveau des '/', ce qui me donne les différentes partie du numéro de
        # versement, je récupère l'article et j'y ajoute un rembourrage de 0 volontairement exagéré car je ne connais
        # pas la taille de rembourrage que l'article aura au niveau du nommage des fichiers.
        unitid = c.find('./did/unitid')
        versement = unitid.text.split('/')
        rembourrage_article = '0000000000000000' + versement[1]

        # Si la longueur total du texte se trouvant de unitid est inférieur ou égal à 16 caractères (donc si dans la
        # balise se trouve un intervalle de plusieurs articles sous la forme 20110288/6-20110288/12),
        # alors je considère que nous somme au dernier <ArchiveUnit> d'une branche de l'arborescence, donc je peux
        # intégrer à celle-ci les fichiers qui lui correspondent.
        if len(unitid.text) <= 16:

            # Pour tous les fichiers qui ont été traités par Siegfried, je découpe son nom pour n'avoir que le nom du
            # fichier, si le nom du fichier est Thumbs.db je ne le consèrve pas.
            for files in liste_fichiers:
                filename = files['filename'].split('\\')[-1]
                if 'Thumbs.db' not in filename:

                    # Je découpe encore le nom des autres fichiers au niveau des "_" et je récupère le numéro
                    # d'article de celui-ci qui est toujours à une place fixe grâce à la méthode de nomme des
                    # fichiers issus de Constance. Je récupère le numéro de versement obtenu dans l'unitid auquel
                    # j'ajoute le numéro d'article avec le rembourrage suffisant compté dans le nommage des fichiers
                    # (certain nom de fichiers Constance ont des rembourrages différents de 3 ou 4 caractères).
                    article_fichier = filename.split('_')[2]
                    versement_article = versement[0] + '_' + rembourrage_article[-len(article_fichier):]

                    # Si cet unitid modifié correspond à ce que l'on trouve dans le nom du fichier on créé un
                    # ArchiveUnit, content de niveau de Description "Item" et comme titre le nom du fichier d'origine.
                    if versement_article in filename:
                        au_item = et.SubElement(c, 'ArchiveUnit')
                        item_content = et.Element('Content')
                        au_item.insert(0, item_content)
                        lvl_item = et.SubElement(item_content, 'DescriptionLevel')
                        lvl_item.text = 'Item'
                        title_item = et.SubElement(item_content, 'Title')
                        title_item.text = filename
    # Enfin une fois tous ces traitements effectués je nettoie le reste des balises héritées de l'XML EAD. Pour
    # chaque ArchiveUnit je supprime les balises qui ne sont pas des Content ou d'autre ArchiveUnit, puis je lui
    # donne un attribut "id" que j'incrémente de 1 à chaque ArchiveUnit
    for autest in au_racine.findall('.//ArchiveUnit'):
        for child in autest.getchildren():
            if child.tag != 'Content' and child.tag != 'ArchiveUnit':
                child.getparent().remove(child)
        noid += 1
        autest.attrib['id'] = 'ID' + str(noid)

    # Pour finir, la fonction renvoie le dernier numéro ID et le sous-arbre DescriptiveMetadata.
    return noid, arbre_descriptive_metadata
