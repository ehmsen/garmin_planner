from .base import ASTNode

intensities_defintions = {}

class IntensityASTNode(ASTNode):
    def __init__(self, children=None, leaf=None):
        super().__init__(children, leaf)

    def get_avg_speed(self):
        return None

class IntensitiesNode(ASTNode):
    def __init__(self, definitions):
        super().__init__(children=definitions)
        self.definitions = definitions

class IntensityDefNode(ASTNode):
    def __init__(self, name, intensity):
        super().__init__(children=[intensity])
        self.name = name
        self.intensity = intensity
        if name in intensities_defintions:
            raise ValueError(f"Intensity '{name}' already defined")
        intensities_defintions[name] = intensity

class IntensityPaceNode(ASTNode):
    def __init__(self, min_tuple, max_tuple):
        if min_tuple > max_tuple:
            max_tuple, min_tuple = min_tuple, max_tuple
        super().__init__(leaf=(min_tuple, max_tuple))
        self.min_tuple = min_tuple
        self.max_tuple = max_tuple

    def get_min_speed(self):
        # Convert pace (min/km) to speed (m/s)
        return 1000 / (((self.min_tuple[0] * 60 + self.min_tuple[1]) * 60) + self.min_tuple[2])
    
    def get_max_speed(self):
        # Convert pace (min/km) to speed (m/s)
        return 1000 / (((self.max_tuple[0] * 60 + self.max_tuple[1]) * 60) + self.max_tuple[2])

    def get_avg_speed(self):
        return (self.get_min_speed() + self.get_max_speed()) / 2

class IntensityCadenceNode(ASTNode):
    def __init__(self, min, max):
        if min > max:
            max, min = min, max
        super().__init__(leaf=(min, max))
        self.min = min
        self.max = max

class IntensityHRZoneNode(ASTNode):
    def __init__(self, zone):
        super().__init__(leaf=zone)
        self.zone = zone

class IntensityHRNode(ASTNode):
    def __init__(self, min, max):
        if min > max:
            max, min = min, max
        super().__init__(leaf=(min, max))
        self.min = min
        self.max = max

class IntensityPowerZoneNode(ASTNode):
    def __init__(self, zone):
        super().__init__(leaf=zone)
        self.zone = zone

class IntensityPowerNode(ASTNode):
    def __init__(self, min, max):
        if min > max:
            max, min = min, max
        super().__init__(leaf=(min, max))
        self.min = min
        self.max = max

class IntensityIDNode(ASTNode):
    def __init__(self, name):
        super().__init__(leaf=name)
        self.name = name
        if not name in intensities_defintions:
            raise ValueError(f"Intensity '{name}' not defined")
        self.intensity = intensities_defintions[name]

    def get_avg_speed(self):
        return self.intensity.get_avg_speed()