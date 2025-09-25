from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
import CustomEnv

env = CustomEnv.CustomEnv(num_processes=5)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=1000000)


obs, _ = env.reset()
for _ in range(100): 
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()
    if terminated or truncated:
        print("Episode finished")
        print(f"Total waiting time: {info['total_waiting_time']}")
        break

env.close()

