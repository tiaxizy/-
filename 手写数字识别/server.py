import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import numpy as np
from matplotlib import pyplot as plt
import os,base64 
import tensorflow as tf
import mnist_cnn as mnist_interence
import mnist_train as mnist_train
from tornado.options import define, options
define("port", default=11111, help="run on the given port", type=int)

class IndexHandler(tornado.websocket.WebSocketHandler):
    def get(self):
        self.render('page1.html')


class wbs(tornado.websocket.WebSocketHandler):         #websocket
    def open(self):
        print("一个新连接")
    def on_close(self):
        print("断开连接！")
    def on_message(self,message):
        m=message.split(',')
        print(len(m))
        print(type(len(m)))
        IMG=[[[0,0,0]for i in range(28)]for i in range(28)]
        for i in range(3136):
            if(i%4==0):
                IMG[i//112][i//4%28][0]=int(m[i])*int(m[i+3])//255
            if(i%4==1):
                IMG[i//112][i//4%28][1]=int(m[i])*int(m[i+2])//255
            if(i%4==2):
                IMG[i//112][i//4%28][2]=int(m[i])*int(m[i+1])//255
        print(IMG)                   
        self.write_message(str(img1(IMG)))


def img1(IMG):
    IMG=np.dot(IMG,[1/3,1/3,1/3])
    plt.figure("Image")
    plt.imshow(IMG,cmap='gray')
    plt.axis('on')
    plt.title('image')
    #plt.show()
    return evaluate(IMG)
def evaluate(IMG):
    with tf.Graph().as_default():
        x = tf.placeholder(tf.float32, shape=[None,
                                              mnist_interence.IMAGE_SIZE,
                                              mnist_interence.IMAGE_SIZE,
                                              mnist_interence.NUM_CHANNEL], name='x-input')
        reshape_xs = np.reshape(IMG, (-1, mnist_interence.IMAGE_SIZE,
                                     mnist_interence.IMAGE_SIZE,
                                     mnist_interence.NUM_CHANNEL))
        val_feed = {x: reshape_xs}
        y = mnist_interence.interence(x, False, None)
        num=tf.argmax(y, 1)
        saver = tf.train.Saver()
        with tf.Session() as sess:
            ckpt = tf.train.get_checkpoint_state(mnist_train.MODEL_PATH)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
                num2= sess.run(num, feed_dict=val_feed)
                return num2[0]
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r"/", IndexHandler),
        (r'/page1', wbs)],
         template_path=os.path.join(os.path.dirname(__file__), "1")
         )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()