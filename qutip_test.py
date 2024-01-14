from qutip import qutip, basis, tensor, Bloch, Qobj, qeye
from typing import List, Dict, Tuple
import numpy as np
from qutip.qip.operations import *

import matplotlib.pyplot as plt

class InvalidArgumentError(Exception):
    Exception()


class Qutip_Helper:
    def __init__(self, state_vec : List = None, groundState : tuple[bool, int] = (False, None)):
        """
        Example to initialize on the H|1> state: Qutip_Helper(1/np.sqrt(2)*np.array([1, -1]))
        
        """
        if len(groundState) != 2 or not isinstance(groundState[0], bool) or not isinstance(groundState[1], int):
            raise InvalidArgumentError("Invalid ground state given. It should be a tuple with a boolean and an integer.")

        if groundState[0]:
            self.state = tensor([basis(2, 0) for _ in range(groundState[1])])
            self.num_qubits = groundState[1]

        else:
            if state_vec is None:
                raise RuntimeError("State vector should be given!")
            
            # This part is lacking of different sized quantum states!
            # Works only for the one qubit change it so it will work for every possible state
            self.state = Qobj(state_vec, dims=[[2], [1]])
            self.num_qubits = 1

    def apply_gate(self, gate_name : str, target, control = None):
        gate : Qobj = getattr(qutip.qip.operations.gates, gate_name)(N=self.num_qubits, target=target)

        if gate is None:
            raise Exception("No such a gate found in the gate set!")
        
        # Create the tensor product with the X gate at the specified index
        #gate_multi_qubit = tensor([qeye(2) if j == target else gate for j in range(self.num_qubits)])

        self.state = gate * self.state


    def stateInfo(self):
        total_size = 1
        for dim in self.state.dims[0]:
            total_size *= dim

        print("""Total dimension of the state: {}\nState Sizes (Dimensions): {}
              """.format(total_size, self.state.dims))
    

    def display_Bloch(self):
        bloch_obj = qutip.Bloch()

        if len(self.state.dims[0]) > 1:
            for i in range(len(self.state.dims[0])):

                bloch_obj.add_states(self.state.ptrace(i))
                bloch_obj.make_sphere()

                bloch_obj.show()
                bloch_obj.clear()

        else:
            bloch_obj.add_states(self.state)
            bloch_obj.make_sphere()
            bloch_obj.show()
        