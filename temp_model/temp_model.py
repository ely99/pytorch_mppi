import gymnasium as gym
import numpy as np

flag_wrapped = 1

class ModifyJointsWrapper(gym.ActionWrapper):
    def __init__(self, env):
        super(ModifyJointsWrapper, self).__init__(env)

    def action(self, action):
        print(f"Initial action: {action}")  # Debugging statement
        
        # If the action space has zero dimensions, return a zero action.
        if self.action_space.shape[0] == 0:
            print("Action space is empty. No action will be sent.")
            return np.zeros(0)  # Returning an empty action to match the expected size

        # Check if action has the expected size
        if len(action) < 7:
            print(f"Action size is less than 7. Adjusting to zeros: {action}")
            action = np.zeros(7)  # Use zeros if action is not sufficiently sized
        
        # Modify specific joints if there are actions to modify
        action[2] = 0.0  # Freeze the elbow roll
        action[4] = 0.0  # Freeze the forearm roll
        action[5] = 0.0  # Freeze the wrist flex
        action[6] = 0.0  # Freeze the wrist roll
        
        return action

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        mujoco_env = self.env.unwrapped  # Unwrap to access Mujoco
        mujoco_env.data.qpos[5] = np.pi / 2  # Set joint positions
        mujoco_env.data.qpos[6] = np.pi
        return obs, info

# Load and Wrap the environment
if flag_wrapped:
    env = gym.make('Pusher-v5' ,xml_file="pusher_v5_modified.xml", render_mode='human')
    wrapped_env = ModifyJointsWrapper(env)
else:
    env = gym.make('Pusher-v5', xml_file = "pusher_v5_original.xml", render_mode='human')
    wrapped_env = env

# Initial reset
observation, _ = wrapped_env.reset()
print("Action Space:", wrapped_env.action_space)  # Check action space
print("Action Space Shape:", wrapped_env.action_space.shape)

# Environment loop
for _ in range(1000):
    wrapped_env.render()

    # Handle action based on action space shape
    if wrapped_env.action_space.shape[0] == 0:
        action = np.zeros(0)  # Set a default action of zeros (no action)
    else:
        action = wrapped_env.action_space.sample()  # Take a random action

    # Step through the environment
    try:
        observation, reward, done, truncated, info = wrapped_env.step(action)  # Unpack with truncated
    except Exception as e:
        print(f"Error during step: {e}")
        break  # Exit loop on error

    if done or truncated:
        wrapped_env.reset()  # Reset if done or truncated

wrapped_env.close()
