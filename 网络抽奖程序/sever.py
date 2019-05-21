import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import numpy as np

from tornado.options import define, options
define("port", default=11111, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

def f1(l1,l2):
        n=np.random.randint(len(l1))
        l2.append(l1[n])
        l1.pop(n)
class Page1Handler(tornado.web.RequestHandler):
    def post(self):
        n1 = int(self.get_argument('N1'))
        n2 = int(self.get_argument('N2'))
        n3 = int(self.get_argument('N3'))
        md = self.get_argument('md')
        list0=md.split()
        list1=list()
        list2=list()
        list3=list()
        for i in range(n1):
            f1(list0,list1)
        for i in range(n2):
            f1(list0,list2)
        for i in range(n3):
            f1(list0,list3)
        self.render('page1.html',num1=list1,num2=list2,num3=list3, list=md)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r"/", IndexHandler),
         (r'/page1', Page1Handler)],
         template_path=os.path.join(os.path.dirname(__file__), "1")
         )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()