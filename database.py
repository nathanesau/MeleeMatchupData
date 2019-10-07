from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os


class Database:
    def _DatabaseConnect(self, dbName):
        if QSqlDatabase.isDriverAvailable("QSQLITE"):
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(dbName)
            if not db.open():
                qWarning("DatabaseConnect - ERROR " + db.lastError().text())
        else:
            qWarning("DatabaseConnect - ERROR: no driver available")

    def _createSSBMRankTable(self, tname):
        query = QSqlQuery("CREATE TABLE " + tname +
                          " (id INTEGER PRIMARY KEY, Rank INTEGER, Player TEXT)")
        if not query.isActive():
            qWarning("createSSBMRankTable - ERROR " + query.lastError().text())

    def _populateSSBMRankTable(self, tname, playerData):
        query = QSqlQuery("INSERT INTO " + tname +
                          " (Rank, Player) VALUES(?, ?)")
        QSqlDatabase.database().transaction()
        for row in playerData:
            query.bindValue(0, int(row[0]))
            query.bindValue(1, row[1])
            if not query.exec():
                qWarning("populateSSBMRankTable - ERROR " +
                         query.lastError().text())
        QSqlDatabase.database().commit()

    def _readSSBMRankTable(self, tname, tdata):  # for one table
        query = QSqlQuery()
        if not query.exec("SELECT Rank, Player FROM " + tname):
            qWarning("loadSSBMRankData - ERROR: " + query.lastError().text())
        while query.next():
            rank = query.value(0)
            player = query.value(1)
            tdata.append([rank, player])

    def _createMatchupTable(self):
        query = QSqlQuery("CREATE TABLE MATCHUP " +
                          " (id INTEGER PRIMARY KEY, Player1 TEXT, Player2 TEXT, " +
                          "SetWins INTEGER, SetLosses INTEGER)")
        if not query.isActive():
            qWarning("createMatchupTable - ERROR: " + query.lastError().text())

    def _populateMatchupTable(self, matchup_dict):
        query = QSqlQuery("INSERT INTO MATCHUP (Player1, Player2, SetWins, SetLosses) " +
                          "VALUES(?, ?, ?, ?)")
        QSqlDatabase.database().transaction()
        for key, value in matchup_dict.items():
            player1 = key[0]
            player2 = key[1]
            wins = value['wins']
            losses = value['losses']
            query.bindValue(0, player1)
            query.bindValue(1, player2)
            query.bindValue(2, wins)
            query.bindValue(3, losses)
            if not query.exec():
                qWarning("populateMatchupTable - ERROR " +
                         query.lastError().text())
        QSqlDatabase.database().commit()

    def _readMatchupTable(self, matchup_dict):
        query = QSqlQuery()
        if not query.exec("SELECT Player1, Player2, SetWins, SetLosses FROM MATCHUP"):
            qWarning("readMatchupTable - ERROR: " + query.lastError().text())
        while query.next():
            player1 = query.value(0)
            player2 = query.value(1)
            wins = query.value(2)
            losses = query.value(3)
            matchup_dict[(player1, player2)] = {'wins': wins, 'losses': losses}

    def __init__(self, dbName):
        self.dbName = dbName
        self._DatabaseConnect(dbName)

    def SaveSSBMRankData(self, tname, playerData):  # for one table
        self._createSSBMRankTable(tname)
        self._populateSSBMRankTable(tname, playerData)

    def LoadSSBMRankData(self, ssbm_rank_dict):
        query = QSqlQuery()
        if not query.exec("SELECT name FROM sqlite_master WHERE type='table' ORDER by name"):
            qWarning("DatabaseInit - ERROR " + query.lastError().text())
        while query.next():  # process existing tables
            tname = query.value(0)
            tdata = []
            self._readSSBMRankTable(tname, tdata)
            ssbm_rank_dict[tname] = tdata

    def SaveMatchupData(self, matchup_dict):
        self._createMatchupTable()
        self._populateMatchupTable(matchup_dict)

    def LoadMatchupData(self, matchup_dict):
        self._readMatchupTable(matchup_dict)
