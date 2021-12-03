
from dataclasses import asdict
import datetime
import re
# from pprint import pprint
from tinydb import TinyDB, Query

db = TinyDB('db.json', ensure_ascii=False)


class Serialization:

    @staticmethod
    def date_serialization(datetime_obj) -> str:
        """Adapte à la db en changeant un datetime en str"""
        return datetime_obj.strftime("%d/%m/%Y")

    @staticmethod
    def serialize_all_dates(dict_obj):
        """
        Trouve les objets datetime au format datetime.datetime(2000, 1, 1, 0, 0) dans un dict.
        Change tous les datetime présents dans les valeurs d'un dict en string.(Juste la date)
        """
        dates = {}
        for k, v in dict_obj.items():
            if type(v) == datetime.datetime:
                dates[k] = v.strftime("%d/%m/%Y")
        for k, v in dates.items():
            dict_obj[k] = v
        return dict_obj

    @staticmethod
    def serialize_all_times(dict_obj):
        """
        Trouve les objets datetime au format datetime.datetime(2000, 1, 1, 0, 0) dans un dict.
        Change tous les datetime présents dans les valeurs d'un dict en string.(Avec l'heure)
        """
        dates = {}
        for k, v in dict_obj.items():
            if type(v) == datetime.datetime:
                dates[k] = v.strftime("%d/%m/%Y, %H:%M:%S")
        for k, v in dates.items():
            dict_obj[k] = v
        return dict_obj

    @staticmethod
    def date_deserialization(date_string) -> datetime:
        """Adapte à l'usage un objet date str venant de la db"""
        return datetime.datetime.strptime(date_string, "%d/%m/%Y")

    @staticmethod
    def find_datestring(text):
        """Trouve la première date au format **/**/**** dans l'élément string
        et la change en datetime."""
        match = re.search(r'\d{2}/\d{2}/\d{4}', text)
        date = datetime.datetime.strptime(match.group(), '%d/%m/%Y').date()
        print(date)
        return date

    @staticmethod
    def findall_datestring(elt) -> list:
        """Trouve juste les dates au format **/**/**** dans l'élément."""
        match = re.findall(r'\d{2}/\d{2}/\d{4}', str(elt))
        dates = []
        for date in match:
            dates.append(date)
        return dates

    def deserialize_all_dates(self, dict_obj=None):
        """Trouve les dates au format **/**/**** dans l'élément.
        Les change en datetime. """
        match = re.findall(r'\d{2}/\d{2}/\d{4}', str(dict_obj))
        dates = {}
        for date in match:
            for k, v in dict_obj.items():
                if v == date:
                    dates[k] = datetime.datetime.strptime(v, "%d/%m/%Y")
        for k, v in dates.items():
            dict_obj[k] = v
        return dict_obj

    def calculate_age(valeur):
        today = datetime.datetime.now()
        age = today.year - valeur.year - ((today.month, today.day) < (valeur.month, valeur.day))
        return age


class Database:
    def __init__(self=db):
        pass

    def insert(self, dataclass_instance_to_insert):
        Recherche = Query()
        dict_du_modele = asdict(dataclass_instance_to_insert)
        # On change les datetimes en date_strings:
        dict_du_modele = Serialization.serialize_all_dates(dict_obj=dict_du_modele)
        # On vérifie avec le nom si l'objet est déjà dans la db:
        if db.contains(Recherche.name == [dict_du_modele['name']]):
            print(f"{dict_du_modele['name']} est déjà enregistré dans la base de données")
        else:
            db.insert(dict_du_modele)
            print(f"\nEnregistrement de {dict_du_modele['name']} dans la base de données...")

    def check_if_in_db(self, to_find: str):
        """Vérifie si un objet est dans la db"""
        Recherche = Query()
        to_find = to_find.upper()
        if db.contains(Recherche.name == to_find):
            return True
        else:
            return False

    def get_dict_from_db(self, to_find: str) -> dict:
        Recherche = Query()
        to_find = str(to_find).upper()
        if db.contains(Recherche.name == to_find):
            result = db.get(Recherche.name == to_find)
            serialization = Serialization()
            serialization.deserialize_all_dates(result)
            return dict(result)
        else:
            return False

    def get_in_db(self, to_find: str) -> list:
        """Cherche un objet dans la db à partir de son nom (clé = name). Prévoit les erreurs de casse.
        Renvoie les valeurs de l'objet sous forme de liste."""
        Recherche = Query()
        to_find = str(to_find).upper()
        if db.contains(Recherche.name == to_find):
            # resultat = db.search (Recherche.name.matches( a_chercher, flags=re.IGNORECASE))
            # donne une liste avec tout le dico dedans
            result = db.get(Recherche.name == to_find).values()
            return list(result)
        else:
            return False

    def change(self, k, v, k_to_change, v_to_change):
        """
        Modifie un objet dans la db.

        k = clé du champs pour trouver l'objet (ex: "firstname")
        v = valeur connue pour trouver l'objet (ex: "Jasper")
        k_to_change = clé du champs à changer
        v_to_change = nouvelle valeur
        """
        Recherche = Query()
        action = db.update({k_to_change: v_to_change}, Recherche[k] == v)
        return action

        # db.update ({"count": 10}, fruit type == "apple")}) >>> [{'count': 10, 'type': 'apple'}

    def delete(self, to_delete):
        """Efface de la db, à partir du nom"""
        Recherche = Query()
        to_delete = to_delete.upper()
        db.remove(Recherche.name == to_delete)

    def getFieldList(self, fieldName):
        """ Crée une liste de toutes les valeurs correspondant à la clé donnée (fieldname)"""
        result = [r[fieldName] for r in db]
        return result
        # exemple d'utilisation dans le code: print(getFieldData('firstname')) >>> liste des prénoms

    def getFieldData(self, key, value, field_name):
        """
        clé: name, firstname, birthdate... entre guillements
        objet_a_trouver: la valeur connue entre guillements
        fieldname: la clé du champs dont on souhaite voir la valeur.

        Par exemple: si key = firstname,
        objet_a_trouver = "Brigitte" et field_name = name,
        le retour sera Bardot.
        """
        Recherche = Query()
        results = db.search(Recherche[key] == value)
        result = [r[field_name] for r in results]
        return result
        # plus tard dans le code:
        # res = getFieldData('name',"TOURNOI DES FOUS", "players")
        # for name in res:
        # print(name)


