import psycopg2
import Validations  

class PostgresqlUtils:

    def __init__(self):
        print('Create PostgreSQL instance')
        

    def connect(self, secrets):
        self.connection = None
        try:
            # Connectar al servidor postgres
            self.connection = psycopg2.connect(
                host=secrets["host"], 
                database=secrets["database"], 
                user=secrets["user"], 
                password=secrets["password"]
            )

            # Crear un cursor
            self.cursor = self.connection.cursor()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print('Something was wrong with postgreSQL Connection')
            print(error)
    
    def get_database_version(self):
        try:
            print('Run getDatabaseVersion method')
            
            sql = "SELECT version()"
            
            self.cursor.execute(sql)
            
            version = self.cursor.fetchone()
            
            print('Database Version', version)
                        
        except (Exception, psycopg2.DatabaseError) as error:
            print('Something was wrong with removeData method')
            print(error)
    
    def remove_data(self):
        try:
            print('Run removeData method')
            
            sql = "DELETE FROM mm_participants_plan_b WHERE id > 0"
            
            self.cursor.execute(sql)
                        
        except (Exception, psycopg2.DatabaseError) as error:
            print('Something was wrong with removeData method')
            print(error)  
    
    def insert_data(self, lista):
        try:
            
            print('Run inserData method')
            
            
            for row in lista:
                
                obligaciones_del_cliente_cerradas_u12m = row.get_obligaciones_del_cliente_cerradas_u12m() if row.get_obligaciones_del_cliente_cerradas_u12m() else 0
                meses_cuotas_pagadas_cliente_por_credito = row.get_meses_cuotas_pagadas_cliente_por_credito() if row.get_meses_cuotas_pagadas_cliente_por_credito() else 0
                valor_desembolsado_por_credito = row.get_valor_desembolsado_por_credito() if row.get_valor_desembolsado_por_credito() else 0
                
                register_type = Validations.validate_register_type(row)
                
                sql = 'INSERT INTO mm_participants_plan_b("document_type", "document_number", "client_obligations_closed_u12m", "monthly_paid_fees_customer_by_credit", "amount_disbursed_by_credit", "intra_month_debt", "restructured_client", "customer_collections_or_normalized", "rejected_requests_mantiz_flow_u6m", "rejected_requests_flow_gpou6m", "pending_requests_in_gpo", "obligations_number_greater_500m", "created_at", "register_type") VALUES (\'{0}\', \'{1}\', {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9},  {10}, {11}, CURRENT_TIMESTAMP, \'{12}\')'.format(row.get_tipo_documento(),
                row.get_documento(),
                obligaciones_del_cliente_cerradas_u12m,
                meses_cuotas_pagadas_cliente_por_credito,
                valor_desembolsado_por_credito,
                row.get_mora_intrames(),
                row.get_cliente_reestructurado(),
                row.get_cliente_cobranzas_o_normalizado(),
                row.get_solicitudes_rechazas_flujo_mantiz_u6m(),
                row.get_solicitudes_rechazadas_flujo_gpou6m(),
                row.get_solicitudes_pendientes_en_gpo(),
                row.get_numero_obligaciones_mayor_500m(),
                register_type)

                self.cursor.execute(sql)
            
            self.connection.commit()
            self.cursor.close()
            
            
        except (Exception, psycopg2.DatabaseError) as error:
            print('Something was wrong with insertData method')
            print(error)
            self.cursor.close()
        
        
