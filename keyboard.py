import gym
import gym_nat
import time
from agent import AgentBasic, AgentRandom, AgentLearning
import numpy as np
import threading

# clock = pygame.time.Clock()

env = gym.make("nat-v0")

if not hasattr(env.action_space, 'n'):
	raise Exception('Keyboard agent only supports discrete action spaces')
ACTIONS = env.action_space.n
SKIP_CONTROL = 0  # Use previous control decision SKIP_CONTROL times, that's how you
# can test what skip is still usable.

human_agent_action = 0
human_wants_restart = False
human_sets_pause = False


def key_press(key, mod):
	global human_agent_action, human_wants_restart, human_sets_pause
	if key == 0xff0d: human_wants_restart = True
	if key == 32: human_sets_pause = not human_sets_pause
	a = int(key - ord('0'))

	# print('press', str(a))
	if a <= 0 or a >= ACTIONS: return
	human_agent_action = a


def key_release(key, mod):
	global human_agent_action
	a = int(key - ord('0'))
	if a <= 0 or a >= ACTIONS: return
	if human_agent_action == a:
		human_agent_action = 0


env.render()
env.unwrapped.viewer.window.on_key_press = key_press
env.unwrapped.viewer.window.on_key_release = key_release

#
# def rollout(env):
# 	global human_agent_action, human_wants_restart, human_sets_pause
# 	human_wants_restart = False
# 	obser = env.reset()
# 	skip = 0
# 	total_reward = 0
# 	total_timesteps = 0
# 	while 1:
# 		if not skip:
# 			# print("taking action {}".format(human_agent_action))
# 			a = human_agent_action
# 			total_timesteps += 1
# 			skip = SKIP_CONTROL
# 		else:
# 			skip -= 1
#
# 		obser, r, done, info = env.step(a)
# 		if r != 0:
# 			print("reward %0.3f" % r)
# 		total_reward += r
# 		window_still_open = env.render()
# 		if window_still_open == False: return False
# 		if done: break
# 		if human_wants_restart: break
# 		while human_sets_pause:
# 			env.render()
# 			time.sleep(0.1)
# 		time.sleep(0.1)
# 	print("timesteps %i reward %0.2f" % (total_timesteps, total_reward))
#

print("ACTIONS={}".format(ACTIONS))
print("Press keys 1 2 3 ... to take actions 1 2 3 ...")
print("No keys pressed is taking action 0")

# while 1:
# 	window_still_open = rollout(env)
# 	if window_still_open == False: break
start_time = time.time()  # start time of the loop
totals = []
for episode in range(50000):
	episode_rewards = 0
	obs = env.reset()
	for step in range(1000):  # 1000 steps max
		env.render()
		# action = agent.
		if time.time() - start_time > .02 / 4:
			action = env.action_space.sample()  # your agent here (this takes random actions)
			action = human_agent_action
			print(action)
			# env.step(action)
			# action = agent.act()
			obs, reward, done, info = env.step(action)
			episode_rewards += reward
			env.episode(episode, step, episode_rewards)
			start_time = time.time()
			if done:
				print('ep {} step={} reward={}'.format(episode, step, episode_rewards))
				break
	totals.append(episode_rewards)
