import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import json
import pymongo

connection = pymongo.MongoClient()
db = connection.EducationSys
user = db.user
message = db.message

class IndexPageHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

class RegisterHandler(tornado.web.RequestHandler):
	def post(self):
		json_string = self.request.body
		json_object = json.loads(json_string);
		username = json_object['username']
		password = json_object['password']
		userNo = json_object['userNo']
		phone = json_object['phone']

		query = {}
		query['username'] = username
		print query
		find_data = user.find_one(query)
		print find_data
		status = 0
		msg = "Error"
		if(None == find_data):
			print("None == find_data")
			user.insert(json_object)
			status = 1
			msg = "Success"
			
		ret = {}
		ret['status'] = status
		ret['msg'] = msg
		ret_json = json.dumps(ret)
		
		self.write(ret_json)

	def set_default_headers(self):
		self.set_header('Content-type', 'application/json;charset=utf-8')

class LoginHandler(tornado.web.RequestHandler):
	def post(self):
		json_string = self.request.body
		json_object = json.loads(json_string);
		username = json_object['username']
		password = json_object['password']
		status = 0
		msg = "Error"
		if(None == username or None == password):
			print "None == username or None == password"
		query = {}
		query['username'] = username
		query['password'] = password
		query_result = user.find_one(query)
		print query_result
		data = {}
		if(None != query_result):
			data['username'] = query_result['username']
			data['role'] = 'role'
			data['isSuccess'] = True
			data['userNo'] = query_result['userNo']
			data['phone'] = query_result['phone']
			data['messageList'] = ""
			status = 1
			msg = "Success"
		response = {}
		response['status'] = status
		response['msg'] = msg
		response['data'] = data
		self.write(json.dumps(response))

	def set_default_headers(self):
		self.set_header('Content-type', 'application/json;charset=utf-i')

class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def check_origin(self, origin):
		return True

	def open(self):
		print "WebSocket opened"

	def on_message(self, message):
		self.write_message(u"You said: " + message)

	def on_close(self):
		print "WebSocket closed"


class Application(tornado.web.Application):
	def __init__(self):
		handlers = {
			(r'/', IndexPageHandler),
			(r'/register', RegisterHandler),
			(r'/login', LoginHandler),
			(r'/ws', WebSocketHandler)
		}

		settings = {"template_path" : "."}
		tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
	ws_app = Application()
	server = tornado.httpserver.HTTPServer(ws_app)
	server.listen(8080)
	tornado.ioloop.IOLoop.instance().start()
