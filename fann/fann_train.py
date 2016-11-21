#! /usr/bin/python
from fann2 import libfann
import sys

connection_rate = 1
learning_rate = 0.7
num_input = 3
num_hidden = 4
num_output = 2

desired_error = 0.00026
max_interations = 100000
iterations_between_reports = 1000

ann = libfann.neural_net()
ann.create_sparse_array(connection_rate, (num_input,num_hidden,num_output))
ann.set_learning_rate(learning_rate)
ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)

ann.train_on_file(sys.argv[1], max_iterations, iterations_between_reports, desired_error)

ann.save(sys.argv[2])
