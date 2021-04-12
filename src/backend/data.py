class Data:
    
    def __init__(self, parent):
        self.parent = parent
    
    def get_telemetry(self):
        telemetry_data = self.parent.get_telemetry()
        return telemetry_data
    
    # Function pushes telemetry to frontend upon request
    def telemetry(self):
        pass