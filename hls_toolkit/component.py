
"""
@attention: Not used yet
"""
class HLSCompoenet(object):
    def __init__(self, name):
        self.name = name
        self.port =[]
        self.body = []
        self.stages = []
        self.extraTypes = []

    def isSequntial(self):
        return hasattr(self, "clk")