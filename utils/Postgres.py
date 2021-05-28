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
            
            sql = "DELETE FROM mm_plan_b WHERE id > 0"
            
            self.cursor.execute(sql)
                        
        except (Exception, psycopg2.DatabaseError) as error:
            print('Something was wrong with removeData method')
            print(error)  
    
    def insertData(self, lista):
        try:
            
            print('Run inserData method')
            
            
            for row in lista:
                
                obligacionesDelClienteCerradasU12M = row.getObligacionesDelClienteCerradasU12M() if row.getObligacionesDelClienteCerradasU12M() else 0
                mesesCuotasPagadasClientePorCredito = row.getMesesCuotasPagadasClientePorCredito() if row.getMesesCuotasPagadasClientePorCredito() else 0
                valorDesembolsadoPorCredito = row.getValorDesembolsadoPorCredito() if row.getValorDesembolsadoPorCredito() else 0
                
                sql = 'INSERT INTO public.mm_plan_b("tipoDocumento", "documento", "obligacionesDelClienteCerradasU12M", "mesesCuotasPagadasClientePorCredito", "valorDesembolsadoPorCredito", "moraIntrames", "clienteReestructurado", "clienteCobranzasONormalizado", "solicitudesRechazasFlujoMantizU6M", "solicitudesRechazadasFlujoGPOU6M", "solicitudesPendientesEnGPO", "numeroObligacionesMayor500M", "createdAt") VALUES (\'{0}\', \'{1}\', {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9},  {10}, {11}, CURRENT_TIMESTAMP)'.format(row.getTipoDocumento(),
                row.getDocumento(),
                obligacionesDelClienteCerradasU12M,
                mesesCuotasPagadasClientePorCredito,
                valorDesembolsadoPorCredito,
                row.getMoraIntrames(),
                row.getClienteReestructurado(),
                row.getClienteCobranzasONormalizado(),
                row.getSolicitudesRechazasFlujoMantizU6M(),
                row.getSolicitudesRechazadasFlujoGPOU6M(),
                row.getSolicitudesPendientesEnGPO(),
                row.getNumeroObligacionesMayor500M())

                self.cursor.execute(sql)
            
            self.connection.commit()
            self.cursor.close()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print('Something was wrong with insertData method')
            print(error)
            self.cursor.close()
        
        
