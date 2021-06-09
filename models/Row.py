class DataRow:
    
    def __init__(self, row):
        self.__tipo_documento = row[0]
        self.__documento = row[1]
        self.__obligaciones_del_cliente_cerradas_u12m = row[2]
        self.__meses_cuotas_pagadas_cliente_por_credito = row[3]
        self.__valor_desembolsado_por_credito = row[4]
        self.__mora_intrames = row[5]
        self.__cliente_reestructurado = row[6]
        self.__cliente_cobranzas_o_normalizado = row[7]
        self.__solicitudes_rechazas_flujo_mantiz_u6m = row[8]
        self.__solicitudes_rechazadas_flujo_gpou6m = row[9]
        self.__solicitudes_pendientes_en_gpo = row[10]
        self.__numero_obligaciones_mayor_500m = row[11]

    def get_tipo_documento(self):
        return self.__tipo_documento
    
    def get_documento(self):
        return self.__documento
    
    def get_obligaciones_del_cliente_cerradas_u12m(self):
        return self.__obligaciones_del_cliente_cerradas_u12m
    
    def get_meses_cuotas_pagadas_cliente_por_credito(self):
        return self.__meses_cuotas_pagadas_cliente_por_credito
    
    def get_valor_desembolsado_por_credito(self):
        return self.__valor_desembolsado_por_credito
    
    def get_mora_intrames(self):
        return self.__mora_intrames
    
    def get_cliente_reestructurado(self):
        return self.__cliente_reestructurado
    
    def get_cliente_cobranzas_o_normalizado(self):
        return self.__cliente_cobranzas_o_normalizado
    
    def get_solicitudes_rechazas_flujo_mantiz_u6m(self):
        return self.__solicitudes_rechazas_flujo_mantiz_u6m
    
    def get_solicitudes_rechazadas_flujo_gpou6m(self):
        return self.__solicitudes_rechazadas_flujo_gpou6m
    
    def get_solicitudes_pendientes_en_gpo(self):
        return self.__solicitudes_pendientes_en_gpo
    
    def get_numero_obligaciones_mayor_500m(self):
        return self.__numero_obligaciones_mayor_500m
