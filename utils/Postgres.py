import psycopg2

HOST = "localhost"
PORT = "5432"
USER = "postgres"
PASS = "Felipegarzon2021"
DB   = "bbog-mm-general"

class PostgresqlUtils:

    def __init__(self):
        print('Create PostgreSQL instance')
        

    def connect(self):
        self.connection = None
        try:
            # Connectar al servidor postgres
            self.connection = psycopg2.connect(host=HOST, database=DB, user=USER, password=PASS)

            # Crear un cursor
            self.cursor = self.connection.cursor()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print('Something was wrong with postgreSQL Connection')
            print(error)
            
    def removeData(self):
        try:
            print('Run removeData method')
            
            sql = "DELETE FROM public.mm_plan_b WHERE id > 0"
            
            self.cursor.execute(sql)
            
            self.cursor.close()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print('Something was wrong with removeData method')
            print(error)  
    
    def insertData(self, lista):
        try:
            
            print('Run inserData method')
            
            sql = 'INSERT INTO public.mm_plan_b("tipoDocumento", "documento", "obligacionesDelClienteCerradasU12M", "mesesCuotasPagadasClientePorCredito", "valorDesembolsadoPorCredito", "moraIntrames", "clienteReestructurado", "clienteCobranzasONormalizado", "solicitudesRechazadasFlujoGPOU6M", "solicitudesPendientesEnGPO", "numeroObligacionesMayor500M", "solicitudesRechazasFlujoMantizU6M", "createdAt") VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9},  {10}, {11}, CURRENT_TIMESTAMP)'.format("'C'","'1069753422'",1,2,25000000,0,1,2,3,4,5,6)
            
            #for row in data:
            #row = lista[0]
            self.cursor.execute(sql)
            
            self.connection.commit()
            self.cursor.close()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print('Something was wrong with insertData method')
            print(error)
            self.cursor.close()
        
        
