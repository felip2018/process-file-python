def validateRegisterType(row):
    try:
        registerType = ""
        if(row.getObligacionesDelClienteCerradasU12M() and
           row.getMesesCuotasPagadasClientePorCredito() and
           row.getValorDesembolsadoPorCredito()):
            registerType = "RENOVACION"
        else:
            registerType = "PARALELO"
            
        return registerType
                
        
    except Exception as error:
            print('Something was wrong with validateRegisterType Connection')
            print(error)