class GoalManager:
    def __init__(self):
        self.goals = {}  # Dictionary to store goals for each user

    def set_goal(self, user_id, goal):
        self.goals[user_id] = {"goal": goal, "progress": 0}  # Initialize progress to 0

    def get_goal_status(self, user_id):
        return self.goals.get(user_id)  # Returns None if no goal is set

    def update_progress(self, user_id, progress):
        if user_id in self.goals:
            self.goals[user_id]["progress"] = progress