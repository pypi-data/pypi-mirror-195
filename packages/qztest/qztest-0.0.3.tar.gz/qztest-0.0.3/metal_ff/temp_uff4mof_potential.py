# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 下午7:40
# @Author  : wzd
# @File    : temp_uff4mof_potential.py
import networkx as nx

from rdkit.Chem.rdchem import HybridizationType

from .uff4mof_parameter import UFF4MOF, TOTAL_ELEMENTS, get_uff4mof_key, SINGLE_HITS, MULTI_HITS, get_uff4mof_para
from ..molecule import HostGuestComplex


class AtomTypeError(Exception):
    pass


class UFF4MOFPotential:
    def __init__(self, host, guest):
        self._host = host
        self._guest = guest
        self._complex = HostGuestComplex.init_from_molecule(self._host, self._guest)

    def mol_to_graph(self):
        """
        Convert the molecule to a graph.

        Returns
        ------------
        'networkx.Graph': The graph of the molecule.

        """
        mol_graph = nx.Graph()
        for atom in self._complex.get_atoms():
            # Add element name in UFF4MOF style.
            # If the element is 1 character, add a symbol '_' after it.
            # Such as 'C_' is 'C'.
            if len(atom.get_element()) == 1:
                mol_graph.add_node(atom.get_atom_id(), element=f"{atom.get_element()}_",
                                   formal_charge=atom.get_formal_charge(), valence=atom.get_valence(),
                                   is_aromatic=atom.get_is_aromatic(), hybridization=atom.get_hybridization(),
                                   is_metal=atom.get_is_metal())
            else:
                mol_graph.add_node(atom.get_atom_id(), element=atom.get_element(),
                                   formal_charge=atom.get_formal_charge(), valence=atom.get_valence(),
                                   is_aromatic=atom.get_is_aromatic(), hybridization=atom.get_hybridization(),
                                   is_metal=atom.get_is_metal())
        for bond in self._complex.get_bonds():
            edge = (bond.get_atom_1_id(), bond.get_atom_2_id())
            mol_graph.add_edge(*edge, bond_id=bond.get_bond_id(), bond_type=bond.get_bond_type())
        return mol_graph

    def _get_atom_type(self):
        """
        Firstly, match the atom element with the UFF4MOF key.

        """
        mol_graph = self.mol_to_graph()
        for node in mol_graph.nodes:
            element = mol_graph.nodes[node]['element']
            formal_charge = mol_graph.nodes[node]['formal_charge']
            valence = mol_graph.nodes[node]['valence']
            is_aromatic = mol_graph.nodes[node]['is_aromatic']
            hybridization = mol_graph.nodes[node]['hybridization']
            is_metal = mol_graph.nodes[node]['is_metal']
            if element in SINGLE_HITS:
                mol_graph.nodes[node]['atom_type'] = get_uff4mof_key(element)
            elif element in MULTI_HITS:
                if element == 'Ag':
                    if valence == 2 and formal_charge == 1:
                        mol_graph.nodes[node]['atom_type'] = 'Ag1f1'
                    elif valence == 3 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Ag2f2'
                    # elif valence == 4 and formal_charge == 2:
                    #     mol_graph.nodes[node]['atom_type'] = 'Ag3f2'
                    # # Square planar Ag
                    # elif valence == 4 and formal_charge == 2:
                    #     mol_graph.nodes[node]['atom_type'] = 'Ag4f2'
                    else:
                        raise AtomTypeError(
                            f"{element} with valence {valence} is not included.")
                elif element == 'Al':
                    if valence == 6 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'Al6+3'
                    else:
                        if valence == 4 and formal_charge == 2:
                            mol_graph.nodes[node]['atom_type'] = 'Al3f2'
                        else:
                            raise AtomTypeError(
                                f"{element} with valence {valence} is not included.")
                elif element == 'Au':
                    if valence == 4 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'Au4+3'
                    elif valence == 2 and formal_charge == 1:
                        mol_graph.nodes[node]['atom_type'] = 'Au1f1'
                    else:
                        raise AtomTypeError(
                            f"{element} with valence {valence} is not included.")
                elif element == 'B_':
                    if valence == 4:
                        mol_graph.nodes[node]['atom_type'] = 'B_3'
                    elif valence == 3:
                        mol_graph.nodes[node]['atom_type'] = 'B_2'
                    else:
                        raise AtomTypeError(
                            f"{element} with valence {valence} is not included.")

                elif element == 'Ba':
                    if valence == 6 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Ba6+2'
                    elif valence == 4 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Ba3f2'
                    else:
                        raise AtomTypeError(
                            f"{element} with valence {valence} is not included.")

                elif element == 'C_':
                    if hybridization == HybridizationType.SP3:
                        mol_graph.nodes[node]['atom_type'] = 'C_3'
                    elif hybridization == HybridizationType.SP2:
                        if is_aromatic:
                            mol_graph.nodes[node]['atom_type'] = 'C_R'
                        else:
                            mol_graph.nodes[node]['atom_type'] = 'C_2'
                    elif hybridization == HybridizationType.SP:
                        mol_graph.nodes[node]['atom_type'] = 'C_1'
                    else:
                        raise AtomTypeError(
                            f"{element} with valence {valence} is not included.")

                elif element == 'Ca':
                    if valence == 6 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Ca6+2'
                    elif valence == 4 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Ca3f2'
                    else:
                        raise AtomTypeError(
                            f"{element} with valence {valence} is not included.")

                elif element == 'Cd':
                    # ------Sp3 and dSp2 Cd------
                    # if valence == 4 and formal_charge == 2:
                    #     mol_graph.nodes[node]['atom_type'] = 'Cd3+2'
                    # elif valence == 2 and formal_charge == 1:
                    #     mol_graph.nodes[node]['atom_type'] = 'Cd1f1'
                    # elif valence == 4 and formal_charge == 2:
                    #     mol_graph.nodes[node]['atom_type'] = 'Cd3f2'
                    # else:
                    raise AtomTypeError(
                        f"{element} with valence {valence} is not included.")

                elif element == 'Ce':
                    raise AtomTypeError(
                        f"{element} with valence {valence} is not included.")

                elif element == 'Co':
                    raise AtomTypeError(
                        f"{element} with valence {valence} is not included.")

                elif element == 'Cr':
                    if valence == 4 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Cr4+2'
                    elif valence == 6 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'Cr6f3'
                    else:
                        raise AtomTypeError(
                            f"{element} with valence {valence} is not included.")

                elif element == 'Cu':
                    if valence == 4 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Cu3f2'
                    elif valence == 3 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Cu2f2'
                    elif valence == 2 and formal_charge == 1:
                        mol_graph.nodes[node]['atom_type'] = 'Cu1f1'
                    elif valence == 4 and formal_charge == 1:
                        mol_graph.nodes[node]['atom_type'] = 'Cu3+1'
                    else:
                        raise AtomTypeError(
                            f"{element} with valence {valence} is not included.")

                elif element == 'Dy':
                    if valence == 8 and formal_charge == 4:
                        mol_graph.nodes[node]['atom_type'] = 'Dy8f4'
                    elif valence == 6 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'Dy6f3'
                    else:
                        raise AtomTypeError(
                            f"{element} with valence {valence} is not included.")

                elif element == 'Er':
                    if valence == 8 and formal_charge == 4:
                        mol_graph.nodes[node]['atom_type'] = 'Er8f4'
                    elif valence == 6 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'Er6+3'
                    else:
                        raise AtomTypeError(
                            f"{element} with valence {valence} is not included.")

                elif element == 'Eu':
                    if valence == 8 and formal_charge == 4:
                        mol_graph.nodes[node]['atom_type'] = 'Eu8f4'
                    elif valence == 6 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'Eu6+3'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Fe':
                    # SP3 and DSP2 Fe
                    if valence == 6 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'Fe6+3'
                    elif valence == 6 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Fe6+2'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Ga':
                    if valence == 6 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'Ga6f3'
                    elif valence == 4 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Ga3f2'
                    elif valence == 4 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'Ga3+3'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Gd':
                    if valence == 8 and formal_charge == 4:
                        mol_graph.nodes[node]['atom_type'] = 'Gd8f4'
                    elif valence == 6 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'Gd6f3'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'H_':
                    if valence == 1:
                        mol_graph.nodes[node]['atom_type'] = 'H_'
                    elif valence == 2:
                        mol_graph.nodes[node]['atom_type'] = 'H_b'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Hf':
                    if valence == 4 and formal_charge == 4:
                        mol_graph.nodes[node]['atom_type'] = 'Hf3+4'
                    elif valence == 8 and formal_charge == 4:
                        mol_graph.nodes[node]['atom_type'] = 'Hf8f4'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Hg':
                    if valence == 2 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Hg1+2'
                    elif valence == 4 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Hg3f2'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Ho':
                    if valence == 8 and formal_charge == 4:
                        mol_graph.nodes[node]['atom_type'] = 'Ho8f4'
                    elif valence == 6 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'Ho6+3'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'In':
                    if valence == 8 and formal_charge == 4:
                        mol_graph.nodes[node]['atom_type'] = 'In8f4'
                    elif valence == 6 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'In6f3'
                    elif valence == 4 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'In3f2'
                    elif valence == 4 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'In3+3'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'K_':
                    # K_4f2 and K_3f2
                    mol_graph.nodes[node]['atom_type'] = 'K_'
                    # raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'La':
                    pass
                    raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Li':
                    pass
                    raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Lu':
                    pass
                    raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Mg':
                    if valence == 6 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'Mg6f3'
                    elif valence == 4 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Mg3+2'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Mn':
                    pass
                    raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Mo':
                    pass
                    raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'N_':
                    if hybridization == HybridizationType.SP3:
                        mol_graph.nodes[node]['atom_type'] = 'N_3'
                    elif hybridization == HybridizationType.SP2:
                        if is_aromatic:
                            mol_graph.nodes[node]['atom_type'] = 'N_R'
                        else:
                            mol_graph.nodes[node]['atom_type'] = 'N_2'
                    elif hybridization == HybridizationType.SP:
                        mol_graph.nodes[node]['atom_type'] = 'N_1'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Na':
                    pass
                    raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Nb':
                    if valence == 8 and formal_charge == 4:
                        mol_graph.nodes[node]['atom_type'] = 'Nb8f4'
                    elif valence == 4 and formal_charge == 5:
                        mol_graph.nodes[node]['atom_type'] = 'Nb3+5'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Nd':
                    if valence == 8 and formal_charge == 4:
                        mol_graph.nodes[node]['atom_type'] = 'Nd8f4'
                    elif valence == 6 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'Nd6+3'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'O_':
                    if hybridization == HybridizationType.SP3:
                        neighbor = [n for n in mol_graph.neighbors(node)]
                        if is_aromatic:
                            mol_graph.nodes[node]['atom_type'] = 'O_R'
                        else:
                            for n in neighbor:
                                if mol_graph.nodes[n]['is_metal']:
                                    mol_graph.nodes[node]['atom_type'] = 'O_3_f'
                                else:
                                    mol_graph.nodes[node]['atom_type'] = 'O_3'
                    elif hybridization == HybridizationType.SP2:
                        mol_graph.nodes[node]['atom_type'] = 'O_2'
                    elif hybridization == HybridizationType.SP:
                        mol_graph.nodes[node]['atom_type'] = 'O_1'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Os':
                    pass
                    raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'P_':
                    if hybridization == HybridizationType.SP3:
                        neighbor = [n for n in mol_graph.neighbors(node)]
                        for n in neighbor:
                            if mol_graph.nodes[n]['is_metal']:
                                mol_graph.nodes[node]['atom_type'] = 'P_3_q'
                            else:
                                mol_graph.nodes[node]['atom_type'] = 'P_3+3'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Pb':
                    if valence == 4 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Pb4f2'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Pd':
                    if valence == 6 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'Pd6f3'
                    elif valence == 4 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Pd4+2'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Pr':
                    if valence == 8 and formal_charge == 4:
                        mol_graph.nodes[node]['atom_type'] = 'Pr8f4'
                    elif valence == 6 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'Pr6+3'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Re':
                    if valence == 6 and formal_charge == 3:
                        mol_graph.nodes[node]['atom_type'] = 'Re6f3'
                    elif valence == 3 and formal_charge == 7:
                        mol_graph.nodes[node]['atom_type'] = 'Re3+7'
                    elif valence == 6 and formal_charge == 5:
                        mol_graph.nodes[node]['atom_type'] = 'Re6+5'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'Ru':
                    if valence == 4 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Ru4f2'
                    elif valence == 6 and formal_charge == 2:
                        mol_graph.nodes[node]['atom_type'] = 'Ru6+2'
                    else:
                        raise AtomTypeError(f"{element} with valence {valence} is not included.")

                elif element == 'S_':
                    pass

                elif element == 'Sc':
                    pass

                elif element == 'Sm':
                    pass

                elif element == 'Sr':
                    pass

                elif element == 'Tb':
                    pass

                elif element == 'Tc':
                    pass

                elif element == 'Ti':
                    pass

                elif element == 'Tm':
                    pass

                elif element == 'U_':
                    pass

                elif element == 'V_':
                    pass

                elif element == 'W_':
                    pass

                elif element == 'Y_':
                    pass

                elif element == 'Yb':
                    pass

                elif element == 'Zn':
                    pass

                elif element == 'Zr':
                    pass

            else:
                raise ValueError(f"Element {mol_graph.nodes[node]['element']} is not supported.")
        return mol_graph

    def get_parameter(self):
        """


        """
        mol_graph = self._get_atom_type()
        for node in mol_graph.nodes:
            para_list = get_uff4mof_para(mol_graph.nodes[node]['uff4mof_atom_type'])
            mol_graph.nodes[node]['r1'] = para_list[0]
            mol_graph.nodes[node]['theta0'] = para_list[1]
            mol_graph.nodes[node]['x1'] = para_list[2]
            mol_graph.nodes[node]['D1'] = para_list[3]
            mol_graph.nodes[node]['zeta'] = para_list[4]
            mol_graph.nodes[node]['Z1'] = para_list[5]
            mol_graph.nodes[node]['Vi'] = para_list[6]
            mol_graph.nodes[node]['Uj'] = para_list[7]
            mol_graph.nodes[node]['Xi'] = para_list[8]
            mol_graph.nodes[node]['Hard'] = para_list[9]
            mol_graph.nodes[node]['Radius'] = para_list[10]
        return mol_graph

    def cal_potential(self):
        pass
