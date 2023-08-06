import random
import numpy as np
import SimplePyAi.simplepyai as spa
from collections import deque

from tqdm import tqdm

color1 = '\033[92m'
color2 = '\033[94m'
color3 = '\033[0m'

print(
    f"{color1}You use the library SimplePyDeepQLearning !\n{color2}Credit: LeLaboDuGame on Twitch -> "
    f"https://twitch.tv/LeLaboDuGame{color3}")


def action_function(state, action):
    """

    :param state: Actual State
    :param action: Index of action
    :return: reward, next_state, done
    """
    return 1, [1, 1], True


def epsylone_greedy(epsylone):
    if np.random.rand() <= epsylone:
        return True
    else:
        return False


# Some functions
# -----------------------------------------------------------------------------------------------------------------------
# Models
class DeepQLearning:
    #                  state_size, action_size
    def __init__(self, input_size, output_size, learning_rate=0.05, gama=0.95, epsylone=1, epsylone_decay=0.995,
                 epsylone_min=0.1, batch_size=10, memory_max_len=2000, choose_action_function=epsylone_greedy,
                 ai_model=None, ai_model_is_a_tensorflow=False):
        self.ai_model_is_a_tensorflow = ai_model_is_a_tensorflow
        self.action_function = None
        self.initial_function = None
        self.batch_size = batch_size
        self.choose_action_function = choose_action_function
        self.epsylone_min = epsylone_min
        self.epsylone_decay = epsylone_decay
        self.epsylone = epsylone
        self.gama = gama
        self.learning_rate = learning_rate
        self.memory = deque(maxlen=memory_max_len)
        self.input_size = input_size
        self.output_size = output_size

        if ai_model is not None:
            self.ai_model = ai_model
        else:
            print(input_size, output_size)
            layers = [spa.Layer(input_size),
                      spa.Layer(64, activation_function=spa.relu, derivation_function=spa.relu_derivative,
                                optimizer=spa.AdamOptim(learning_rate=self.learning_rate)),
                      spa.Layer(64, activation_function=spa.relu, derivation_function=spa.relu_derivative,
                                optimizer=spa.AdamOptim(learning_rate=self.learning_rate)),
                      spa.Layer(output_size, activation_function=spa.linear, derivation_function=spa.linear_derivative,
                                optimizer=spa.AdamOptim(learning_rate=self.learning_rate))]
            self.ai_model = spa.Neural_Network(layers, loss_function=spa.mse, learning_rate=self.learning_rate)

    def save_in_memory(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        return self.memory

    def choose_action(self, state):
        if self.choose_action_function(self.epsylone):
            return random.randrange(self.output_size)
        if self.ai_model_is_a_tensorflow:
            self.ai_model.predict([state], verbose=0)
        else:
            prediction = self.ai_model.predict([state])
        return np.argmax(prediction[0])

    def train_model(self, train_iterations):
        minibatch = random.sample(self.memory, self.batch_size)
        last_A = None
        for state, action, reward, newt_state, done in minibatch:
            target = reward
            if not done:
                if self.ai_model_is_a_tensorflow:
                    target = (reward + self.gama * np.amax(self.ai_model.predict(newt_state, verbose=0)[0]))
                else:
                    target = (reward + self.gama * np.amax(self.ai_model.predict(newt_state)[0]))

            if self.ai_model_is_a_tensorflow:
                prediction = [self.ai_model.predict([state], verbose=0).flatten()]
            else:
                prediction = [self.ai_model.predict([state]).flatten()]

            prediction[0][action] = target
            if self.ai_model_is_a_tensorflow:
                last_A = self.ai_model.fit([state], prediction, epoch=1, verbose=0)
            else:
                last_A = self.ai_model.train([state], prediction, n_iter=train_iterations, show=False, verbose=False)

        return last_A

    """
    play with just ai_model = No random actions
    """

    def play(self):
        state = self.initial_function()
        done = False
        score = 0
        step = 0
        while not done:
            if self.ai_model_is_a_tensorflow:
                prediction = self.ai_model.predict([state], verbose=0)
            else:
                prediction = self.ai_model.predict([state])
            action = np.argmax(prediction[0])
            reward, next_state, done = action_function(state, action)
            score += reward
            step += 1
        print(
            f"Score: {score} | epsylone: {self.epsylone} | n step: {step}")

    def train(self, initial_function, iterations=100, action_function=action_function, train_iterations=1,
              verbose=3):
        last_A = None
        self.initial_function = initial_function
        self.action_function = action_function
        if verbose == 1:
            for i in tqdm(range(0, iterations)):
                state = initial_function()
                done = False
                while not done:
                    action = self.choose_action(state)
                    reward, next_state, done = action_function(state, action)
                    self.save_in_memory(state, action, reward, next_state, done)
                if len(self.memory) >= self.batch_size:
                    last_A = self.train_model(train_iterations)

                if self.epsylone > self.epsylone_min:
                    self.epsylone *= self.epsylone_decay

        else:
            m_step = 0
            for i in range(iterations):
                state = initial_function()
                done = False

                score = 0
                step = 0
                while not done:
                    action = self.choose_action(state)
                    reward, next_state, done = action_function(state, action)
                    score += reward

                    self.save_in_memory(state, action, reward, next_state, done)
                    m_step = (m_step + step) / 2
                    step += 1

                if len(self.memory) >= self.batch_size:
                    last_A = self.train_model(train_iterations)

                if self.epsylone > self.epsylone_min:
                    self.epsylone *= self.epsylone_decay

                if verbose >= 3:
                    print(
                        f"\rEpisode: {i}/{iterations} | score: {score} | epsylone: {self.epsylone} | mean step per iteration: {m_step}",
                        end="")

        if verbose >= 2:
            print(f"{color2}Trained finished !{color1}\nMETRICS:{color3}\nEpsylone = {self.epsylone}")
            if not self.ai_model_is_a_tensorflow:
                self.ai_model.print_metrics(last_A)


"""
class Manager:
    def __init__(self):
        self.map = [[1, 0, 0, -1],
                    [-1, 0, 1, 0],
                    [0, 0, 0, 0],
                    [1, -1, 0, -1]]
        self.total_reward = 0
        self.actions = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    def initial_function(self, x=1, y=1):
        self.total_reward = 0
        self.map = [[1, 1, 0, -1],
                    [0, 0, 1, 0],
                    [0, 0, 0, 0],
                    [1, -1, 0, 0]]
        state = list(np.array(self.map).flatten())
        state.append(x)
        state.append(y)
        return state

    def action_function(self, state, action):
        next_state = np.array([state[-2], state[-1]]) + self.actions[action]
        reward = np.array(self.map)[next_state[1]][next_state[0]]
        self.total_reward += reward
        self.map[next_state[1]][next_state[0]] = 0
        if reward == -1 or self.total_reward == 2:
            done = True
        else:
            done = False
        state = list(np.array(self.map).flatten())
        state.append(next_state[0])
        state.append(next_state[1])
        return reward, state, done

    def show_player_pass(self, states):
        map = np.array(self.map.tolist(), dtype=str)
        for s in states[0]:
            if states[0].index(s) == 0:
                map[tuple(s)] = "S"
            elif states[0].index(s) == len(states[0]) - 1:
                map[tuple(s)] = "E"
            else:
                map[tuple(s)] = "P"
        return map

    def show_pass(self, state, ai_model):
        done = False
        states = []
        while not done:
            action = np.argmax(ai_model.predict([state])[0])
            reward, state, done = self.action_function(state, action)
            states.append([state, reward])

        print(self.show_player_pass(states))


m = Manager()
spdql = DeepQLearning(18, 4, learning_rate=0.5, gama=0.95, epsylone=1, epsylone_decay=0.999,
                      epsylone_min=0.1, batch_size=10)
spdql.train(initial_function=m.initial_function, iterations=1000, action_function=m.action_function, train_iterations=2)

print("hey")
m.show_pass(m.initial_function(), spdql.ai_model)
"""
