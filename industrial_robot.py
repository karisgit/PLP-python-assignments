#Class: Blueprint for creating objects
#Object: Instance of a class (like welder or painter)
#Inheritance: Child classes get properties from parent class
#Methods: Functions that belong to a class
#Attributes: Variables that store data about the object
#Inheritance: WeldingRobot and PaintingRobot inherit from IndustrialRobot
#Polymorphism: Each robot type has its own specialized behavior
#----------------------------------------------------------------------------------



class IndustrialRobot:
    
    def __init__(self, name, robot_type, max_weight):
        # Constructor - initializes the robot with unique values
        self.name = name          # Robot's name/ID
        self.robot_type = robot_type  # Type of robot (welding, painting, etc.)
        self.max_weight = max_weight  # Maximum weight it can lift (kg)
        self.is_working = False   # Is the robot currently working?
        self.tasks_completed = 0  # Count of completed tasks
    
    def start_work(self):
        if not self.is_working:
            self.is_working = True
            print(f"{self.name} is now working, keep safe distance!")
        else:
            print(f"{self.name} is already working!")
    
    def stop_work(self):
        if self.is_working:
            self.is_working = False
            print(f"{self.name} has stopped working.")
        else:
            print(f"{self.name} is not working right now.")
    
    def perform_task(self, task_name):
        if self.is_working:
            print(f"{self.name} is performing: {task_name}")
            self.tasks_completed += 1
            return f"Task '{task_name}' completed successfully!"
        else:
            return "Robot is not working. Start work first!"
    
    def lift_object(self, weight):
        if weight <= self.max_weight:
            return f"{self.name} lifted {weight}kg object!"
        else:
            return f"Too heavy! {self.name} can only lift {self.max_weight}kg."
    
    def get_status(self):
        status = "working" if self.is_working else "idle"
        return f"{self.name} ({self.robot_type}) is {status}. Tasks completed: {self.tasks_completed}"

# Create a specialized WeldingRobot class that inherits from IndustrialRobot
class WeldingRobot(IndustrialRobot):
    
    def __init__(self, name, max_weight, welding_type):
        # Call the parent class constructor
        super().__init__(name, "Welding Robot", max_weight)
        self.welding_type = welding_type  # Special attribute for welding robot
        self.welds_completed = 0
    
    def perform_weld(self, material):
        """Special method only for welding robots"""
        if self.is_working:
            result = self.perform_task(f"Welding {material} with {self.welding_type}")
            self.welds_completed += 1
            return result + f" Total welds: {self.welds_completed}"
        else:
            return "Start work first!"
    
    def get_status(self):
        """Override the parent method to show welding-specific info"""
        base_status = super().get_status()
        return base_status + f" | Welds: {self.welds_completed}"


# Create a specialized PaintingRobot class
class PaintingRobot(IndustrialRobot):
    
    def __init__(self, name, max_weight, color):
        super().__init__(name, "Painting Robot", max_weight)
        self.color = color
        self.surfaces_painted = 0
    
    def paint_surface(self, surface):
        """Special method for painting robots"""
        if self.is_working:
            result = self.perform_task(f"Painting {surface} with {self.color} paint")
            self.surfaces_painted += 1
            return result + f" 🎨"
        else:
            return "Start work first!"
    
    def change_color(self, new_color):
        self.color = new_color
        return f"Paint color changed to {new_color}!"

# Robots tests.
print("=== ROBOT FACTORY DEMO ===\n")

# Create a basic industrial robot
basic_robot = IndustrialRobot("Robo-001", "General Purpose", 50)
print(basic_robot.get_status())

basic_robot.start_work()
print(basic_robot.perform_task("Moving parts"))
print(basic_robot.lift_object(30))
print(basic_robot.lift_object(60))  # Too heavy!
print()

# Create a welding robot (inheritance example)
welder = WeldingRobot("WeldMaster-2000", 40, "MIG Welding")
print(welder.get_status())

welder.start_work()
print(welder.perform_weld("steel"))
print(welder.perform_weld("aluminum"))
print(welder.get_status())
print()

# Create a painting robot (inheritance example)
painter = PaintingRobot("PaintPro-3000", 25, "blue")
print(painter.get_status())

painter.start_work()
print(painter.paint_surface("car door"))
print(painter.change_color("red"))
print(painter.paint_surface("bonnet"))
print(painter.get_status())
print()

# Show that all robots can use the same basic methods (polymorphism)
robots = [basic_robot, welder, painter]

print("=== ALL ROBOTS STATUS ===")
for robot in robots:
    # Each robot has its own version of get_status()
    print(robot.get_status())
    # All robots can perform tasks
    if robot.is_working:
        print(robot.perform_task("cleaning up"))
    print()
