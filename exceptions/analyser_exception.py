class AnalyserException(Exception):
    
    def __init__(self, module, cause, advice):
        super().__init__()
        self.module = module
        self.cause = cause
        self.advice = advice
        
    def get_module(self):
        return self.module
    
    def get_cause(self):
        return self.cause
    
    def get_advice(self):
        return self.advice