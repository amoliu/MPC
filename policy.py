import tensorflow as tf
import numpy as np

# Predefined function to build a feedforward neural network
def build_mlp(input_placeholder,
              output_size,
              scope,
              n_layers=2,
              size=64,
              activation=tf.tanh,
              output_activation=None
              ):
    out = input_placeholder
    with tf.variable_scope(scope):
        for _ in range(n_layers):
            out = tf.layers.dense(out, size, activation=activation)
        out = tf.layers.dense(out, output_size, activation=output_activation)
    return out

class NNPolicy():
    def __init__(self,
                 env,
                 n_layers,
                 size,
                 activation,
                 output_activation,
                 normalization,
                 batch_size,
                 iterations,
                 learning_rate,
                 sess
                 ):
        """ YOUR CODE HERE """
        """ Note: Be careful about normalization """

        self.normalization = normalization
        self.batch_size = batch_size
        self.iterations = iterations

        self.states = tf.placeholder(shape = [None, env.observation_space.shape[0]], dtype = tf.float32)
        self.actions = tf.placeholder(shape = [None, env.action_space.shape[0]], dtype = tf.float32)

        self.mean = build_mlp(self.states, env.action_space.shape[0], "policy", n_layers, size, activation, output_activation)

        self.loss = tf.reduce_mean(tf.square((self.actions) - self.mean))
        self.update_op = tf.train.AdamOptimizer(learning_rate).minimize(self.loss)

    def fit(self, data):
        """
        Write a function to take in a dataset of (unnormalized)states, (unnormalized)actions and imitate the actions taken by an expert.
        """

        """YOUR CODE HERE """
        observations = np.concatenate([path['observations'] for path in data])
        actions = np.concatenate([path['actions'] for path in data])

        "Normalize the data"
        observations = (observations - self.normalization[0]) / (self.normalization[1] + 1e-10)
        actions = (actions - self.normalization[4]) / (self.normalization[5] + 1e-10)

        for i in range(self.iterations):

            batch_id = np.random.choice(observations.shape[0], self.batch_size)#, replace = False)
            _ = tf.get_default_session().run(self.update_op, feed_dict = {self.states : observations[batch_id], self.actions : actions[batch_id]})


    def get_action(self, states):
        """ Write a function to take in a batch of (unnormalized) states and return the (unnormalized) actions as predicted by using the model """
        """ YOUR CODE HERE """

        mean = tf.get_default_session().run(self.model, feed_dict = {self.states : states})
        std = np.ones(mean.shape[0])

        return tf.contrib.distributions.MultivariateNormalDiag(mean, std)
