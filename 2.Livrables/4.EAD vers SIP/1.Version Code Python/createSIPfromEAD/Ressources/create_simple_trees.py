from lxml import etree as et


def create_code_list_versions():
    """Créée le sous-arbre CodeListVersions, celui-ci ayant toujours les mêmes valeurs il m'a semblé plus simple de
    le créer à la volée dans une petite fonction dédiée qui ne prend aucun paramètre mais renvoie un objet de la
    class ElementTree propre à la librairie lxml.

    :returns: l'arbre XML ayant pour racine <CodeListVersions>
    :rtype: object ElementTree
    """
    # Création de l'élement racine <CodeListVersions>
    arbre_code_list_versions = et.Element("CodeListVersions")

    # Je créé le sous-élément <ReplyCodeListVersion> enfant de la balise <CodeListVersions> et je lui donne comme valeur
    # textuelle "ReplyCodeListVersion0"
    reply_code_list_version = et.SubElement(arbre_code_list_versions, 'ReplyCodeListVersion')
    reply_code_list_version.text = 'ReplyCodeListVersion0'

    # Je créé le sous-élément <MessageDigestAlgorithmCodeListVersion> enfant de la balise <CodeListVersions> et je
    # lui donne comme valeur textuelle "MessageDigestAlgorithmCodeListVersion0"
    message_digest_algorithm_code_list_version = et.SubElement(arbre_code_list_versions,
                                                               'MessageDigestAlgorithmCodeListVersion')
    message_digest_algorithm_code_list_version.text = 'MessageDigestAlgorithmCodeListVersion0'

    # Je créé le sous-élément <MimeTypeCodeListVersion> enfant de la balise <CodeListVersions> et je
    # lui donne comme valeur textuelle "MimeTypeCodeListVersion0"
    mime_type_code_list_version = et.SubElement(arbre_code_list_versions, 'MimeTypeCodeListVersion')
    mime_type_code_list_version.text = 'MimeTypeCodeListVersion0'

    # Je créé le sous-élément <EncodingCodeListVersion> enfant de la balise <CodeListVersions> et je
    # lui donne comme valeur textuelle "EncodingCodeListVersion0"
    encoding_code_list_version = et.SubElement(arbre_code_list_versions, 'EncodingCodeListVersion')
    encoding_code_list_version.text = 'EncodingCodeListVersion0'

    # Je créé le sous-élément <FileFormatCodeListVersion> enfant de la balise <CodeListVersions> et je
    # lui donne comme valeur textuelle "FileFormatCodeListVersion0"
    file_format_code_list_version = et.SubElement(arbre_code_list_versions, 'FileFormatCodeListVersion')
    file_format_code_list_version.text = 'FileFormatCodeListVersion0'

    # Je créé le sous-élément <CompressionAlgorithmCodeListVersion> enfant de la balise <CodeListVersions> et je
    # lui donne comme valeur textuelle "CompressionAlgorithmCodeListVersion0"
    compression_algorithm_code_list_version = et.SubElement(arbre_code_list_versions,
                                                            'CompressionAlgorithmCodeListVersion')
    compression_algorithm_code_list_version.text = 'CompressionAlgorithmCodeListVersion0'

    # Je créé le sous-élément <DataObjectVersionCodeListVersion> enfant de la balise <CodeListVersions> et je
    # lui donne comme valeur textuelle "DataObjectVersionCodeListVersion0"
    data_object_version_code_list_version = et.SubElement(arbre_code_list_versions, 'DataObjectVersionCodeListVersion')
    data_object_version_code_list_version.text = 'DataObjectVersionCodeListVersion0'

    # Je créé le sous-élément <StorageRuleCodeListVersion> enfant de la balise <CodeListVersions> et je
    # lui donne comme valeur textuelle "StorageRuleCodeListVersion0"
    storage_rule_code_list_version = et.SubElement(arbre_code_list_versions, 'StorageRuleCodeListVersion')
    storage_rule_code_list_version.text = 'StorageRuleCodeListVersion0'

    # Je créé le sous-élément <AppraisalRuleCodeListVersion> enfant de la balise <CodeListVersions> et je
    # lui donne comme valeur textuelle "AppraisalRuleCodeListVersion0"
    appraisal_rule_code_list_version = et.SubElement(arbre_code_list_versions, 'AppraisalRuleCodeListVersion')
    appraisal_rule_code_list_version.text = 'AppraisalRuleCodeListVersion0'

    # Je créé le sous-élément <AccessRuleCodeListVersion> enfant de la balise <CodeListVersions> et je
    # lui donne comme valeur textuelle "AccessRuleCodeListVersion0"
    access_rule_code_list_version = et.SubElement(arbre_code_list_versions, 'AccessRuleCodeListVersion')
    access_rule_code_list_version.text = 'AccessRuleCodeListVersion0'

    # Je créé le sous-élément <DisseminationRuleCodeListVersion> enfant de la balise <CodeListVersions> et je
    # lui donne comme valeur textuelle "DisseminationRuleCodeListVersion0"
    dissemination_rule_code_list_version = et.SubElement(arbre_code_list_versions, 'DisseminationRuleCodeListVersion')
    dissemination_rule_code_list_version.text = 'DisseminationRuleCodeListVersion0'

    # Je créé le sous-élément <ReuseRuleCodeListVersion> enfant de la balise <CodeListVersions> et je
    # lui donne comme valeur textuelle "ReuseRuleCodeListVersion0"
    reuse_rule_code_list_version = et.SubElement(arbre_code_list_versions, 'ReuseRuleCodeListVersion')
    reuse_rule_code_list_version.text = 'ReuseRuleCodeListVersion0'

    # Je créé le sous-élément <ClassificationRuleCodeListVersion> enfant de la balise <CodeListVersions> et je
    # lui donne comme valeur textuelle "ClassificationRuleCodeListVersion0"
    classification_rule_code_list_version = et.SubElement(arbre_code_list_versions, 'ClassificationRuleCodeListVersion')
    classification_rule_code_list_version.text = 'ClassificationRuleCodeListVersion0'

    # Je créé le sous-élément <AuthorizationReasonCodeListVersion> enfant de la balise <CodeListVersions> et je
    # lui donne comme valeur textuelle "AuthorizationReasonCodeListVersion0"
    authorization_reason_code_list_version = et.SubElement(arbre_code_list_versions,
                                                           'AuthorizationReasonCodeListVersion')
    authorization_reason_code_list_version.text = 'AuthorizationReasonCodeListVersion0'

    # Je créé le sous-élément <RelationshipCodeListVersion> enfant de la balise <CodeListVersions> et je
    # lui donne comme valeur textuelle "RelationshipCodeListVersion0"
    relationship_code_list_version = et.SubElement(arbre_code_list_versions, 'RelationshipCodeListVersion')
    relationship_code_list_version.text = 'RelationshipCodeListVersion0'

    # Une fois cet arbre créé la fonction le renvoie vers la partie de code qui a appelée la fonction.
    return arbre_code_list_versions


