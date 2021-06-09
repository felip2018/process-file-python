class ReportInfo:
    
    def __init__(self):
        self.__total_processed = 0
        self.__success_lines = 0
        self.__wrong_lines = 0
        self.__report = []
        
    
    def set_total_processed(self, total):
        self.__total_processed = total
        
    def update_success_lines(self):
        self.__success_lines += 1
        
    def update_wrong_lines(self):
        self.__wrong_lines += 1
        
    def update_report(self, element):
        self.__report.append(element)
        
    def get_report(self):
        report = "Processing Report: \n"
        report += "- Processed Lines: " + str(self.__total_processed) +  "\n"
        report += "- Success Lines: " + str(self.__success_lines) + "\n"
        report += "- Wrong Lines: " + str(self.__wrong_lines) + "\n"
        report += "Error lines: \n"
                        
        for line in self.__report:
            report += line
        
        return report