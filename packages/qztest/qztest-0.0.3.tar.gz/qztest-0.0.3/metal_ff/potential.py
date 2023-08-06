# -*- coding: utf-8 -*-
# @Time    : 2022/9/27 下午7:59
# @Author  : wzd
# @File    : potential.py
import abc
import numpy as np

from ..molecule import HostGuestComplex
from .uff4mof_parameter_assign import UFF4MOFAssign

from scipy.spatial import distance
from rdkit.Chem import AllChem


class UFFPotential:
    """
    Very fast energy calculation through 'AllChem.UFFGetMoleculeForceField'
    in 'rdkit'.

    """

    def __init__(
            self,
            host,
            guest
    ):
        self._host = host
        self._guest = guest
        self._complex = HostGuestComplex.init_from_molecule(self._host, self._guest)

    def cal_potential(self):
        """
        Calculate UFF energy using 'AllChem.UFFGetMoleculeForceField()'

        Returns
        -----------------
        'float': The UFF energy.
                 Unit: kcal/mol.

        """
        mol = self._complex.molecule_to_rdkit_mol()
        ff = AllChem.UFFGetMoleculeForceField(mol)
        return ff.CalcEnergy()


class UFF4MOFPotential:
    def __init__(self, host, guest):
        self._host = host
        self._guest = guest
        self._complex = HostGuestComplex.init_from_molecule(self._host, self._guest)

    @staticmethod
    def _cal_vdw(
            len_host,
            len_guest,
            D_i,
            D_j,
            x_i,
            x_j,
            dis_matrix
    ):
        """
        Calculate van der Waals energy.

        Parameters
        -----------------


        Returns
        -----------------
        'numpy.ndarray': The van der Waals energy of each pair of atoms.
                         Unit: kcal/mol.

        """
        vdw_potential = np.zeros(shape=(len_host, len_guest))
        for i in range(len_host):
            for j in range(len_guest):
                D_ij = np.sqrt(D_i[i] * D_j[j])
                x_ij = np.sqrt(x_i[i] * x_j[j])
                d_ij = dis_matrix[i, j]
                vdw_potential[i, j] = D_ij * (-2 * (x_ij / d_ij) ** 6 + (x_ij / d_ij) ** 12)

        return vdw_potential

    @staticmethod
    def _cal_electrostatic(
            len_host,
            len_guest,
            q_i,
            q_j,
            dis_matrix
    ):
        """
        Calculate electrostatic energy.

        Parameters
        -----------------
        """
        electrostatic_potential = np.zeros(shape=(len_host, len_guest))
        for i in range(len_host):
            for j in range(len_guest):
                q_ij = q_i[i] * q_j[j]
                d_ij = dis_matrix[i, j]
                electrostatic_potential[i, j] = 332.0637 * (q_ij / d_ij)

        return electrostatic_potential

    def cal_potential(
            self,
            mol_path,
            format_in='mol',
            ff_name='UFF',
            charge='qeq'):
        host_uff4mof_assign = UFF4MOFAssign(
            mol_path=mol_path,
            format_in=format_in,
            molecule=self._host,
            ff_name=ff_name,
            charge=charge
        )
        guest_uff4mof_assign = UFF4MOFAssign(
            mol_path=mol_path,
            format_in=format_in,
            molecule=self._guest,
            ff_name=ff_name,
            charge=charge
        )

        host_graph = host_uff4mof_assign.get_parameter()
        guest_graph = guest_uff4mof_assign.get_parameter()

        len_host = self._host.get_atom_number()
        len_guest = self._guest.get_atom_number()
        D_i = [host_graph.nodes[i]['D1'] for i in host_graph]
        D_j = [guest_graph.nodes[i]['D1'] for i in guest_graph]
        x_i = [host_graph.nodes[i]['x1'] for i in host_graph]
        x_j = [guest_graph.nodes[i]['x1'] for i in guest_graph]
        q_i = [host_graph.nodes[i]['partial_charge'] for i in host_graph]
        q_j = [guest_graph.nodes[i]['partial_charge'] for i in guest_graph]

        dis_matrix = distance.cdist(
            self._host.get_positions(),
            self._guest.get_positions()
        )

        vdw_potential = self._cal_vdw(
            len_host=len_host,
            len_guest=len_guest,
            D_i=D_i,
            D_j=D_j,
            x_i=x_i,
            x_j=x_j,
            dis_matrix=dis_matrix
        )

        electrostatic_potential = self._cal_electrostatic(
            len_host=len_host,
            len_guest=len_guest,
            q_i=q_i,
            q_j=q_j,
            dis_matrix=dis_matrix
        )

        return np.sum(vdw_potential) + np.sum(electrostatic_potential)
