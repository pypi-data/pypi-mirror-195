import sqlite3

class JGVutils:
    @staticmethod
    def get_database():
        database = getattr(g, '_database', None)
        if database is None:
            database = g._database = sqlite3.connect("sqlite.db")
        return database
    
    @staticmethod
    def close_connection():
        database = getattr(g, '_database', None)
        if database is not None:
            database.close()
    
    # Método para ejecutar consultas
    @staticmethod
    def execute_query(query, args=()):
        database = Utils.get_database()
        query_lower = query.lower()
        cursor = database.execute(query, args)
        if "insert" in query_lower or "delete" in query_lower or "update" in query_lower or "drop" in query_lower:
            database.commit()
        filas = cursor.fetchall()
        cursor.close()
        return filas
    