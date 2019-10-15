import tensorflow as tf
import numpy as np
import tensorflow_probability as tfp
import collections
from data_generator import *
from model import *

MAX_CONTEXT_POINTS = 50 #@param {type:"number"}
random_kernel_parameters=True #@param {type:"boolean"}

# Train dataset
dataset_train = GPCurvesReader(
    batch_size=16, max_num_context=MAX_CONTEXT_POINTS, random_kernel_parameters=random_kernel_parameters)
data_train = dataset_train.generate_curves()

# Test dataset
dataset_test = GPCurvesReader(
    batch_size=1, max_num_context=MAX_CONTEXT_POINTS, testing=True, random_kernel_parameters=random_kernel_parameters)
data_test = dataset_test.generate_curves()


###MODEL####
HIDDEN_SIZE = 128 #@param {type:"number"}
latent_encoder_output_sizes = HIDDEN_SIZE*4
num_latents = HIDDEN_SIZE
deterministic_encoder_output_sizes= HIDDEN_SIZE*4
decoder_output_sizes = HIDDEN_SIZE*2 + 2
use_deterministic_encoder = True

model = NPModel(latent_encoder_output_sizes, 
	        num_latents,               
		decoder_output_sizes, 
		deterministic_encoder_output_sizes,
		use_deterministic_encoder)

optimizer = tf.keras.optimizers.Adam(1e-4)

## Define the loss
_, _, log_prob, _, loss = model(data_train.query, data_train.num_total_points,data_train.target_y)

# Get the predicted mean and variance at the target points for the testing set
mu, sigma, _, _, _ = model(data_test.query, data_test.num_total_points)

'''

for epoch in range(3):
     print('Start of epoch %d' % (epoch,))
     # Define the loss
     with tf.GradientTape() as tape:



     grads = tape.gradient(loss, model.trainable_weights)
     optimizer.apply_gradients(zip(grads, model.trainable_weights))

'''


#train_step = optimizer.minimize(loss)


#print('mean : ', mu)
#print('sigma : ', sigma)

print('Done')                                    
        
