import pyodbc
class Conexion():
    def connect(self):
        direccion_servidor = 'DESKTOP-4GCAPQ1\SQLEXPRESS'
        nombre_bd = 'inteligencia'
        try:
            conexion = pyodbc.connect(driver='{SQL Server Native Client 11.0}',
                          server=direccion_servidor, 
                          database=nombre_bd,               
                          trusted_connection='yes')
            return conexion
        except Exception as e:
            print("Ocurrió un error al conectar a SQL Server: ", e)
