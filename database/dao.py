from database.DB_connect import DBConnect
from model.album import Album
from model.connessione import Connessione


class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_album_durata():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT a.id, a.title, a.artist_id, SUM(t.milliseconds)/(60000) as durata
                    FROM album a, track t
                    WHERE a.id = t.album_id 
                    GROUP BY a.id   """

        cursor.execute(query)

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def album_connessi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT a1.id as album1, a2.id as album2
                    FROM album a1, album a2, track t1, track t2, playlist_track pt1, playlist_track pt2
                    WHERE a1.id  = t1.album_id and a2.id = t2.album_id 
	                    AND t1.id = pt1.track_id  and t2.id = pt2.track_id
	                    AND pt1.playlist_id = pt2.playlist_id 
	                    and a1.id < a2.id
 """

        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(row['album1'],row['album2']))

        cursor.close()
        conn.close()
        return result
