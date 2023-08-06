import itertools
import numpy as np

from pybendt.interaction import Interaction, kB_in_kcal_per_mole_per_kelvin
from pybendt.reaction import Reaction

class Atom():
	id_iter = itertools.count()
	def __init__(self, position, friction, label = "", dimensions = 3, color = 'red'):
		self.id = next(Atom.id_iter)+1
		self.label = label
		self.position = np.array(position)
		self.dimensions = dimensions
		self.color = color
		assert len(self.position) == dimensions, 'Number of dimensions is set to {}, but you provided {}-component position vector'.format(dimensions, len(position))
		self.interactions = []
		self.reactions = []
		self.force = np.zeros(dimensions)
		self.mobility = 1/friction
	def __str__(self):
		position_string = self.dimensions*'{} '
		position_string = position_string[:-1]
		return ('{}#{} '+position_string).format(self.label, self.id, *self.position)
	def __repr__(self):
		return self.__str__()
	def add_interaction(self, atom2, force_function, energy_function, parameters):
		interaction = Interaction(self, atom2, force_function, energy_function, parameters)
		self.interactions.append(interaction)
		atom2.interactions.append(interaction)
		return interaction
	def add_existing_interaction(self, atom2, interaction):
		assert (interaction.atom1 is None) and (interaction.atom2 is None), 'The interaction {} already has atoms'.format(interaction)
		interaction.atom1 = self
		interaction.atom2 = atom2
		self.interactions.append(interaction)
		atom2.interactions.append(interaction)
	def add_existing_reaction(self, reaction):
		assert np.all([atom is None for atom in reaction.atoms]), 'The reaction {} already has atoms'.format(interaction)
		atoms = []
		for condition in conditions:
			atoms += [ atom for atom in condition.atoms if atom not in atoms ]
		for atom in atoms:
			atom.reactions.append(reaction)
		return reaction
	def add_reaction(self, conditions, effect_functions, effect_parameters):
		atoms = []
		for condition in conditions:
			atoms += [ atom for atom in condition.atoms if atom not in atoms ]
		reaction = Reaction([self] + atoms, conditions, effect_functions, effect_parameters)
		for atom in atoms:
			atom.reactions.append(reaction)
	def move(self, vector):
		self.position += vector
	def deterministic_move(self, timestep):
		self.move(self.mobility * self.force * timestep)
	def brownian_move(self, timestep, temperature, random_vector):
		self.move(np.sqrt(2*kB_in_kcal_per_mole_per_kelvin*temperature*self.mobility*timestep) * random_vector)
	def remove_interactions_by_id(self, ids):
		for i in self.interactions:
			if i.id in ids: i.remove()
	def remove_reactions_by_id(self, ids):
		for r in self.reactions:
			if r.id in ids: r.remove()
	def reset_force(self):
		self.force = np.zeros(self.dimensions)

def friction_from_hydrodynamic_radius_and_viscosity(hydradius, viscosity):
	return 6 * np.pi * viscosity * hydradius * 6.02 / 41.84