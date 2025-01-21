import ply.yacc as yacc
from .tokens import tokens
import json

intensities_defintions = {}
durations_defintions = {}

class ASTNode(object):
    def __init__(self, children=None, leaf=None):
        self.children = children if children else []
        self.leaf = leaf

    def __str__(self):
        return self.__class__.__name__
    
    def to_dict(self):
        return {
            'type': self.__class__.__name__,
            'children': [child.to_dict() for child in self.children] if self.children else [],
            'leaf': self.leaf
        }

class RootNode(ASTNode):
    def __init__(self, main_body):
        super().__init__(children=main_body)
        self.main_body = main_body

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

class DurationsNode(ASTNode):
    def __init__(self, definitions):
        super().__init__(children=definitions)
        self.definitions = definitions

class DurationDefNode(ASTNode):
    def __init__(self, name, duration):
        super().__init__(children=[duration])
        self.name = name
        self.duration = duration
        if name in durations_defintions:
            raise ValueError(f"Duration '{name}' already defined")
        durations_defintions[name] = duration

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

class WorkoutNode(ASTNode):
    def __init__(self, workout_type, name, body):
        super().__init__(children=body)
        self.workout_type = workout_type
        self.name = name
        self.body = body

class WorkoutStepNode(ASTNode):
    def __init__(self, step_type, duration=None, intensity=None):
        super().__init__(children=[e for e in [duration, intensity] if e is not None])
        self.step_type = step_type
        self.duration = duration
        self.intensity = intensity

class WorkoutStepRepeatNode(ASTNode):
    def __init__(self, count, steps):
        super().__init__(children=steps)
        self.count = count
        self.steps = steps

class DurationTimeNode(ASTNode):
    def __init__(self, time_tuple):
        super().__init__(leaf=time_tuple)
        self.time = time_tuple

class DurationDistanceNode(ASTNode):
    def __init__(self, distance):
        super().__init__(leaf=distance)
        self.distance = distance

class DurationCaloriesNode(ASTNode):
    def __init__(self, calories):
        super().__init__(leaf=calories)
        self.calories = calories

class DurationHRAboveBelowNode(ASTNode):
    def __init__(self, hr_type, hr_value):
        super().__init__(leaf=(hr_type, hr_value))
        self.hr_type = hr_type
        self.hr_value = hr_value

class DurationIDNode(ASTNode):
    def __init__(self, name):
        super().__init__(leaf=name)
        self.name = name
        if not name in durations_defintions:
            raise ValueError(f"Duration '{name}' not defined")
        self.duration = durations_defintions[name]

class IntensityPaceNode(ASTNode):
    def __init__(self, min, max):
        if min > max:
            max, min = min, max
        super().__init__(leaf=(min, max))
        self.min = min
        self.max = max

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

