import gym
import gym_nat
import time
from agent import AgentBasic, AgentRandom, AgentLearning
import threading
# clock = pygame.time.Clock()

env = gym.make("nat-v0")
def environment_info(env):
    ''' Prints info about the given environment. '''
    print('************** Environment Info **************')
    print('Observation space: {}'.format(env.observation_space))
    print('Observation space high values: {}'.format(env.observation_space.high))
    print('Observation space low values: {}'.format(env.observation_space.low))
    print('Action space: {}'.format(env.action_space))
    print()

def basic_guessing_policy(env, agent):
    ''' Execute random guessing policy. '''
    totals = []
    for episode in range(500):
        episode_rewards = 0
        obs = env.reset()
        # env.render()
        for step in range(1000):  # 1000 steps max unless failure
            action = agent.act(obs)
            obs, reward, done, info = env.step(action)
            episode_rewards += reward
            # env.render()
            if done:
                # Terminal state reached, reset environment
                break
        totals.append(episode_rewards)

    print('************** Reward Statistics **************')
    print('Average: {}'.format(np.mean(totals)))
    print('Standard Deviation: {}'.format(np.std(totals)))
    print('Minimum: {}'.format(np.min(totals)))
    print('Maximum: {}'.format(np.max(totals)))    
# observation = env.reset()
# clock = pygame.time.Clock()

# ready = False
# def render(env):
#     global ready
#     while True:
#         if not ready:
#             continue
#         action = env.action_space.sample() # your agent here (this takes random actions)        
#         res = env.step(action)
#         if res:
#             observation, reward, done, info = res
#         time.sleep(.5)

    
# thread = threading.Thread(target=render, args=(env,))
# thread.start()

# start_time = time.time() # start time of the loop    
# env.reset()
# while True:
#     env.render()
#     action = env.action_space.sample() # your agent here (this takes random actions)
#     if time.time() - start_time > .02:
#         env.step(action)
#         start_time = time.time()
#         print("K")
#     # time.sleep(0.01)
# #     ready = True    
# #     print()
# #     print('ts=', time.time() - start_time)
# #     start_time = time.time()
# #     print("FPS: ", 1.0 / (time.time() - start_time))
# env.close()
# print("done")

agent = AgentRandom(env.action_space)
environment_info(env)

start_time = time.time() # start time of the loop    
totals = []
for episode in range(5000):
    episode_rewards = 0
    obs = env.reset()
    for step in range(10000):  # 1000 steps max
        env.render()
        # action = agent.
        if time.time() - start_time > .01:
            action = env.action_space.sample() # your agent here (this takes random actions)
            # env.step(action)
            # obs, reward, done, info = env.step(action)
            # episode_rewards += reward
            # env.episode(episode, step, episode_rewards)
            start_time = time.time()
            # if done:
            #     # print('ep {} reward={}'.format(episode, episode_rewards))
            #     break
    totals.append(episode_rewards)