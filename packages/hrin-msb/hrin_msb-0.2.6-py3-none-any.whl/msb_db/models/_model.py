from django.core.serializers import serialize
from django.db import models as Models

from msb_cipher import Cipher
from ._model_manager import MsbModelManager
from .._constants import (COLUMN_NAME_DELETED, COLUMN_NAME_DELETED_BY)


class MsbModel(Models.Model):
	_private_fields: list = []
	_list_field_names: list = []
	_identifier_field: str = ""

	class Meta:
		abstract = True

	@property
	def secure_fields(self):
		return [self._meta.pk.attname, *self._private_fields]

	@property
	def identifier_field_name(self):
		if isinstance(self._identifier_field, str) and len(self._identifier_field) > 0:
			return self._identifier_field
		return None

	def _get_field_value(self, field_name: str, encrypt: bool = False):
		if hasattr(self, field_name):
			field_value = getattr(self, field_name)
			return Cipher.encrypt(field_value) if (field_name in self.secure_fields or encrypt) else field_value
		return None

	@property
	def related_fields(self):
		fields = []
		for field in self._meta.fields:
			if field.get_internal_type() in ['ForeignKey']:
				fields.append(field.name)
		return fields

	@property
	def pk_name(self):
		return self._meta.pk.attname

	@property
	def pk_value(self):
		return getattr(self, self.pk_name) if self.pk_name is not None else ""

	@property
	def identifier(self):
		return f"{getattr(self, self.identifier_field_name)}" if hasattr(self, self.identifier_field_name) else ""

	@property
	def list_field_names(self) -> list:
		_list_field_names = [self.pk_name]
		if isinstance(self._list_field_names, list) and len(self._list_field_names) > 0:
			_list_field_names.extend(self._list_field_names)
		return _list_field_names

	def dict(self, encrypted=True):
		try:
			return {
				k: v if (k not in self.secure_fields or not encrypted) else Cipher.encrypt(v)
				for k, v in super().__dict__.items()
				if not k.startswith('__') and not k.startswith('_') and not callable(k)
			}

		except Exception:
			return dict()

	@property
	def list_fields(self):
		return {field_name: self._get_field_value(field_name) for field_name in self.list_field_names}


	@property
	def serialized(self):
		return serialize('python', [self])

	def delete(self, deleted_by=None, using=None, keep_parents=False):
		if hasattr(self, COLUMN_NAME_DELETED):
			setattr(self, COLUMN_NAME_DELETED, True)

		if hasattr(self, COLUMN_NAME_DELETED_BY):
			setattr(self, COLUMN_NAME_DELETED_BY, deleted_by)
		self.save()
		return True

	def __str__(self):
		return f"<{self.__class__.__name__} [{self.pk_value}]: {self.identifier}>"

	def __unicode__(self):
		return self.__str__()

	def __repr__(self):
		return self.__str__()

	@property
	def rows(self):
		return self.objects

	objects = MsbModelManager()
