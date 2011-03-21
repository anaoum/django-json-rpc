from errors import InvalidParams
from utils import validate_arguments

def publicmethod(method):
	return PublicMethod(method)

class PublicMethod(object):
	def __init__(self, method):
		self.method = method
	def __call__(self, *args, **kwargs):
		if not validate_arguments(self.method, args, kwargs):
			raise InvalidParams
		return self.method(*args, **kwargs)