class Report:
    def __init__(self=db):
        pass

    def get_tournaments_list(self=db):
        """
        Génère une liste des tournois si leur nom commence pas tournoi.
        Idéalement il aurait fallu rajouter un champs "nature: tournoi ou joueur
        dans les dataclass et trouver comment récupérer
        l'objet entier d'après une clé dans la db (mais comment faire?)
        """
        registered_tournaments = []
        result = [r['name'] for r in db]
        for r in result:
            if "TOURNOI" in r:
                registered_tournaments.append(r)
        return registered_tournaments

    def get_players_list(self=db):
        """Renvoie la liste de tous les joueurs présents dans la base de données.
        Utiliser avec: players_in_db = Report.get_players_list()"""
        registered_players = []
        result = [r['name'] for r in db]
        for r in result:
            if "TOURNOI" not in r:
                registered_players.append(r)
        return registered_players

    def get_names_and_ratings(self=db, players_list=[]) -> dict:
        """ Donne une liste de dictionnaires contenant pour nom, prénom et classement de chaque joueur.
        Utiliser avec names_and_ratings = Report.get_names_and_ratings(players_list = players_in_db)"""
        players_names_and_ratings = []
        for player in players_list:
            instance_db = Database()
            player = instance_db.get_in_db(player)
            name = player[0]
            firstname = player[1]
            rating = player[4]
            player_name_and_rating = {"name": name, "firstname": firstname, "rating": rating}
            players_names_and_ratings.append(player_name_and_rating)
        return players_names_and_ratings

    def sort_by_rating(self=db, list_to_sort=[]):
        """Renvoie la liste des noms de joueurs triée par classement.
        Brute sous forme de dictionnaire [0] ou Bien présentée en string [1]"""
        sortable_list = self.get_names_and_ratings(list_to_sort)
        sorted_list = sorted(sortable_list, key=lambda k: k["rating"], reverse=True)
        pretty_sorted_list = []
        for player in sorted_list:
            pplayer = "{firstname} {name}, classement:{rating}".format(**player)
            pretty_sorted_list.append(pplayer)
        return sorted_list, pretty_sorted_list

    def sort_by_name(self=db, list_to_sort=[]):
        """Renvoie la liste des noms des joueurs triée par ordre alphabétique.
        Brute sous forme de dictionnaire [0] ou Bien présentée en string [1]"""
        sortable_list = self.get_names_and_ratings(list_to_sort)
        sorted_list = sorted(sortable_list, key=lambda k: k["name"])
        pretty_sorted_list = []
        for player in sorted_list:
            pplayer = "{firstname} {name}".format(**player)
            pretty_sorted_list.append(pplayer)
        return sorted_list, pretty_sorted_list

    def get_a_report(self=db, elt=None) -> list:
        if isinstance(elt, str):
            elt = elt.upper()
        else:
            elt = elt
        report = []
        result = [r['name'] for r in db]
        for r in result:
            if elt in r:
                report.append(r)
        return report
        # Use with: rech = Report.get_a_report(elt="TOURNOI")


if __name__ == "__main__":
    database = Database()
    rapport = Report()
    tournois = rapport.get_tournaments_list()
    # print(tournois)

    tournoi = "Tournoi des reines"
    tournoi = tournoi.upper()
    bidule = database.get_dict_from_db(tournoi)
    # pprint(bidule)

    tout = db.all()
    # print(tout)

    # db.truncate()

    # database.change("name", "HULOT", "name", "HIBOU")
