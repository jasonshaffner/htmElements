class query:
	def __init__(self, elementName, *elements):
		self.elementName = elementName
		if elements and not isinstance(elements, type(self)) and not isinstance(elements[0], type(self)):
			self.elements = [e for element in elements for e in element]
		else: self.elements = elements

	def __call__(self):
		return self.construct()

	def addElement(self, element):
		self.elements.append(element)

	def construct(self, indent=0):
		query = 'query ' + self.elementName
		if not self.elements: return query + "\n"
		if isinstance(self.elements, type(self)):
			query += " {\n\t" + self.elements.construct(indent + 1)
		else:
			for element in self.elements:
				query += " {\n\t" + element.construct(indent + 1)
		query += "\n}"
		return query


class queryElement(query):
	def __init__(self, elementName, *elements, **kwargs):
		self.elementName = elementName
		if elements and not isinstance(elements, type(self)) and not isinstance(elements[0], type(self)):
			self.elements = [e for element in elements for e in element]
		else: self.elements = elements
		self.condition = kwargs.get('condition', None)

	def __call__(self, indent=0):
		return self.construct(indent)

	def construct(self, indent=0):
		query = self.elementName
		if self.condition: query += " " + self.condition()
		if not self.elements: return query + "\n"
		if isinstance(self.elements, type(self)):
			query += " {\n" + ((indent + 1) * '\t') + self.elements.construct(indent + 1)
		else:
			query += " {\n"
			for element in self.elements:
				query += ((indent + 1) * '\t') + element.construct(indent + 1)
		query += '\n' + (indent * '\t') + '}\n'
		return query


class nodes(queryElement):
	def __init__(self, *elements):
		super().__init__('nodes', elements)


class condition(queryElement):
	def __init__(self, field, condition):
		self.field = field
		self.condition = condition

	def construct(self, *args):
		if isinstance(self.condition, int): return '(condition: { ' + self.field + ': ' + str(self.condition) + ' })'
		return '(condition: { ' + self.field + ': "' + self.condition + '" })'