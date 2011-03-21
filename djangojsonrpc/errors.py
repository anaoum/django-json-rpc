from exceptions import Exception

class JsonRpcException(Exception):
	def to_json_rpc_error(self):
		return {"code": self.code, "message": self.message}
	def __str__(self):
		return self.message
		
class JsonRpcExceptionWithData(JsonRpcException):
	def to_json_rpc_error(self):
		json = super(JsonRpcExceptionWithData, self).to_json_rpc_error()
		json["data"] = self.data
		return json
	
class InvalidRequest(JsonRpcExceptionWithData):
	code = -32600
	message = "Invalid request."
	def __init__(self, cause=None):
		if cause:
			self.data = str(cause)
		else:
			self.data = "Could not understand request."

class NoSuchMethod(JsonRpcException):
	code = -32601
	message = "Method not found."
	
class InvalidParams(JsonRpcException):
	code = -32602
	message = "Invalid method parameter(s)."
	
class InternalError(JsonRpcExceptionWithData):
	code = -32603
	message = "Internal error."
	def __init__(self, cause):
		self.data = str(cause)
		
class ParserError(JsonRpcExceptionWithData):
	code = -32700
	message = "Parser error."
	def __init__(self, cause):
		self.data = str(cause)