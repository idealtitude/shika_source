#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import sqlite3 as bdd

REAL_CWD = os.getcwd()
DB_PATH = REAL_CWD + os.sep  + 'saveload' + os.sep + 'shikabdd'

class UsersMng:
    """
    Classe de gestion de la table `users`
    =====================================
    """
    def __init__(self):
        """
        Initialisation de la classe
        ============================

        :param self.db: type string, chemin de la bdd
        """
        self.db = DB_PATH #Fichier sqlite (base de données)
        self.con = None

    def _dbcon(self):
        """
        Connexion à la base de données
        ==============================
        """
        return bdd.connect(self.db)

    def db_close(self):
        """Fermeture de la connexion
        """
        self.con.close()

    def read_table(self, iduser):
        """
        Lecture bdd
        ============
        
        :param iduser: type int, identifiant bdd de la ligne à lire dans la table, si iduser = 0: lecture de toute la table

        :return: tabledatas list, tableau python contenant les données retournées par la requête
        """

        self.con = self._dbcon() #On se connecte à la bdd
        user = ''
        if iduser > 0:
            user = ' where id = %s' % iduser
        query = 'select * from users%s' % user
        tabledatas = {}

        with self.con:
            cur = self.con.cursor()
            cur.execute(query)
            rows = cur.fetchall()

            for row in rows:
                x = {'iduser': row[0], 'name': str(row[1]), 'argent': row[2], 'courses': row[3], 'achievements': row[4], 'date': row[5], 'key': row[6]} #On crée un dico pour chaque ligne
                tabledatas[row[1]] = x #On range chaque dico dans le tableau

        return tabledatas

    def add_user(self, datatostore):
        """
        Ajout dans la bdd
        =================
        
        :param datatostore: dictionnaire contenant toutes les données à enregistrer dans la bdd (ex.: {'nom': 'albator', 'monnaie': 20} )

        :return: writeresult, booléen, true si succès, false si échec de la requête
        """
        pass

    def update_user(self, iduser, datatoupdate):
        """
        Mise à jour bdd
        ===============
        
        :param iduser: type int, identifiant bdd, ne peut-être vide

        :param datatoupdate: dictionnaire contenant les données à mettre à jour dans la table

        :return updateresult: booléen, true si succès, false si échec de la requête
        """
        pass

