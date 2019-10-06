import random

import math
import numpy as np


# import matplotlib.pyplot as plt

# plt.rcParams['axes.unicode_minus'] = False
# plt.rcParams['font.sans-serif'] = ['SimHei']


def forword(hidden_layer_count, hidden_layer_neurons, input_data_count, output_data_count,
            input_data, ideal_output, neurons_link):
    out_list = input_data
    store_out = [[]]
    for i in range(1, neurons_link.__len__()):
        temp_list = []
        for j in range(neurons_link[i].__len__()):
            neurons = neurons_link[i][j]
            outx = neurons.get_out(out_list)
            # print(outx)
            temp_list.append(outx)
        out_list = temp_list
        store_out.append(out_list)
        # print(out_list)
    return out_list


def backword(hidden_layer_count, hidden_layer_neurons, input_data_count, output_data_count,
             input_data, ideal_output, neurons_link, out_list, Etotal, learn_rate):
    for i in range(neurons_link.__len__() - 1, 0, -1):
        for j in range(neurons_link[i].__len__()):
            # print(str(i) + " " + str(j))
            neurons = neurons_link[i][j]
            if i == neurons_link.__len__() - 1:  # 先完成输出层更新
                for k in range(len(neurons.weights)):
                    neuron_last = neurons_link[i - 1][k]  # 取出当前修改的权值对应于上一层哪个神经元
                    neurons.backword_change(neuron_last.out, ideal_output[j], k, learn_rate)
            else:
                neurons_list = neurons_link[i + 1]
                # print(neurons_list.__len__())
                add_loss = 0
                for x in range(neurons_list.__len__()):
                    # print(neurons_list[x].weights)
                    add_loss += neurons_list[x].add_loss(j)
                # neurons.update_loss()  # 先更新误差
                neurons.add_loss_sum = add_loss
                # print("前向传导误差：" + str(add_loss))
                for k in range(len(neurons.weights)):
                    neuron_last = neurons_link[i - 1][k]  # 取出当前修改的权值对应于上一层哪个神经元
                    neurons.backword_for_hidden_layer(neuron_last.out, k, learn_rate)


def start_the_loop(hidden_layer_count, hidden_layer_neurons, input_data_count, output_data_count,
                   input_data, ideal_output, neurons_link, learn_rate, out_loss):
    step_arr, loss_arr = [], []
    for time in range(100000):
        out_list = forword(hidden_layer_count, hidden_layer_neurons, input_data_count, output_data_count,
                           input_data, ideal_output, neurons_link)
        # print(out_list)
        # 计算当前误差
        Etotal = 0
        for i in range(ideal_output.__len__()):
            Etotal += 0.5 * (ideal_output[i] - out_list[i]) ** 2
        # "当前输出：" + str(out_list) +
        if Etotal < float(out_loss):
            print("结束训练")
            return out_list, time, step_arr, loss_arr, neurons_link
        if time % 100 == 0:
            step_arr.append(time)
            loss_arr.append(Etotal)
            # print(" 计算当前误差：" + str(Etotal) + " 结束一次正向传播" + "次数" + str(time))
            # draw_fit_curve(input_data, ideal_output, out_list, step_arr, loss_arr)
        # if time % 10000 == 0:
        #     print("当前输出：" + str(out_list) + "次数" + str(time))
        backword(hidden_layer_count, hidden_layer_neurons, input_data_count, output_data_count,
                 input_data, ideal_output, neurons_link, out_list, Etotal, learn_rate)


class neurons:
    def __init__(self, bias, weights):
        self.bias = bias
        self.weights = weights
        self.net = 0
        self.out = 0
        self.transfer_loss = 0
        self.add_loss_sum = 0

    def set_weight(self, change_weight, loc):
        self.weights[loc] = change_weight

    def get_weight(self, loc):
        return self.weights[loc]

    def get_net(self, input_datas):
        sum = 0
        for i in range(self.weights.__len__()):
            sum = sum + input_datas[i] * self.weights[i]
        sum = sum + self.bias
        self.net = sum

    def sigmoid(self):
        self.out = 1 / (1 + math.exp(-self.net))

    def get_out(self, input_datas):
        self.get_net(input_datas)
        self.sigmoid()
        return self.out

    def set_out(self, out):
        self.out = out

    def backword_change(self, out_of_last_layer, target, loc, l_r):
        # print("(" + str(self.out) + "-" + str(target) + ")*" + str(self.out) + "*(1-" + str(self.out) + ")")
        temp0 = (self.out - target) * self.out * (1 - self.out)
        # print("temp0 " + str(temp0))
        # print(out_of_last_layer)
        temp = temp0 * out_of_last_layer
        # print("temp：", str(temp))
        self.weights[loc] = self.weights[loc] - l_r * temp
        # print("更新前的偏移" + str(self.bias))
        if loc == 0:
            self.bias = self.bias - l_r * temp0
            self.transfer_loss = temp0
        # print("更新后的权值" + str(self.weights[loc]))
        # print("更新后的偏移" + str(self.bias))

    def backword_for_hidden_layer(self, out_of_last_layer, loc, l_r):
        temp0 = self.add_loss_sum * self.out * (1 - self.out)
        temp = temp0 * out_of_last_layer
        self.weights[loc] = self.weights[loc] - l_r * temp
        if loc == 0:
            self.bias = self.bias - l_r * temp0
            self.transfer_loss = temp0
        # print("更新后的权值" + str(self.weights[loc]))
        # print("更新后的偏移" + str(self.bias))

    def add_loss(self, j):
        # print(j)
        # print(self.weights[j] * self.transfer_loss)
        return self.weights[j] * self.transfer_loss


