import numpy as np
import math

from .baseagent import Agent

class PFAgent(Agent):
    def __init__(self):
        super().__init__()

    def act(self, robot_pos, goal_pos, dist_sensors):
        # TODO: implement potential fields
        trajectory = np.zeros(2)
        goal = np.zeros(2)
        obstacle = np.zeros(2)

        dx = goal_pos[0] - robot_pos[0]
        dy = goal_pos[1] - robot_pos[1]

        if (abs(dx) > 1) or (abs(dy) > 1):
            goal[0] = dx
            goal[1] = dy
            goal_norm = np.linalg.norm(goal)
            if goal_norm != 0:
                goal = goal/goal_norm

            threshold = 15.0
            inc = (2.0 * math.pi) / 16
            offset = (robot_pos[2]-90.0) * math.pi / 180.0

            for i in range (0,16):
                if (dist_sensors[i] < threshold):
                    sensor_angle = offset + (i * inc)
                    mag = (threshold - dist_sensors[i]) / threshold
                    obstacle[0] += mag * math.cos(sensor_angle - math.pi / 1.5)
                    obstacle[1] += mag * math.sin(sensor_angle - math.pi/1.5)

        trajectory = goal + obstacle *.66

        trajectory_norm = np.linalg.norm(trajectory)
        if trajectory_norm != 0:
            trajectory = trajectory / trajectory_norm
        
        return trajectory
