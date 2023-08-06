
from abc import ABC

from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random


class ParamsEnv(Env, ABC):
    def __init__(self):
        # 所采取的动作空间维度，如 参数减小，参数不变，参数增加，
        self.action_space = Box(low=-5, high=5, shape=(12,))
        # 参数范围数组 Box允许在整个空间内有连续值
        self.observation_space = Box(low=-20, high=20, shape=(6,))
        # 参数初始值设定
        self.state = [1.00, 1.00, 0.20, 0.02, 0.50, 0.05, 0, 0]
        self.step_num = 0
        self.last_max = 0
        self.now_max = 0
        self.done = False
        self.num = 0
        self.TH1 = 0.8
        self.TH2 = 0.5
        self.TH3 = 0.15
        self.TH4 = 0.05
        self.TH5 = 0.01
        self.err = 0  # 残差
        self.err_err = 0  # 上一次残差与新的参数的残差 之间的误差
        self.patient = None
        self.params = None
        self.kws = None
        self.mul_num = 5  # 状态乘系数
        self.max_step_perEpisode = 4000  # 单个回合最大步数
        self.gamma = 0.99  # 强化学习折扣率γ
        self.lr = 0.0003  # 学习率

    def get_state(self, observation):
        state = np.array(observation).reshape(1, 6)
        state = state * self.mul_num
        return state

    # 奖励函数
    def get_reward(self):
        if abs(self.err) > self.TH1:
            r1 = 1
        elif abs(self.err) > self.TH2:
            r1 = 3
        elif abs(self.err) > self.TH3:
            r1 = 5
        elif abs(self.err) > self.TH4:
            r1 = 9
        elif abs(self.err) > self.TH5:
            r1 = 12
        else:
            r1 = 15
        # r2 = 10
        # if abs(self.err) > abs(self.real_past):
        #     if abs(self.err_err) > abs(self.real_past_past):
        #         r2 = -10
        r2 = -10
        reward = 0.0003 * r1 + 0.0002 * r2
        return reward

    # 重置环境
    def reset(self):
        self.num = 0
        self.now_max = 0
        self.last_max = 0
        self.done = False
        observation = self.patient.reset_params()  # 重置参数为初始值
        state = self.get_state(observation)
        return state

    # 主程序
    def step(self, action):
        self.step_num = self.step_num + 1
        a = random.random()  # 生成[0,1)的数
        if a <= 0.49:
            a = -1
        else:
            a = 1
        k1 = (action[0][0] + 5) + a * 0.01
        k2 = (action[0][1] + 5) + a * 0.01
        k3 = (action[0][2] + 5) + a * 0.01
        k4 = (action[0][3] + 5) + a * 0.01
        fa = (action[0][4] + 5) + a * 0.01
        vb = (action[0][5] + 5) + a * 0.01
        p = [k1, k2, k3, k4, fa, vb]
        err = self.patient.compartment_model_residual(self.patient, self.params, None, **self.kws)
        new_err = self.patient.compartment_model_residual(self.patient, p, None, **self.kws)
        err_err = new_err - err
        observation = [k1, k2, k3, k4, fa, vb, err, err_err]
        # 获取动作对应奖励
        reward = self.get_reward()
        # 获取下一状态
        state = self.get_state(observation)
        return reward, state


# if __name__ == '__main__':