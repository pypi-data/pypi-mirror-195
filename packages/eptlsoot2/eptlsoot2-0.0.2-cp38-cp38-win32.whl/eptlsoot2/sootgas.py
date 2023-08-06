import numpy as np
from ._eptlsoot2 import CSootGas

class SootGas(CSootGas):
    def __init__(self):
       super().__init__();

    @property
    def molecular_weights(self):
        return self.MWs;

    @molecular_weights.setter
    def molecular_weights(self, MWs):
        if type(MWs) == np.ndarray:
            self.set_MWs(MWs.tolist());
        elif type(MWs) == list:
            if all(isinstance(MW, int) or isinstance(MW, float) for MW in MWs):
                self.set_MWs(MWs);
            else:
                raise TypeError("Wrong type! Molecular weight must be a list of float/int")
        else:
            raise TypeError("Wrong type! Molecular weight must be a list or array")
        
    @property
    def TPX(self):
        return self._T, self._P, self._X;

    @TPX.setter
    def TPX(self, TPX):
        # Temperature
        if type(TPX[0]) == float:
           T = TPX[0];
        else:
            raise TypeError("Wrong type! T must be a float");
        # Pressure
        if type(TPX[1]) == float:
           P = TPX[1];
        else:
            raise TypeError("Wrong type! P must be a float") 

        if type(TPX[2]) == np.ndarray:
            X = TPX[2].tolist();
        elif type(TPX[2]) == list:
            if all(isinstance(x, float) for x in TPX[2]):
                X = TPX[2];
            else:
                raise TypeError("Wrong type! Mole fractions must be a list of floats")
        else:
            raise TypeError("Wrong type! Mole fractions must be a list or array");

        self.update_TPX(T, P, X);

    @property
    def viscosity(self):
        return self.mu;

    @viscosity.setter
    def viscosity(self, mu):
        # Viscosity
        if not type(mu) == float:
            raise TypeError("Wrong type! Viscosity must be a float");
        self.update_mu(mu);

    @property
    def density(self):
        return self.rho;

    @density.setter
    def density(self, rho):
        # Density
        if type(rho) == float:
            raise TypeError("Wrong type! Density must be a float");
        self.update_rho(rho);
    
    @property
    def mean_molecular_weight(self):
        return self._mean_MW;

    @property
    def mean_free_path(self):
        return self.lambda_gas;
    
    def update_by_cantera_gas(self, cantera_gas):
        self.update(cantera_gas.T, cantera_gas.P, cantera_gas.X,
                    cantera_gas.density, cantera_gas.viscosity, 
                    cantera_gas.mean_molecular_weight/1000.0);

    def get_molecular_weights_from_cantera(self, cantera_gas):
        self.update_MWs(cantera_gas.molecular_weights/1000.0);


