import numpy as np
from csv import writer
from pandas import read_csv, DataFrame
import matplotlib.pyplot as plt

## Shared methods
def harvest_draw(self, quota):
    """
    Select a value to harvest at each time step.
    """
    
    ## index (fish.population[0]) to avoid promoting float to array
    self.harvest = min(self.fish_population[0], quota)
    self.fish_population = max(self.fish_population - self.harvest, 0.0)
    return self.harvest

def population_draw(self):
    """
    Select a value for population to grow or decrease at each time step.
    """
    self.fish_population = max(
                            self.fish_population + self.r * self.fish_population \
                            * (1.0 - self.fish_population / self.K) \
                            + self.fish_population * self.sigma * np.random.normal(0,1),
                            0.0)
    return self.fish_population


def csv_entry(self):
  row_contents = [self.years_passed, 
                  self.state[0],
                  self.action,
                  self.reward]
  csv_writer = writer(self.write_obj)
  csv_writer.writerow(row_contents)
  return row_contents
    
def simulate_mdp(env, model, reps = 1):
  row = []
  for rep in range(reps):
    obs = env.reset()
    for t in range(env.Tmax):
      action, _state = model.predict(obs)
      obs, reward, done, info = env.step(action)
      row.append([t, obs, action, reward, rep])
      if done:
        break
  df = DataFrame(row, columns=['time', 'state', 'action', 'reward', "rep"])
  return df


def estimate_policyfn(env, model, reps = 1):
  row = []
  for rep in range(reps):
    for obs in range(2*env.K):
      action, _state = model.predict(obs)
      row.append([obs, action, rep])
      if done:
        break
  df = DataFrame(row, columns=['state', 'action', 'rep'])
  return df

def plot_mdp(self, df, output = "results.png"):
  fig, axs = plt.subplots(3,1)
  for i in range(np.max(df.rep)):
    results = df[df.rep == i]
    episode_reward = np.cumsum(results.reward)                    
    axs[0].plot(results.time, results.state, color="blue", alpha=0.3)
    axs[1].plot(results.time, results.action, color="blue", alpha=0.3)
    axs[2].plot(results.time, episode_reward, color="blue", alpha=0.3)
  
  axs[0].set_ylabel('state')
  axs[1].set_ylabel('action')
  axs[2].set_ylabel('reward')
  fig.tight_layout()
  plt.savefig(output)
  plt.close("all")
