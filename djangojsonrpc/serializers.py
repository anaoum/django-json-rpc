from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.db.models import Model

class DefaultJSONEncoder(DjangoJSONEncoder):
	
	def default(self, o):
		
		if isinstance(o, Model):
			return serialize("python", [o])[0]
			
		if hasattr(o, "to_json") and callable(getattr(o, "to_json")):
			return o.to_json()
			
		try:
			return list(iter(o))
		except TypeError:
			pass
			
		return super(DefaultJSONEncoder, self).default(o)
