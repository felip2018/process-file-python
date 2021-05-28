class DataRow:
    
    def __init__(self, row):
        self.__tipoDocumento = row[0]
        self.__documento = row[1]
        self.__obligacionesDelClienteCerradasU12M = row[2]
        self.__mesesCuotasPagadasClientePorCredito = row[3]
        self.__valorDesembolsadoPorCredito = row[4]
        self.__moraIntrames = row[5]
        self.__clienteReestructurado = row[6]
        self.__clienteCobranzasONormalizado = row[7]
        self.__solicitudesRechazasFlujoMantizU6M = row[8]
        self.__solicitudesRechazadasFlujoGPOU6M = row[9]
        self.__solicitudesPendientesEnGPO = row[10]
        self.__numeroObligacionesMayor500M = row[11]

    def getTipoDocumento(self):
        return self.__tipoDocumento
    
    def getDocumento(self):
        return self.__documento
    
    def getObligacionesDelClienteCerradasU12M(self):
        return self.__obligacionesDelClienteCerradasU12M
    
    def getMesesCuotasPagadasClientePorCredito(self):
        return self.__mesesCuotasPagadasClientePorCredito
    
    def getValorDesembolsadoPorCredito(self):
        return self.__valorDesembolsadoPorCredito
    
    def getMoraIntrames(self):
        return self.__moraIntrames
    
    def getClienteReestructurado(self):
        return self.__clienteReestructurado
    
    def getClienteCobranzasONormalizado(self):
        return self.__clienteCobranzasONormalizado
    
    def getSolicitudesRechazadasFlujoGPOU6M(self):
        return self.__solicitudesRechazadasFlujoGPOU6M
    
    def getSolicitudesPendientesEnGPO(self):
        return self.__solicitudesPendientesEnGPO
    
    def getNumeroObligacionesMayor500M(self):
        return self.__numeroObligacionesMayor500M
