class ReportInfo:
    
    def __init__(self):
        self.__totalProcessed = 0
        self.__successLines = 0
        self.__wrongLines = 0
        self.__report = []
        
    
    def setTotalProcessed(self, total):
        self.__totalProcessed = total
        
    def updateSuccessLines(self):
        self.__successLines += 1
        
    def updateWrongLines(self):
        self.__wrongLines += 1
        
    def updateReport(self, element):
        self.__report.append(element)
        
    def getReport(self):
        report = "Processing Report: \n"
        report += "- Processed Lines: " + str(self.__totalProcessed) +  "\n"
        report += "- Success Lines: " + str(self.__successLines) + "\n"
        report += "- Wrong Lines: " + str(self.__wrongLines) + "\n"
        report += "Error lines: \n"
                        
        for line in self.__report:
            report += line
        
        return report