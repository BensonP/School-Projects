import numpy as np

from .baseagent import Agent

class PFAgent(Agent):
    def __init__(self):
        super().__init__()

    def act(self, robot_pos, goal_pos, dist_sensors):
        # TODO: implement potential fields
        trajectory = np.ones(2)

        trajectory_norm = np.linalg.norm(trajectory)
        if trajectory_norm != 0:
            trajectory = trajectory / trajectory_norm

        return trajectory
