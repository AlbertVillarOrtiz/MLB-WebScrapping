# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:26:44 2019

@author: AlbertVillarOrtiz
"""

class Match:
    league = "MLB"
    
    def __init__(self, idsTeams, idMatch):
        self.idsTeams = {"home": idsTeams[0], "away": idsTeams[1]}
        self.id = idMatch
        
    def setNamesMatch(self, names):
        self.names = {"home": names[0], "away": names[1]}
    
    def setH2h(self, h2h):
        self.h2hOverall = {"home": h2h[0], "away": h2h[2], "mutual": h2h[4]}
        self.h2hHome = {"home": h2h[1], "mutual": h2h[5]}
        self.h2hAway = {"away": h2h[3], "mutual": h2h[6]}
        
    def setOdds(self, oddsW, oddsOU, oddsAH):
        self.oddsW = {"home": oddsW[0], "away": oddsW[1]}
        self.oddsOU = oddsOU
        self.oddsAH = oddsAH
        
    def setClasification(self, overall, home, away):
        self.clasOverall = {
                "home": {
                        "POS": overall[0][0],
                        "GP": overall[0][1],
                        "GW": overall[0][2],
                        "GL": overall[0][3],
                        "PF": overall[0][4],
                        "PA": overall[0][5],
                        "PCT": overall[0][6]
                        },
                "away": {
                        "POS": overall[1][0],
                        "GP": overall[1][1],
                        "GW": overall[1][2],
                        "GL": overall[1][3],
                        "PF": overall[1][4],
                        "PA": overall[1][5],
                        "PCT": overall[1][6]
                        }
        }
        self.clasHome = {
                "home": {
                        "POS": home[0][0],
                        "GP": home[0][1],
                        "GW": home[0][2],
                        "GL": home[0][3],
                        "PF": home[0][4],
                        "PA": home[0][5],
                        "PCT": home[0][6]
                        },
                "away": {
                        "POS": home[1][0],
                        "GP": home[1][1],
                        "GW": home[1][2],
                        "GL": home[1][3],
                        "PF": home[1][4],
                        "PA": home[1][5],
                        "PCT": home[1][6]
                        }
        }
        self.clasAway = {
                "home": {
                        "POS": away[0][0],
                        "GP": away[0][1],
                        "GW": away[0][2],
                        "GL": away[0][3],
                        "PF": away[0][4],
                        "PA": away[0][5],
                        "PCT": away[0][6]
                        },
                "away": {
                        "POS": away[1][0],
                        "GP": away[1][1],
                        "GW": away[1][2],
                        "GL": away[1][3],
                        "PF": away[1][4],
                        "PA": away[1][5],
                        "PCT": away[1][6]
                        }
        }