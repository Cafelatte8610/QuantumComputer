# ===========import===========
import tensorflow as tf
import os
from tensorflow.examples.tutorials.mnist import input_data
# GPUの無効化
os.environ['CUDA_VISIBLE_DEVICES'] = ""

def main():
	# ===========init===========
	image_size = 28*28
	output_num = 10
	learning_rate = 0.001
	loop_num = 30000
	batch_size = 100

	mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

	# ===========model===========
	with tf.device("/cpu:0"):
		x = tf.placeholder(tf.float32, [None, image_size])
		W = tf.Variable(tf.zeros([image_size, output_num]))
		b = tf.Variable(tf.zeros([output_num]))
		y = tf.nn.softmax(tf.matmul(x, W) + b)
		y_ = tf.placeholder(tf.float32, [None, output_num])

		cross_entropy = -tf.reduce_sum(y_ * tf.log(y))
		train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)
		correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
		accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

		init = tf.global_variables_initializer()
		sess = tf.InteractiveSession()
		sess.run(init)

		# ===========training===========
		for i in range(loop_num):
			batch_xs, batch_ys = mnist.train.next_batch(batch_size)
			sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

			if i % 1 == 0:
				print("step", i, "train_accuracy:", sess.run(accuracy, feed_dict={x: batch_xs, y_: batch_ys}))

		# ===========test===========
		print("test_accuracy:", sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))


if __name__ == "__main__":
	main()