import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import datetime
from tornado.options import define, options

define("port", default=11111, help="run on the given port", type=int)

roomdict = {"聊天室1": {}, "聊天室2": {},"聊天室3": {}}

class IndexHandler(tornado.web.RequestHandler):                   #登录界面
    def get(self):
        self.render('index.html', roomlist=roomdict.keys())

class Page1Handler(tornado.websocket.WebSocketHandler):                #加载聊天页面
    def post(self):
        room = self.get_argument("select1")
        name = self.get_argument("name")
        if(room == "-1"):
            room=name+"的聊天室"
            roomdict[room]={}
            print(roomdict)
        self.render('page1.html',roomdict=roomdict,room=room,name=name)

class wbs(tornado.websocket.WebSocketHandler):         #websocket实现聊天通讯
    def open(self):
        name=self.get_query_argument('name')
        room=self.get_query_argument('room')
        roomdict[room][self]=name
        for i in roomdict[room].keys():
            i.write_message(name+' connected!233\r\n')
    def on_close(self):
        name=self.get_query_argument('name')
        room=self.get_query_argument('room')
        roomdict[room].pop(self)
        for i in roomdict[room].keys():
            i.write_message(name+"离开聊天室qaq"+"\r\n")
    def on_message(self, message):
        room=self.get_query_argument('room')
        for i in roomdict[room].keys():
            i.write_message(message+"\r\n")


if __name__ == "__main__":
    tornado.options.parse_command_line()

    app = tornado.web.Application(
        handlers=[(r"/", IndexHandler),
                  (r'/action1', Page1Handler),
                  (r'/action2', wbs)],
        template_path=os.path.join(os.path.dirname(__file__), "1")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