class WorkoutParser:
    def __init__(self):
        self.parser = None
        self.tokens = tokens

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser

    def parse(self, input, lexer):
        return self.parser.parse(input, lexer=lexer.lexer)

    # Parsing rules
    def p_root(self, p):
        'root : main_body'
        p[0] = RootNode(p[1])

    def p_main_body(self, p):
        '''main_body : main_body main_def'''
        p[1].append(p[2])
        p[0] = p[1]

    def p_main_body_single(self, p):
        '''main_body : main_def'''
        p[0] = [p[1]]

    def p_main_def(self, p):
        '''main_def : intensities
                   | durations
                   | workout
                   | garmin'''
        p[0] = p[1]
    
    def p_garmin(self, p):
        'garmin : GARMIN LBRACKET garmin_body RBRACKET'
        p[0] = GarminNode(p[3])
    
    def p_garmin_body(self, p):
        'garmin_body : garmin_body garmin_def'
        p[1].append(p[2])
        p[0] = p[1]
    
    def p_garmin_body_single(self, p):
        'garmin_body : garmin_def'
        p[0] = [p[1]]
    
    def p_garmin_def(self, p):
        '''garmin_def : USERNAME STRING
                    | PASSWORD STRING'''
        p[0] = GarminDefNode(p[1], p[2])

    def p_durations(self, p):
        'durations : DURATIONS LBRACKET durations_body RBRACKET'
        p[0] = DurationsNode(p[3])

    def p_durations_body(self, p):
        'durations_body : durations_body duration_def'
        p[1].append(p[2])
        p[0] = p[1]

    def p_durations_body_single(self, p):
        'durations_body : duration_def'
        p[0] = [p[1]]

    def p_duration_def(self, p):
        'duration_def : ID duration'
        p[0] = DurationDefNode(p[1], p[2])

    def p_intensities(self, p):
        'intensities : INTENSITIES LBRACKET intensities_body RBRACKET'
        p[0] = IntensitiesNode(p[3])

    def p_intensities_body(self, p):
        'intensities_body : intensities_body intensity_def'
        p[1].append(p[2])
        p[0] = p[1]

    def p_intensities_body_single(self, p):
        'intensities_body : intensity_def'
        p[0] = [p[1]]

    def p_intensity_def(self, p):
        'intensity_def : ID intensity'
        p[0] = IntensityDefNode(p[1], p[2])

    def p_workout(self, p):
        'workout : workout_type ID LBRACKET workout_body RBRACKET'
        p[0] = WorkoutNode(p[1], p[2], p[4])

    def p_workout_type(self, p):
        '''workout_type : RUN
                       | STRENGTH'''
        p[0] = p[1]

    def p_workout_body(self, p):
        'workout_body : workout_body workout_step'
        p[1].append(p[2])
        p[0] = p[1]

    def p_workout_body_single(self, p):
        'workout_body : workout_step'
        p[0] = [p[1]]

    def p_workout_step(self, p):
        'workout_step : step_type duration AT intensity'
        p[0] = WorkoutStepNode(p[1], p[2], p[4])

    def p_workout_step_no_intensity(self, p):
        'workout_step : step_type duration'
        p[0] = WorkoutStepNode(p[1], p[2])

    def p_workout_step_no_duration(self, p):
        'workout_step : step_type AT intensity'
        p[0] = WorkoutStepNode(p[1], intensity=p[3])

    def p_workout_step_no_duration_intensity(self, p):
        'workout_step : step_type'
        p[0] = WorkoutStepNode(p[1])

    def p_workout_step_times_body(self, p):
        'workout_step : INT_REP LBRACKET workout_body RBRACKET'
        p[0] = WorkoutStepRepeatNode(p[1], p[3])

    def p_workout_step_times(self, p):
        'workout_step : INT_REP workout_step'
        p[0] = WorkoutStepRepeatNode(p[1], [p[2]])

    def p_step_type(self, p):
        '''step_type : WARMUP
                    | COOLDOWN
                    | RUN
                    | RECOVER
                    | REST
                    | OTHER'''
        p[0] = p[1]

    def p_duration_time(self, p):
        'duration : TIME'
        p[0] = DurationTimeNode(p[1])

    def p_duration_distance(self, p):
        'duration : distance'
        p[0] = DurationDistanceNode(p[1])

    def p_duration_calories(self, p):
        'duration : INT CALORIES'
        p[0] = DurationCaloriesNode(p[1])

    def p_duration_heart_rate_above(self, p):
        'duration : ABOVE INT BPM'
        p[0] = DurationHRAboveBelowNode(p[1], p[2])

    def p_duration_heart_rate_below(self, p):
        'duration : BELOW INT BPM'
        p[0] = DurationHRAboveBelowNode(p[1], p[2])

    def p_duration_id(self, p):
        'duration : ID'
        p[0] = DurationIDNode(p[1])

    def p_distance(self, p):
        '''distance : INT
                    | FLOAT'''
        p[0] = float(p[1])

    def p_intensity_pace(self, p):
        'intensity : TIME HYPHEN TIME'
        p[0] = IntensityPaceNode(p[1], p[3])

    def p_intensity_cadence(self, p):
        'intensity : INT HYPHEN INT SPM'
        p[0] = IntensityCadenceNode(p[1], p[3])

    def p_intensity_hr_zone(self, p):
        'intensity : HR ZONE INT'
        p[0] = IntensityHRZoneNode(p[3])

    def p_intensity_custom_hr(self, p):
        'intensity : INT HYPHEN INT BPM'
        p[0] = IntensityHRNode(p[1], p[3])

    def p_intensity_power_zone(self, p):
        'intensity : POWER ZONE INT'
        p[0] = IntensityPowerZoneNode(p[3])

    def p_intensity_custom_power(self, p):
        'intensity : INT HYPHEN INT WATTS'
        p[0] = IntensityPowerNode(p[1], p[3])

    def p_intensity_id(self, p):
        'intensity : ID'
        p[0] = IntensityIDNode(p[1])

    def p_error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}, token='{p.type}', value='{p.value}'")
            print(f"Remaining input: {p.lexer.lexdata[p.lexpos:]}")
            print(f"Lexer state: pos={p.lexpos}, lineno={p.lineno}")
        else:
            print("Syntax error at EOF")