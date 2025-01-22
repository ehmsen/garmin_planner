from typing import Dict, Any, List
from .parser import (
    RootNode, DurationsNode, IntensitiesNode, WorkoutNode, WorkoutStepNode,
    WorkoutStepRepeatNode, DurationTimeNode, DurationDistanceNode,
    DurationCaloriesNode, DurationHRAboveBelowNode, DurationIDNode,
    IntensityPaceNode, IntensityCadenceNode, IntensityHRZoneNode,
    IntensityHRNode, IntensityPowerZoneNode, IntensityPowerNode, IntensityIDNode,
    GarminNode, GarminDefNode
)

class GarminVisitor:
    def __init__(self):
        self.durations: Dict[str, Any] = {}
        self.intensities: Dict[str, Any] = {}
        self.step_order = 1
        self.username = None
        self.password = None

    def visit(self, node) -> Any:
        method_name = f"visit_{node.__class__.__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise NotImplementedError(f"No visit method for {type(node)}")

    def visit_RootNode(self, node: RootNode) -> Dict[str, Any]:
        # Skip any nodes not defined
        for child in node.children:
            if isinstance(child, (DurationsNode, IntensitiesNode, GarminNode)):
                self.visit(child)
            elif isinstance(child, WorkoutNode):
                return self.visit(child)
        return {}
    
    def visit_GarminNode(self, node: GarminNode) -> Dict[str, Any]:
        for def_node in node.definitions:
            if isinstance(def_node, GarminDefNode):
                name = def_node.name
                if name == "username":
                    self.username = def_node.value
                elif name == "password":
                    self.password = def_node.value

    def visit_DurationsNode(self, node: DurationsNode) -> None:
        for def_node in node.definitions:
            name = def_node.name
            self.durations[name] = self.visit(def_node.duration)

    def visit_IntensitiesNode(self, node: IntensitiesNode) -> None:
        for def_node in node.definitions:
            name = def_node.name
            self.intensities[name] = self.visit(def_node.intensity)

    def visit_WorkoutNode(self, node: WorkoutNode) -> Dict[str, Any]:
        sport_type = {
            "run": {"sportTypeId": 1, "sportTypeKey": "running"},
            "strength": {"sportTypeId": 3, "sportTypeKey": "strength"}
        }.get(node.workout_type.lower(), {"sportTypeId": 1, "sportTypeKey": "running"})

        steps = []
        self.step_order = 1
        for step in node.body:
            step_json = self.visit(step)
            if isinstance(step_json, list):
                for s in step_json:
                    s["stepOrder"] = self.step_order
                    self.step_order += 1
                steps.extend(step_json)
            else:
                step_json["stepOrder"] = self.step_order
                self.step_order += 1
                steps.append(step_json)

        return {
            "workoutName": node.name,
            "sportType": sport_type,
            "workoutSegments": [{
                "segmentOrder": 1,
                "sportType": sport_type,
                "workoutSteps": steps
            }]
        }

    def visit_WorkoutStepNode(self, node: WorkoutStepNode) -> Dict[str, Any]:
        step_types = {
            "warmup": {"stepTypeId": 1, "stepTypeKey": "warmup"},
            "cooldown": {"stepTypeId": 2, "stepTypeKey": "cooldown"},
            "run": {"stepTypeId": 3, "stepTypeKey": "interval"},
            "recover": {"stepTypeId": 4, "stepTypeKey": "recovery"},
            "rest": {"stepTypeId": 5, "stepTypeKey": "rest"},
            "other": {"stepTypeId": 7, "stepTypeKey": "other"}
        }

        step = {
            "type": "ExecutableStepDTO",
            "stepType": step_types.get(node.step_type.lower(), step_types["other"])
        }

        if node.duration:
            duration = self.visit(node.duration)
            step["endCondition"] = {
                "conditionTypeId": duration["conditionTypeId"],
                "conditionTypeKey": duration["conditionTypeKey"]
            }
            if "endConditionValue" in duration:
                step["endConditionValue"] = duration["endConditionValue"]
            if "endConditionCompare" in duration:
                step["endConditionCompare"] = duration["endConditionCompare"]
        else:
            step["endCondition"] = {
                "conditionTypeId": 1,
                "conditionTypeKey": "lap.button"
            }
        
        if node.intensity:
            intensity = self.visit(node.intensity)
            step["targetType"] = intensity["targetType"]
            if "targetValueOne" in intensity:
                step["targetValueOne"] = intensity["targetValueOne"]
            if "targetValueTwo" in intensity:
                step["targetValueTwo"] = intensity["targetValueTwo"]
            if "zoneNumber" in intensity:
                step["zoneNumber"] = intensity["zoneNumber"]
        else:
            step["targetType"] = {
                "workoutTargetTypeId": 1,
                "workoutTargetTypeKey": "no.target"
            }

        return step

    def visit_WorkoutStepRepeatNode(self, node: WorkoutStepRepeatNode) -> List[Dict[str, Any]]:
        step = {
            "type": "RepeatGroupDTO",
            "stepType": {
                "stepTypeId": 6,
                "stepTypeKey": "repeat"
            },
            "numberOfIterations": node.count
        }

        sub_steps = []
        sub_step_order = 1
        for sub_step in node.steps:
            sub_step_json = self.visit(sub_step)
            sub_step_json["stepOrder"] = sub_step_order
            sub_step_order += 1
            sub_steps.append(sub_step_json)

        step["workoutSteps"] = sub_steps

        return step

    def visit_DurationTimeNode(self, node: DurationTimeNode) -> Dict[str, Any]:
        total_seconds = node.time[0] * 3600 + node.time[1] * 60 + node.time[2]
        return {
            "conditionTypeId": 2,
            "conditionTypeKey": "time",
            "endConditionValue": total_seconds
        }

    def visit_DurationDistanceNode(self, node: DurationDistanceNode) -> Dict[str, Any]:
        return {
            "conditionTypeId": 3,
            "conditionTypeKey": "distance",
            "endConditionValue": int(node.distance * 1000)  # Convert to meters
        }

    def visit_DurationCaloriesNode(self, node: DurationCaloriesNode) -> Dict[str, Any]:
        return {
            "conditionTypeId": 4,
            "conditionTypeKey": "calories",
            "endConditionValue": node.calories
        }

    def visit_DurationHRAboveBelowNode(self, node: DurationHRAboveBelowNode) -> Dict[str, Any]:
        return {
            "conditionTypeId": 6,
            "conditionTypeKey": "heart.rate",
            "endConditionValue": node.hr_value,
            "endConditionCompare": "gt" if node.hr_type == "above" else "lt"
        }

    def visit_DurationIDNode(self, node: DurationIDNode) -> Dict[str, Any]:
        duration = self.visit(node.duration)
        return duration

    def visit_IntensityPaceNode(self, node: IntensityPaceNode) -> Dict[str, Any]:
        # Convert pace (min/km) to speed (m/s)
        min_speed = 1000 / (((node.min[0] * 60 + node.min[1]) * 60) + node.min[2])
        max_speed = 1000 / (((node.max[0] * 60 + node.max[1]) * 60) + node.max[2])
        return {
            "targetType": {
                "workoutTargetTypeId": 6,
                "workoutTargetTypeKey": "speed.zone"
            },
            "targetValueOne": min_speed,
            "targetValueTwo": max_speed
        }

    def visit_IntensityCadenceNode(self, node: IntensityCadenceNode) -> Dict[str, Any]:
        return {
            "targetType": {
                "workoutTargetTypeId": 3,
                "workoutTargetTypeKey": "cadence.zone"
            },
            "targetValueOne": node.min,
            "targetValueTwo": node.max
        }

    def visit_IntensityHRZoneNode(self, node: IntensityHRZoneNode) -> Dict[str, Any]:
        return {
            "targetType": {
                "workoutTargetTypeId": 4,
                "workoutTargetTypeKey": "heart.rate.zone"
            },
            "zoneNumber": node.zone
        }

    def visit_IntensityHRNode(self, node: IntensityHRNode) -> Dict[str, Any]:
        return {
            "targetType": {
                "workoutTargetTypeId": 4,
                "workoutTargetTypeKey": "heart.rate.zone"
            },
            "targetValueOne": node.min,
            "targetValueTwo": node.max
        }

    def visit_IntensityPowerZoneNode(self, node: IntensityPowerZoneNode) -> Dict[str, Any]:
        return {
            "targetType": {
                "workoutTargetTypeId": 2,
                "workoutTargetTypeKey": "power.zone"
            },
            "zoneNumber": node.zone
        }

    def visit_IntensityPowerNode(self, node: IntensityPowerNode) -> Dict[str, Any]:
        return {
            "targetType": {
                "workoutTargetTypeId": 2,
                "workoutTargetTypeKey": "power.zone"
            },
            "targetValueOne": node.min,
            "targetValueTwo": node.max
        }

    def visit_IntensityIDNode(self, node: IntensityIDNode) -> Dict[str, Any]:
        intensity = self.visit(node.intensity)
        return intensity