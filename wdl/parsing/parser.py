import ply.yacc as yacc
from .tokens import tokens
import logging

from ..ast import (
    ASTNode,
    RootNode,
    WorkoutNode,
    WorkoutStepNode,
    WorkoutStepRepeatNode,
    ProgramNode,
    ProgramWeekNode,
    PlanNode,
    PlanWeekNode,
    IntensitiesNode,
    IntensityDefNode,
    IntensityPaceNode,
    IntensityCadenceNode,
    IntensityHRZoneNode,
    IntensityHRNode,
    IntensityPowerZoneNode,
    IntensityPowerNode,
    IntensityIDNode,
    GarminNode,
    GarminDefNode,
    DurationsNode,
    DurationDefNode,
    DurationTimeNode,
    DurationDistanceNode,
    DurationCaloriesNode,
    DurationHRAboveBelowNode,
    DurationIDNode
)

logger = logging.getLogger(__name__)

class WDLParser:
    def __init__(self, lexer):
        self.parser = None
        self.lexer = lexer
        self.input = None
        self.tokens = tokens

    def build(self):
        self.parser = yacc.yacc(module=self)

    def parse(self, input):
        self.input = input
        return self.parser.parse(input, lexer=self.lexer.lexer, tracking=True)

    def set_span(self, p, ast_node):
        (start_line, end_line) = p.linespan(0)
        (start, end) = p.lexspan(0)
        start_column = start - self.input.rfind('\n', 0, start)
        end_column = end - self.input.rfind('\n', 0, end)
        ast_node.set_span((start_line, start_column), (end_line, end_column))

    def p_root(self, p):
        'root : main_body'
        p[0] = RootNode(p[1])
        self.set_span(p, p[0])

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
                   | garmin
                   | program
                   | plan'''
        p[0] = p[1]

    def p_plan(self, p):
        'plan : PLAN ID DATE_ISO8601 LBRACKET plan_body RBRACKET'
        p[0] = PlanNode(p[2], p[3], p[5])
        self.set_span(p, p[0])

    def p_plan_body(self, p):
        'plan_body : plan_week'
        p[0] = p[1]

    def p_plan_week(self, p):
        'plan_week : WEEK LBRACKET plan_week_body RBRACKET'
        p[0] = PlanWeekNode(p[3])
        self.set_span(p, p[0])
    
    def p_plan_week_body(self, p):
        'plan_week_body : plan_week_body plan_day'
        p[1].append(p[2])
        p[0] = p[1]
    
    def p_plan_week_body_single(self, p):
        'plan_week_body : plan_day'
        p[0] = [p[1]]
    
    def p_plan_day(self, p):
        'plan_day : WEEKDAY ID'
        p[0] = (p[1], p[2])

    def p_program(self, p):
        'program : PROGRAM ID LBRACKET program_body RBRACKET'
        p[0] = ProgramNode(p[2], p[4])
        self.set_span(p, p[0])
    
    def p_program_body(self, p):
        'program_body : program_body program_week'
        p[1].append(p[2])
        p[0] = p[1]
    
    def p_program_body_single(self, p):
        'program_body : program_week'
        p[0] = [p[1]]
    
    def p_program_week(self, p):
        'program_week : WEEK INT LBRACKET program_week_body RBRACKET'
        p[0] = ProgramWeekNode(p[2], p[4])
        self.set_span(p, p[0])

    def p_program_week_body(self, p):
        'program_week_body : program_week_body workout'
        p[1].append(p[2])
        p[0] = p[1]
    
    def p_program_week_body_single(self, p):
        'program_week_body : workout'
        p[0] = [p[1]]

    def p_garmin(self, p):
        'garmin : GARMIN LBRACKET garmin_body RBRACKET'
        p[0] = GarminNode(p[3])
        self.set_span(p, p[0])
    
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
        self.set_span(p, p[0])

    def p_durations(self, p):
        'durations : DURATIONS LBRACKET durations_body RBRACKET'
        p[0] = DurationsNode(p[3])
        self.set_span(p, p[0])

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
        self.set_span(p, p[0])

    def p_intensities(self, p):
        'intensities : INTENSITIES LBRACKET intensities_body RBRACKET'
        p[0] = IntensitiesNode(p[3])
        self.set_span(p, p[0])

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
        self.set_span(p, p[0])

    def p_workout(self, p):
        'workout : workout_type ID LBRACKET workout_body RBRACKET'
        p[0] = WorkoutNode(p[1], p[2], p[4])
        self.set_span(p, p[0])

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
        self.set_span(p, p[0])

    def p_workout_step_no_intensity(self, p):
        'workout_step : step_type duration'
        p[0] = WorkoutStepNode(p[1], p[2])
        self.set_span(p, p[0])

    def p_workout_step_no_duration(self, p):
        'workout_step : step_type AT intensity'
        p[0] = WorkoutStepNode(p[1], intensity=p[3])
        self.set_span(p, p[0])

    def p_workout_step_no_duration_intensity(self, p):
        'workout_step : step_type'
        p[0] = WorkoutStepNode(p[1])
        self.set_span(p, p[0])

    def p_workout_step_times_body(self, p):
        'workout_step : INT_REP LBRACKET workout_body RBRACKET'
        p[0] = WorkoutStepRepeatNode(p[1], p[3])
        self.set_span(p, p[0])

    def p_workout_step_times(self, p):
        'workout_step : INT_REP workout_step'
        p[0] = WorkoutStepRepeatNode(p[1], [p[2]])
        self.set_span(p, p[0])

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
        self.set_span(p, p[0])

    def p_duration_distance(self, p):
        'duration : distance'
        p[0] = DurationDistanceNode(p[1])
        self.set_span(p, p[0])

    def p_duration_calories(self, p):
        'duration : INT CALORIES'
        p[0] = DurationCaloriesNode(p[1])
        self.set_span(p, p[0])

    def p_duration_heart_rate_above(self, p):
        'duration : ABOVE INT BPM'
        p[0] = DurationHRAboveBelowNode(p[1], p[2])
        self.set_span(p, p[0])

    def p_duration_heart_rate_below(self, p):
        'duration : BELOW INT BPM'
        p[0] = DurationHRAboveBelowNode(p[1], p[2])
        self.set_span(p, p[0])

    def p_duration_id(self, p):
        'duration : ID'
        # if not p[1] in durations_defintions:
        #     raise ValueError(f"Duration '{p[1]}' not defined")
        # p[0] = DurationIDNode(p[1], durations_defintions[p[1]])
        p[0] = DurationIDNode(p[1])
        self.set_span(p, p[0])

    def p_distance(self, p):
        '''distance : INT
                    | FLOAT'''
        p[0] = float(p[1])

    def p_intensity_pace(self, p):
        'intensity : TIME HYPHEN TIME'
        p[0] = IntensityPaceNode(p[1], p[3])
        self.set_span(p, p[0])

    def p_intensity_cadence(self, p):
        'intensity : INT HYPHEN INT SPM'
        p[0] = IntensityCadenceNode(p[1], p[3])
        self.set_span(p, p[0])

    def p_intensity_hr_zone(self, p):
        'intensity : HR ZONE INT'
        p[0] = IntensityHRZoneNode(p[3])
        self.set_span(p, p[0])

    def p_intensity_custom_hr(self, p):
        'intensity : INT HYPHEN INT BPM'
        p[0] = IntensityHRNode(p[1], p[3])
        self.set_span(p, p[0])

    def p_intensity_power_zone(self, p):
        'intensity : POWER ZONE INT'
        p[0] = IntensityPowerZoneNode(p[3])
        self.set_span(p, p[0])

    def p_intensity_custom_power(self, p):
        'intensity : INT HYPHEN INT WATTS'
        p[0] = IntensityPowerNode(p[1], p[3])
        self.set_span(p, p[0])

    def p_intensity_id(self, p):
        'intensity : ID'
        # if not p[1] in intensities_defintions:
        #     raise ValueError(f"Intensity '{p[1]}' not defined")
        # p[0] = IntensityRef(p[1], intensities_defintions[p[1]])
        p[0] = IntensityIDNode(p[1])
        self.set_span(p, p[0])

    def p_error(self, p):
        if p:
            logger.error(f"Syntax error at line {p.lineno}, token='{p.type}', value='{p.value}'")
            logger.debug(f"Remaining input: {self.parser.lexer.lexdata[p.lexpos:]}")
        else:
            logger.error("Syntax error at EOF")