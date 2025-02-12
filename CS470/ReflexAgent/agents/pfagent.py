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

        angle_to_goal = math.degrees(math.atan2(dy,dx))
        angle_from_front = angle_to_goal - robot_pos[2]
        angle_from_front = (angle_from_front + 180) % 360 - 180

        distance_to_goal= math.sqrt(dx**2 + dy**2)

        print("angle from robot to goal:", angle_to_goal)
        print("angle the robot is facing:", robot_pos[2])
        print("angle from the front of robot to goal maybe?",angle_from_front)

        travel_to_goal = True
        if (abs(dx) > 1) or (abs(dy) > 1):
            goal[0] = dx
            goal[1] = dy
            goal_norm = np.linalg.norm(goal)
            if goal_norm != 0:
                goal = goal/goal_norm

            threshold = 15.0
            inc = (2.0 * math.pi) / 16
            offset = (robot_pos[2]-90.0) * math.pi / 180.0
            travel_to_goal = False

            front_sensor_angle = math.degrees(offset + (4 * inc))
            if abs (angle_from_front) < 15:
                if(dist_sensors[4] > distance_to_goal):
                    travel_to_goal = True

            else:
                 # Find the safest direction by looking at the longest sensor range
                best_sensor_idx = np.argmax(dist_sensors)  # Sensor with max distance
                best_angle = offset + (best_sensor_idx * inc)  # Convert index to angle
                
                # goal[0] = robot_pos[0] + dist_sensors[best_sensor_idx] * math.cos(best_angle)
                # goal[1] = robot_pos[1] + dist_sensors[best_sensor_idx] * math.sin(best_angle)

            

            print(dist_sensors[4])
            for i in range (0,16):
                if (dist_sensors[i] < threshold):
                    sensor_angle = offset + (i * inc)
                    mag = (threshold - dist_sensors[i]) / threshold
                    obstacle[0] += mag * math.cos(sensor_angle - math.pi / 1.5)
                    obstacle[1] += mag * math.sin(sensor_angle - math.pi/1.5)

        if travel_to_goal:
            trajectory = goal
        else:
            trajectory = goal + obstacle * 1.2

        trajectory_norm = np.linalg.norm(trajectory)
        if trajectory_norm != 0:
            trajectory = trajectory / trajectory_norm
        
        return trajectory