def create_management_metadata():
    """Créée le sous-arbre ManagementMetadata, les valeurs de celui-ci sont rarement changés pour des versements
    unitaires, il m'a semblé plus simple de le créer à la volée dans une petite fonction dédiée qui ne prend aucun
    paramètre mais renvoie un objet de la class ElementTree propre à la librairie lxml. Toutefois c'est ici que l'on
    pourra changer la valeur du service versant ou service producteur qui ont pour l'instant une valeur par défaut,
    mais qui pourront être changés si nous enrichissons directement le manifest via le programme.

    :returns: l'arbre XML ayant pour racine <ManagementMetadata>
    :rtype: object ElementTree
    """
    # Création de l'élement racine <CodeListVersions>
    arbre_management_metadata = et.Element("ManagementMetadata")

    # Je créé le sous-élément <AcquisitionInformation> enfant de la balise <ManagementMetadata> et je lui donne comme
    # valeur textuelle "Versement"
    acquisition_information = et.SubElement(arbre_management_metadata, 'AcquisitionInformation')
    acquisition_information.text = 'Versement'

    # Je créé le sous-élément <LegalStatus> enfant de la balise <ManagementMetadata> et je lui donne comme
    # valeur textuelle "Public Archive"
    legal_status = et.SubElement(arbre_management_metadata, 'LegalStatus')
    legal_status.text = 'Public Archive'

    # Je créé le sous-élément <OriginatingAgencyIdentifier> enfant de la balise <ManagementMetadata> et je lui donne
    # comme valeur textuelle "Service_producteur"
    originating_agency_identifier = et.SubElement(arbre_management_metadata, 'OriginatingAgencyIdentifier')
    originating_agency_identifier.text = 'Service_producteur'

    # Je créé le sous-élément <SubmissionAgencyIdentifier> enfant de la balise <ManagementMetadata> et je lui donne
    # comme valeur textuelle "Service_versant"
    submission_agency_identifier = et.SubElement(arbre_management_metadata, 'SubmissionAgencyIdentifier')
    submission_agency_identifier.text = 'Service_versant'

    # Une fois cet arbre créé la fonction le renvoie vers la partie de code qui a appelée la fonction.
    return arbre_management_metadata
