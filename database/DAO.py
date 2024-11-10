from database.DB_connect import DBConnect
from model.edge import Edge
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.`datetime`) as year
                        from sighting s 
                        order by year(s.`datetime`) desc
"""
            cursor.execute(query)
            for row in cursor:
                result.append(row['year'])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getShapes(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape as forma
                        from sighting s 
                        where s.shape != ''
                        and s.shape is not null
                        and year(`datetime`) = %s
                        order by shape asc
    """
            cursor.execute(query,(year,))
            for row in cursor:
                result.append(row['forma'])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(year,shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.*
                        from sighting s 
                        where year(s.`datetime`) = %s
                        and s.shape = %s
                         """

            cursor.execute(query,(year,shape,))

            rows = cursor.fetchall()

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(year,shape,idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select t1.id as id1,t2.id as id2,(t2.longitude - t1.longitude) as weight
                        from 
                        (select s.longitude, s.id,s.state
                        from sighting s
                        where year(datetime) = %s
                        and shape = %s) as t1,
                        (select s.longitude, s.id,s.state
                        from sighting s
                        where year(datetime) = %s
                        and shape = %s) as t2
                        where t1.longitude < t2.longitude
                        and t1.state = t2.state
                
    """
            cursor.execute(query,(year,shape,year,shape,))
            for row in cursor:
                if row["id1"] in idMap and row["id2"] in idMap:
                    result.append(Edge(idMap[row["id1"]],idMap[row["id2"]],row["weight"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                        from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result