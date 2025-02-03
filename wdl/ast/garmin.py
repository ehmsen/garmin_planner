from .base import ASTNode

class GarminNode(ASTNode):
    def __init__(self, definitions):
        super().__init__(children=definitions)
        self.definitions = definitions
        # print(f"GarminNode: {definitions}")

class GarminDefNode(ASTNode):
    def __init__(self, name, value):
        super().__init__(leaf=value)
        self.name = name
        self.value = value
