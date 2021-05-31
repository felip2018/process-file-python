#!/usr/bin/python
import psycopg2

class PostgresqlUtils:

    def __init__(self):
        print('Create PostgreSQL instance')
        

    def connect(self, secrets):
        self.connection = None
        try:
            # Connectar al servidor postgres
            self.connection = psycopg2.connect(
                host=secrets["HOST"], 
                database=secrets["DB"], 
                user=secrets["USER"], 
                password=secrets["PASS"]
            )

            # Crear un cursor
            self.cursor = self.connection.cursor()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print('Something was wrong with postgreSQL Connection')
            print(error)
    
    def getDatabaseVersion(self):
        try:
            print('Run getDatabaseVersion method')
            
            sql = "SELECT version()"
            
            self.cursor.execute(sql)
            
            version = self.cursor.fetchone()
            
            print('Database Version', version)
                        
        except (Exception, psycopg2.DatabaseError) as error:
            print('Something was wrong with removeData method')
            print(error)
    
    def removeData(self):
        try:
            print('Run removeData method')
            
            sql = "DELETE FROM mm_participants_plan_b WHERE id > 0"
            
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
                
                sql = 'INSERT INTO mm_participants_plan_b("document_type", "document_number", "client_obligations_closed_u12m", "monthly_paid_fees_customer_by_credit", "amount_disbursed_by_credit", "intra_month_debt", "restructured_client", "customer_collections_or_normalized", "rejected_requests_mantiz_flow_u6m", "rejected_requests_flow_gpou6m", "pending_requests_in_gpo", "obligations_number_greater_500m", "created_at") VALUES (\'{0}\', \'{1}\', {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9},  {10}, {11}, CURRENT_TIMESTAMP)'.format(row.getTipoDocumento(),
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
        
        
