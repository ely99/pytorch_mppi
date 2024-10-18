import gymnasium as gym
import numpy as np
import gymnasium.spaces as spaces

class ModifyJointsWrapper(gym.ActionWrapper):
    def __init__(self, env):
        super(ModifyJointsWrapper, self).__init__(env)
        # Define a 7D action space manually
        self.action_space = spaces.Box(low=-1, high=1, shape=(7,), dtype=np.float32)

    def action(self, action):
        print(f"Initial action: {action}")  # Debugging statement

        # Modify specific joints if there are actions to modify
        action[2] = 0.0  # Freeze the elbow roll
        action[4] = 0.0  # Freeze the forearm roll
        action[5] = 0.0  # Freeze the wrist flex
        action[6] = 0.0  # Freeze the wrist roll

        return action

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        mujoco_env = self.env.unwrapped  # Unwrap to access Mujoco
        mujoco_env.data.qpos[5] = 0  # Set joint positions to zero
        mujoco_env.data.qpos[6] = 0  # Set joint positions to zero
        return obs, info

# Load the environment using the original XML file
env = gym.make('Pusher-v5', xml_file="pusher_v5_original.xml", render_mode='human')
wrapped_env = ModifyJointsWrapper(env)

# Initial reset
observation, _ = wrapped_env.reset()
print("Action Space:", wrapped_env.action_space)

# Print detailed action space info
print("Action Space Details:")
print(f"Shape: {wrapped_env.action_space.shape}")
print(f"Low: {wrapped_env.action_space.low}")
print(f"High: {wrapped_env.action_space.high}")

# Manually setting the initial action
initial_action = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])  # Example custom control action
wrapped_env.step(initial_action)

# Environment loop
for step_num in range(1000):
    wrapped_env.render()


    #here i have to put the snext action (in our case it is a prediction) computed by the MPPI

    


    action = wrapped_env.action_space.sample()  # Take a random action
    try:
        observation, reward, done, truncated, info = wrapped_env.step(action)
        print(f"Step {step_num} - Action: {action} - Reward: {reward}")
    except Exception as e:
        print(f"Error during step: {e}")
        break

    if done or truncated:
        wrapped_env.reset()

wrapped_env.close()
