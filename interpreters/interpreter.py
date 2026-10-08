from abc import ABC, abstractmethod

class Interpreter(ABC):
    
    def __init__(self, project_configuration, schedule):
        self.project_configuration = project_configuration
        self.schedule_before_interpretation = schedule
        
    def get_interpreted_shedule(self):
        interpreted_shedule = self.interpret_shedule_according_to_contract_rules()
        return interpreted_shedule
    
    @abstractmethod
    def interpret_shedule_according_to_contract_rules(self):
        pass