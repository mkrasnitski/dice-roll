from dataclasses import dataclass

@dataclass
class SpecialZero:
	name: str

	def __add__(self, other):
		return other + int(self)

	def __radd__(self, other):
		return self.__add__(other)

	def __eq__(self, other):
		return other == int(self)

	def __int__(self):
		return 0