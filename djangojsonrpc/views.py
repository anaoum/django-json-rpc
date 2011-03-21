from errors import *
from . import VERSION
from decorators import PublicMethod
from serializers import DefaultJSONEncoder

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import classonlymethod
from django.utils import simplejson
from django.http import HttpResponse
from django.views.generic import View	
		
class JsonRpcView(View):

	classes = None
	initkwargs = None

	def __init__(self, classes, initkwargs=None):
		if not isinstance(classes, list):
			classes = [classes]
		self.classes = classes
		if not initkwargs:
			initkwargs = [{} for _ in xrange(len(classes))]
		self.initkwargs = initkwargs
		
	@classonlymethod
	def as_view(cls, **initkwargs):
		view = super(JsonRpcView, cls).as_view(**initkwargs)
		view = csrf_exempt(view)
		return view
			
	def get_public_method(self, method_name):
		for clazz, kwargs in zip(self.classes, self.initkwargs):
			if not method_name.startswith(clazz.namespace):
				continue
			try:
				local_method_name = method_name[len(clazz.namespace):]
				if local_method_name.startswith("."):
					local_method_name = local_method_name.lstrip(".")
				method = getattr(clazz, local_method_name)
				if isinstance(method, PublicMethod):
					if kwargs == None:
						kwargs = {}
					instance = clazz(**kwargs)
					return (method, instance)
			except AttributeError:
				pass
		return (None, None)

	def __dispatch(self, method_name, params):
		
		method, instance = self.get_public_method(method_name)
		if not method:
			raise NoSuchMethod
		
		args = [instance]
		kwargs = {}
		
		if isinstance(params, list):
			args += params
		elif isinstance(params, dict):
			# The following allows for unicode keys in params
			for key in params.keys():
				kwargs[str(key)] = params[key]
		
		return method(*args, **kwargs)
	
	def __handle(self, request_dict):

		request_id = None
		
		try:
			request_id = request_dict.get("id", None)
			request_method = request_dict.get("method")
			request_params = request_dict.get("params", [])
		except Exception as e:
			return simplejson.dumps({"jsonrpc": VERSION, "id": request_id, "error": InvalidRequest(e).to_json_rpc_error()})
		
		response = {"jsonrpc": VERSION, "id": request_id}

		try:
			response["result"] = self.__dispatch(request_method, request_params)				
		except JsonRpcException as jre:
			response["error"] = jre.to_json_rpc_error()
		except Exception as e:
			response["error"] = InternalError(e).to_json_rpc_error()
		
		if not request_id: # Notification
			return None
			
		try:
			json = simplejson.dumps(response, cls=DefaultJSONEncoder)
		except Exception as e:
			del response["result"]
			response["error"] = ParserError(e).to_json_rpc_error()
			json = simplejson.dumps(response)
			
		return json

	def post(self, http_request):
		
		request = simplejson.loads(http_request.raw_post_data)

		if isinstance(request, dict):
			response = self.__handle(request)
		elif isinstance(request, list): # Batch
			response_items = []
			for r in request:
				result = self.__handle(r)
				if result:
					response_items.append(result)
			response = "[%s]" % ", ".join(response_items)
		else:
			response = simplejson.dumps({"jsonrpc": VERSION, "id": None, "error": InvalidRequest().to_json_rpc_error()})
		
		return HttpResponse(response) # OK
