import math

class Particle:
    """Class representing a generic particle
    """
    def __init__(self, mass, charge, name, momentum = 0.):   #momentum opzionale, quindi ci metto un valore di default
        self._mass = mass # in MeV
        self._charge = charge
        self._name = name
        self.momentum = momentum # in MeV, non metto privato così uso setter della property, con messaggio di errore
    
    # Voglio attributi read-only -> metto _ e properties senza setter, cosicché non si possano settare a caso

    @property
    def mass(self):
        return self._mass
    
    @property
    def charge(self):
        return self._charge
    
    @property
    def name(self):
        return self._name
    
    @property
    def momentum(self):
        return self._momentum 
    
    @momentum.setter
    def momentum(self, momentum):
        if momentum < 0:
            print('Momentum cannot be lower than zero')
            print('The momentum will be set to zero instead')
            self._momentum = 0
        else:
            self._momentum = momentum

    @property
    def energy(self):
        return math.sqrt(self.mass**2 + self.momentum**2)
    
    @energy.setter
    def energy(self, energy):
        if energy < self.mass:
            print('Cannot set the energy to a value lower of the particle mass')
        else:    
            self.momentum = math.sqrt(energy**2 - self.mass**2) # non posso settare direttamente energy perché non esiste, non è attributo ma property

    @property
    def beta(self):
        return self.momentum / self.energy
    
    @beta.setter
    def beta(self, beta):
        if (beta < 0) or (beta > 1):
            print('Values of beta lower than 0 or higher than 1 are non physical!')
        elif (beta >= 1.) and (self.mass > 0.): # non == perché non è saggio confrontare float
            print('Cannot set beta = 1 for a massive particle') 
        else:
            self.momentum = beta * self.energy 
        
    @property
    def gamma(self):
        return 1 / math.sqrt(1 - self.beta**2)
    
    @gamma.setter
    def gamma(self, gamma):
        if gamma < 1:
            print('Values of gamma lower than 1 are not physical!')
        else:
            self.momentum = math.sqrt((1 - 1/ gamma**2)) * self.energy 

    def print_info(self):
        print(f'Particle {self.name} of mass {self.mass} MeV and charge {self.charge}[e]')
        print(f'The particle momentum is {self.momentum} MeV')

class Proton(Particle):

    MASS = 938. # Mev, per convenzione in py costanti in maiuscolo
    CHARGE = +1
    NAME = 'Proton'

    def __init__(self, momentum=0.):
        Particle.__init__(self, mass=self.MASS, charge=self.CHARGE, 
                          name=self.NAME, momentum=momentum) # in alternativa Proton,MASS, Proton.CHARGE e Proton.NAME

class Alpha(Particle):

    MASS = 3727.3 
    CHARGE = +2
    NAME = 'Alpha'

    def __init__(self, momentum=0.):
        Particle.__init__(self, mass=self.MASS, charge=self.CHARGE, 
                          name=self.NAME, momentum=momentum) 

if __name__ == '__main__':
    muon = Particle(mass=105.6, charge=-1, name='Muon')
    muon.print_info()
    muon.energy = 200
    print(f'Muon energy: {muon.energy:.2f} MeV, '\
          f'momentum: {muon.momentum:.2f} MeV, '\
          f'beta: {muon.beta:.5f}')
    muon.momentum = 20
    print(f'Muon energy: {muon.energy:.2f} MeV, '\
          f'momentum: {muon.momentum:.2f} MeV, '\
          f'beta: {muon.beta:.5f}')
    proton = Proton(momentum=200.)
    proton.print_info()
    proton.beta = 0.8
    proton.print_info()
    alpha = Alpha(momentum=20.)
    alpha.energy = 10000.
    alpha.print_info()