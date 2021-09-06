import os
import Ressources.app as app

if __name__ == '__main__':
    try:
        print('Création du fichier CSV ...')
        app.create_csv("./EAD", "./CSV")
        print('Opération terminée avec succès.')
    except Exception as e:
        print(e)
    finally:
        os.system("pause")