# def draw_fit_curve(origin_xs, origin_ys, prediction_ys, step_arr, loss_arr):
#     plt.cla()
#     fig = plt.figure("BP")
#     ax1 = fig.add_subplot(121)
#     ax1.plot(origin_xs, origin_ys, color='m', linestyle='', marker='.', label='原数据')
#     ax1.plot(origin_xs, prediction_ys, color='#009688', label='拟合曲线')
#     plt.title(label='BP神经网络拟合非线性曲线')
#     ax2 = fig.add_subplot(122)
#     ax2.plot(step_arr, loss_arr, color='red', label='误差曲线')
#     plt.title(label='BP神经网络误差下降曲线')
#     plt.legend()
#     plt.pause(0.001)


def start_to_calculate(h_l_c, h_l_n, i_d_c, o_d_c, l_r, function, out_loss):
    hidden_layer_count = int(h_l_c)  # 隐藏层数
    hidden_layer_neurons = int(h_l_n)  # 隐藏内神经元个数
    input_data_count = i_d_c
    output_data_count = o_d_c
    learn_rate = float(l_r)
    # weight_for_hidden_layer = [[0.15, 0.20], [0.25, 0.30], [0.35, 0.40], [0.40, 0.45, 0.50], [0.55, 0.60, 0.65],
    #                            [0.50, 0.40, 0.30]]
    # weight_for_output_layer = [[0.40, 0.45, 0.50], [0.60, 0.55, 0.40]]
    X = np.arange(0, 10, 0.1)  # 输入层矩阵
    # Y = 5 * np.cos(X) + 5  # 输出层矩阵  # 输出层矩阵
    test_input_data = np.arange(0.1, 10.1, 0.1)

    if function == "y=5 * x + 25":
        Y = 5 * X + 25
        test_ideal_output = 5 * test_input_data + 25
    elif function == "y=5 * sinx + 5":
        Y = 5 * np.sin(X) + 5
        test_ideal_output = 5 * np.sin(test_input_data) + 5
    elif function == "y=5 * cosx + 5":
        Y = 5 * np.cos(X) + 5  # 输出层矩阵
        test_ideal_output = 5 * np.cos(test_input_data) + 5
    elif function == "y=x^2":
        Y = []
        test_ideal_output = []
        for i in range(len(X)):
            Y.append(X[i] * X[i])
            test_ideal_output.append(test_input_data[i] * test_input_data[i])
    else:
        return None
    # print(Y)

    input_data = X
    ideal_output = Y

    max_input_data = max(input_data)
    # print(max_input_data)
    max_ideal_output = max(ideal_output)
    # print(max_ideal_output)
    max_test_input_data = max(test_input_data)
    # print(max_test_input_data)
    max_test_ideal_output = max(test_ideal_output)
    # print(max_test_ideal_output)
    for i in range(input_data_count):
        input_data[i] = input_data[i] / max_input_data
        test_input_data[i] = test_input_data[i] / max_test_input_data
    for i in range(output_data_count):
        ideal_output[i] = ideal_output[i] / max_ideal_output
        test_ideal_output[i] = test_ideal_output[i] / max_test_ideal_output

    # print(input_data)
    # print(ideal_output)
    # print(test_input_data)
    # print(test_ideal_output)
    # print(X.__len__())
    # for xx in range(X.__len__()):
    #     input_data.append(X[xx])
    #     y = 5 * math.sin(X[xx])
    #     ideal_output.append(y)
    # input_data = [0.05, 0.1]
    # ideal_output = [0.01, 0.99]
    print(input_data.__len__())
    print(ideal_output.__len__())
    # bias = [0.35, 0.60, 0.50]
    # neurons_link = [[], [], [], []]
    neurons_link = []
    for i in range(hidden_layer_count + 2):
        neurons_link.append([])

    # print(neurons_link)
    # for i in range(hidden_layer_count):
    #     for j in range(hidden_layer_neurons):
    #         # if i == 0:
    #         #     temp=[]
    #         #     temp.append()
    for count in range(input_data_count):
        start_neuron = neurons(0, [])
        start_neuron.set_out(input_data[count])
        neurons_link[0].append(start_neuron)

    # start_neuron1 = neurons(0, [])
    # start_neuron1.set_out(0.05)
    # start_neuron2 = neurons(0, [])
    # start_neuron2.set_out(0.1)
    # neurons_link[0].append(start_neuron1)
    # neurons_link[0].append(start_neuron2)
    # neurons_link[0].append(neurons(0, []).set_out(0.05))
    # neurons_link[0].append(neurons(0, []).set_out(0.1))

    # print(neurons_link[0][0].out)
    for i in range(hidden_layer_neurons):
        weight_for_the_first_hidden_layer = []
        for count in range(input_data_count):
            weight_for_the_first_hidden_layer.append(random.random())
        print(str(weight_for_the_first_hidden_layer) + " 第 " + str(i) + "个隐藏层神经元")
        neurons_link[1].append(neurons(0.35, weight_for_the_first_hidden_layer))
    for x in range(0, hidden_layer_count - 1):
        for i in range(hidden_layer_neurons):
            weight_for_hidden_layer = []
            for count in range(hidden_layer_neurons):
                weight_for_hidden_layer.append(random.random())
            print(str(weight_for_hidden_layer) + " 第 " + str(i) + "个隐藏层神经元")
            neurons_link[x + 2].append(neurons(0.60, weight_for_hidden_layer))

    # neurons_link[1].append(neurons(0.35, weight_for_the_first_hidden_layer))
    # neurons_link[1].append(neurons(0.35, weight_for_the_first_hidden_layer))
    # neurons_link[1].append(neurons(0.35, weight_for_the_first_hidden_layer))
    # neurons_link[2].append(neurons(0.60, [0.40, 0.45, 0.50]))
    # neurons_link[2].append(neurons(0.60, [0.55, 0.60, 0.65]))
    # neurons_link[2].append(neurons(0.60, [0.50, 0.40, 0.30]))
    # neurons_link[3].append(neurons(0.50, [0.60, 0.55, 0.40]))

    for i in range(output_data_count):
        weight_for_hidden_layer = []
        for count in range(hidden_layer_neurons):
            weight_for_hidden_layer.append(random.random())
        print(str(weight_for_hidden_layer) + " 第 " + str(i) + "个输出神经元")

        neurons_link[hidden_layer_count + 1].append(neurons(0.50, weight_for_hidden_layer))
        print(i)

    out_list, time, step_arr, loss_arr, neurons_link1 = start_the_loop(hidden_layer_count, hidden_layer_neurons,
                                                                       input_data_count,
                                                                       output_data_count,
                                                                       input_data, ideal_output, neurons_link,
                                                                       learn_rate, out_loss)
    print(111111111111111111)
    for count in range(input_data_count):
        neurons_link1[0][count].set_out(test_input_data[count])
        print(test_input_data[count])
    forword_out_list_test = forword(hidden_layer_count, hidden_layer_neurons, input_data_count, output_data_count,
                                    test_input_data, test_ideal_output, neurons_link1)
    # 计算当前误差
    Etotal1 = 0
    for i in range(test_ideal_output.__len__()):
        Etotal1 += 0.5 * (test_ideal_output[i] - forword_out_list_test[i]) ** 2
    # print(ideal_output)
    input = []
    X = np.arange(-5, 5, 0.1)  # 输入层矩阵
    idel = []
    idel1 = []
    input = input_data.tolist()
    test_input = test_input_data.tolist()
    for i in range(X.__len__()):
        input[i] = round(input[i] * max_input_data, 2)
        test_input[i] = round(test_input[i] * max_test_input_data, 2)
    for i in range(output_data_count):
        out_list[i] = round(out_list[i] * max_ideal_output, 2)
        forword_out_list_test[i] = round(forword_out_list_test[i] * max_test_ideal_output, 2)
        ideal_output[i] = round(ideal_output[i] * max_ideal_output, 2)
        test_ideal_output[i] = round(test_ideal_output[i] * max_test_ideal_output, 2)
        idel.append(ideal_output[i])
        idel1.append(test_ideal_output[i])
    return input, out_list, idel, time, step_arr, loss_arr, test_input, idel1, forword_out_list_test

# start_to_calculate(2, 7, 100, 100, 0.15)

# 0.03 0.64128539159
# 0.10
