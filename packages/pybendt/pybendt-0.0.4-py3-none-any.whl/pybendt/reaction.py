import itertools

class Reaction():
	id_iter = itertools.count()
	def __init__(self, atoms, reaction_conditions, effect_functions, effect_parameters, self_remove = True):
		self.id = next(Reaction.id_iter)+1
		self.atoms = atoms
		self.reaction_conditions = reaction_conditions
		self.effect_functions = effect_functions
		self.effect_parameters = effect_parameters
		self.self_remove = self_remove
	def conditions_fulfilled(self):
		return all([ rc.condition_fulfilled for rc in self.reaction_conditions ])
	def effect(self):
		for i in range(len(self.effect_functions)):
			self.effect_functions[i](**self.effect_parameters[i])
		if self.self_remove: remove_reaction_effect(self)
	def remove(self):
		for atom in self.atoms:
			atom.reactions = [ r for r in atom.reactions if r.id != self.id ]
		self.atoms = None
	def __str__(self):
		return '{}'.format(self.id)
		# atoms_string = ('{}-'*len(self.atoms)).format(*[a.id for a in self.atoms])[:-1]
		# return '#{} {} | conditions: {}, effects: {}'.format(self.id, atoms_string, self.condition_function.__name__, self.effect_function.__name__)
	def __repr__(self):
		return self.__str__()

class ReactionCondition():
	def __init__(self, atoms, condition_function, condition_parameters):
		self.atoms = atoms
		self.condition_function = condition_function
		self.condition_parameters = condition_parameters
		self.condition_fulfilled = False
	def evaluate_condition(self, condition_variable):
		self.condition_fulfilled = self.condition_function(condition_variable, **self.condition_parameters)
	def __str__(self):
		return '{} {}'.format(self.condition_function.__name__, self.condition_parameters)
	def __repr__(self):
		return self.__str__()

def distance_condition(distance, sign, reaction_distance):
	if sign == ">":
		return distance > reaction_distance
	elif sign == "<":
		return distance < reaction_distance
	elif sign == ">=":
		return distance >= reaction_distance
	elif sign == "<=":
		return distance <= reaction_distance
	else:
		1/0

def add_interaction_effect(atom1, atom2, interaction):
	print("interaction added")
	atom1.add_existing_interaction(atom2, interaction)

def remove_interaction_effect(interaction):
	print("interaction removed")
	interaction.remove()

def add_reaction_effect(atoms, reaction):
	print("reaction added")
	atoms[0].add_existing_reaction(atoms[1:], reaction)

def remove_reaction_effect(reaction):
	print("reaction removed")
	reaction.remove()

def end_simulation_effect():
	1/0