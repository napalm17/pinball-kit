from ball import Ball, Electron, Proton, Neutron

class Level:
    """
    Implements a pinball level.
    Each level represents an element from the periodic table with ascending atomic number.
    """
    def __init__(self, atomic_number):
        self.atomic_number = atomic_number

        self.electrons = [Electron() for i in range(self.atomic_number)]
        self.protons = [Proton() for i in range(self.atomic_number)]
        self.neutrons = [Neutron() for i in range(self.atomic_number)]

        self.particles = [self.electrons, self.protons, self.neutrons]
        self.build_atom()

    def build_atom(self):
        if self.atomic_number == 1: # Hydrogen
            self.protons[0].position.xy = 300, 200
            self.neutrons[0].position.xy = 300, 220
            self.electrons[0].position.xy = 500, 210
            self.electrons[0].velocity.xy = 0, 5