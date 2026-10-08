from exceptions.analyser_exception import AnalyserException

class CollectorException(AnalyserException):
    
    def __init__(self, cause , advice):
        self.module = "Collector"
        super().__init__(self.module, cause, advice)