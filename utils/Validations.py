def validate_register_type(row):
    try:
        register_type = ""
        if(row.get_obligaciones_del_cliente_cerradas_u12m() and
           row.get_meses_cuotas_pagadas_cliente_por_credito() and
           row.get_valor_desembolsado_por_credito()):
            register_type = "RENOVACION"
        else:
            register_type = "PARALELO"
            
        return register_type
                
        
    except Exception as error:
            print('Something was wrong with validateRegisterType Connection')
            print(error)