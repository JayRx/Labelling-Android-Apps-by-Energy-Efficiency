from src.EnergyAntiPatterns.EnergyAntiPattern import EnergyAntiPattern

class LeakingThread(EnergyAntiPattern):
    def __init__(self):
        super().__init__("LeakingThread")
