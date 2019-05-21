import numpy as np
import time
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import mnist_cnn as mnist_interence
import mnist_train as mnist_train
EVAL_INTERVAL_SECS = 10
BATCH_SIZE = 100


def evaluate(mnist):
    with tf.Graph().as_default():
        x = tf.placeholder(tf.float32, shape=[None,
                                              mnist_interence.IMAGE_SIZE,
                                              mnist_interence.IMAGE_SIZE,
                                              mnist_interence.NUM_CHANNEL], name='x-input')
        y_ = tf.placeholder(tf.float32, shape=[
                            None, mnist_interence.OUTPUT_NODE], name='y-input')

        xs, ys = mnist.test.images, mnist.test.labels
        reshape_xs = np.reshape(xs, (-1, mnist_interence.IMAGE_SIZE,
                                     mnist_interence.IMAGE_SIZE,
                                     mnist_interence.NUM_CHANNEL))
        print(mnist.test.labels[0])
        val_feed = {x: reshape_xs, y_: mnist.test.labels}
        y = mnist_interence.interence(x, False, None)


        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


        
        variable_average = tf.train.ExponentialMovingAverage(
            mnist_train.MOVING_AVERAGE_DECAY)

        val_to_restore = variable_average.variables_to_restore()

        saver = tf.train.Saver(val_to_restore)

        with tf.Session() as sess:
            ckpt = tf.train.get_checkpoint_state(mnist_train.MODEL_PATH)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
                global_step = ckpt.model_checkpoint_path.split(
                    '/')[-1].split('-')[-1]
                accuracy_score = sess.run(accuracy, feed_dict=val_feed)
                print('After %s train ,the accuracy is %g' %
                      (global_step, accuracy_score))
            else:
                print('No Checkpoint file find')


def main():
    mnist = input_data.read_data_sets('./mni_data', one_hot=True)
    evaluate(mnist)


if __name__ == '__main__':
    main()
