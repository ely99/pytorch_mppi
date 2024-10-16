import torch
import gymnasium as gym
import numpy as np


env = gym.make('Pusher-v5')

wrist_joints = ['r_wrist_flex_joint', 'r_wrist_roll_joint']  # Example names
#wrist_joint_ids = [env.env.sim.model.joint_name2id(name) for name in wrist_joints]

