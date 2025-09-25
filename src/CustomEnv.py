import gymnasium as gym
import numpy as np
from gymnasium import spaces


class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, num_processes=5):
        super().__init__()

        self.num_processes = num_processes


        self.action_space = spaces.Discrete(self.num_processes)
        self.observation_space = spaces.Box(low = 0, high=np.inf, shape=(self.num_processes, 2), dtype=np.float32)
        self.burst_times = np.zeros(self.num_processes, dtype=np.float32)
        self.remaining_times = np.zeros(self.num_processes, dtype=np.float32)
        self.waiting_times = np.zeros(self.num_processes, dtype=np.float32)
        self.current_time = 0


    def get_observation(self):
        is_completed = (self.remaining_times == 0).astype(np.float32)
        return np.column_stack([self.remaining_times, is_completed])
    
    def get_info(self):

        return {"total_waiting_time": np.sum(self.waiting_times)}

    
    def step(self, action):
        
        if self.remaining_times[action] == 0:
            reward = -100.0
            terminated = True
            observation = self.get_observation()
            info = self.get_info()
            return observation, reward, terminated, False, info
        
        run_time = self.remaining_times[action]

        self.current_time += run_time

        for i in range(self.num_processes):
            if i != action and self.remaining_times[i] > 0:
                self.waiting_times[i] += run_time

        
        self.remaining_times[action] = 0


        reward = -float(run_time)

        terminated = bool(np.all(self.remaining_times == 0))


        observation = self.get_observation()
        info = self.get_info()






        return observation, reward, terminated, False, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.burst_times = self.np_random.integers(1, 11, size=self.num_processes).astype(np.float32)
        self.remaining_times = self.burst_times.copy()

        self.waiting_times = np.zeros(self.num_processes, dtype=np.float32)
        self.current_time = 0
        
        observation = self.get_observation()
        info = self.get_info()

        return observation, info

    def render(self):
        if self.render_mode == "human":
            print(f"Current Time: {self.current_time}")
            print(f"Remaining Times: {self.remaining_times}")
            print(f"Waiting Times: {self.waiting_times}")
            print("-" * 30)


    

