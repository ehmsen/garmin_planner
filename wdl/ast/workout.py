from .base import ASTNode

class WorkoutNode(ASTNode):
    def __init__(self, workout_type, name, body):
        super().__init__(children=body)
        self.workout_type = workout_type
        self.name = name
        self.body = body
    
    def get_duration_estimate(self):
        duration_estimates = [step.get_duration_estimate() for step in self.body]
        duration_estimates = [d for d in duration_estimates if d is not None]
        return int(sum(duration_estimates))
    
    def get_distance_estimate(self):
        distance_estimates = [step.get_distance_estimate() for step in self.body]
        distance_estimates = [d for d in distance_estimates if d is not None]
        return int(sum(distance_estimates))

class WorkoutStepNode(ASTNode):
    def __init__(self, step_type, duration=None, intensity=None):
        super().__init__(children=[e for e in [duration, intensity] if e is not None])
        self.step_type = step_type
        self.duration = duration
        self.intensity = intensity
    
    def get_duration_estimate(self):
        duration = self.duration.get_duration() if self.duration else None
        if duration is not None:
            return duration
        
        distance = self.duration.get_distance() if self.duration else None
        speed = self.intensity.get_avg_speed() if self.intensity else None
        if distance is not None and speed is not None:
            return distance / speed

        return None
    
    def get_distance_estimate(self):
        distance = self.duration.get_distance() if self.duration else None
        if distance is not None:
            return distance

        duration = self.duration.get_duration() if self.duration else None
        speed = self.intensity.get_avg_speed() if self.intensity else None
        if duration is not None and speed is not None:
            return duration * speed

        return None

class WorkoutStepRepeatNode(ASTNode):
    def __init__(self, count, steps):
        super().__init__(children=steps)
        self.count = count
        self.steps = steps
    
    def get_duration_estimate(self):
        duration_estimates = [step.get_duration_estimate() for step in self.steps]
        duration_estimates = [d for d in duration_estimates if d is not None]
        if duration_estimates:
            return sum(duration_estimates) * self.count
        return None

    def get_distance_estimate(self):
        distance_estimates = [step.get_distance_estimate() for step in self.steps]
        distance_estimates = [d for d in distance_estimates if d is not None]
        if distance_estimates:
            return sum(distance_estimates) * self.count
        return None
