# -*- coding: utf-8 -*-
# @Time    : 6/13/22 8:18 PM
# @Author  : name
# @File    : potential.py
"""
Future work:
    1. Convert 'guest' to 'list(guest)' for multiple guest.
"""
import numpy as np

from numpy import ndarray
from scipy.spatial import distance
from rdkit.Chem import AllChem

from .amber_parameters import Amber99Parameter
from ..molecule import HostGuestComplex


class SimpleLJPotential:

    def __init__(self, host, guest, epsilon=1):
        """

        """
        self._host = host
        self._guest = guest
        self._epsilon = epsilon
        self._host_positions = self._host.get_positions()
        self._guest_positions = self._guest.get_positions()

    @staticmethod
    def _lorentz_berthelot_method(sigma_i: float, sigma_j: float) -> float:
        return 0.5 * (sigma_i + sigma_j)

    def _cal_sigma(self):
        host_radii = self._host.get_radii_list()
        guest_radii = self._guest.get_radii_list()

        sigma_matrix = np.zeros((self._host.get_atom_number(), self._guest.get_atom_number()))
        for i in range(self._host.get_atom_number()):
            for j in range(self._guest.get_atom_number()):
                sigma_matrix[i, j] = self._lorentz_berthelot_method(
                    host_radii[i], guest_radii[j]
                )

        return sigma_matrix

    def _cal_dis_matrix(self):
        return distance.cdist(self._host_positions, self._guest_positions)

    def _cal_lj_potential(self, sigma, distance, epsilon):
        return 4 * epsilon * (
                (sigma / distance) ** 12 - (sigma / distance) ** 6
        )

    def cal_potential(self):
        pair_potential = []
        sigma_matrix = self._cal_sigma()
        dis_matrix = self._cal_dis_matrix()

        for i in range(self._host.get_atom_number()):
            for j in range(self._guest.get_atom_number()):
                pair_potential.append(
                    self._cal_lj_potential(
                        sigma=sigma_matrix[i, j],
                        distance=dis_matrix[i, j],
                        epsilon=self._epsilon,
                    )
                )

        return np.sum(pair_potential, axis=0)


class AmberPotential:
    """
    Inspired by the article:
    'EDock: blind protein–ligand docking by replica-exchange monte carlo simulation'

    Notes
    ------
    There are now 3 equations in this class.
    1. Van Der Waals interaction
        sum(w1 * ((A_ij / d_ij ** 12) - (B_ij / d_ij ** 6)))
        ------
        where:
            A_ij = epsilon_ij * (R_ij ** 12) ;
            B_ij = 2 * epsilon_ij * (R_ij ** 6) ;
            R_ij = host_radii[i] + guest_radii[j] ;
            epsilon_ij = (epsilon_i * epsilon_j) ** 0.5;
            d_ij = dis_matrix[i, j]

    2. Electrostatic interaction
        sum(w2 * ((host_charge[i] * guest_charge[j]) / 4 * dis_matrix[i, j]))

    3. Constrain the distance between host and guest

    """

    def __init__(
            self,
            host,
            guest,
            w1=0.1,
            w2=1
    ):
        self._host = host
        self._guest = guest
        self._w1 = w1
        self._w2 = w2
        self._w3 = 1 - w1

    def _get_charge_param(self):
        pass

    def _get_pair_distance(self):
        dis_matrix = distance.cdist(
            self._host.get_positions(),
            self._guest.get_positions()
        )
        return dis_matrix

    def _cal_vdw(self,
                 host_radii: list,
                 guest_radii: list,
                 len_host: int,
                 len_guest: int,
                 epsilon_i: list,
                 epsilon_j: list,
                 dis_matrix: ndarray) -> ndarray:
        vdw_array = np.zeros((len_host, len_guest))

        for i in range(len_host):
            for j in range(len_guest):
                epsilon_ij = (epsilon_i[i] * epsilon_j[j]) ** 0.5
                R_ij = host_radii[i] + guest_radii[j]
                A_ij = epsilon_ij * (R_ij ** 12)
                B_ij = 2 * epsilon_ij * (R_ij ** 6)
                d_ij = dis_matrix[i, j]

                vdw_array[i, j] = (
                        self._w1 * ((A_ij / d_ij ** 12) - (B_ij / d_ij ** 6))
                )

        return vdw_array

    def _cal_electrostatic(self,
                           len_host: int,
                           len_guest: int,
                           host_charge: list,
                           guest_charge: list,
                           dis_matrix: ndarray) -> ndarray:
        charge_interaction = np.zeros((len_host, len_guest))

        for i in range(len_host):
            for j in range(len_guest):
                charge_interaction[i, j] = (
                        self._w2 * ((host_charge[i] * guest_charge[j]) / 4 * dis_matrix[i, j]))
        return charge_interaction

    def _cal_distance_weight(self) -> ndarray:
        """------NEED TO BE IMPROVED------"""
        com_host = self._host.get_centroid_remove_h()
        distance_matrix = distance.cdist(com_host.reshape(1, 3), self._guest.get_positions())
        # return self._w3 * np.sum(distance_matrix)
        return distance_matrix[0, :]

    def cal_potential(self):
        para_calculator = Amber99Parameter()

        dis_matrix = self._get_pair_distance()
        len_host = self._host.get_atom_number()
        len_guest = self._guest.get_atom_number()

        radii_i, epsilon_i, charge_i = para_calculator.get_parameters(self._host)
        radii_j, epsilon_j, charge_j = para_calculator.get_parameters(self._guest)

        # ------OLD VERSION------
        # vdw_potential = self._cal_vdw(
        #     host_radii=[atom.get_atomic_radius() for atom in self._host.get_atoms()],
        #     guest_radii=[atom.get_atomic_radius() for atom in self._guest.get_atoms()],
        #     len_host=len_host,
        #     len_guest=len_guest,
        #     epsilon_i=epsilon_i,
        #     epsilon_j=epsilon_j,
        #     dis_matrix=dis_matrix
        # )

        vdw_potential = self._cal_vdw(
            host_radii=radii_i,
            guest_radii=radii_j,
            len_host=len_host,
            len_guest=len_guest,
            epsilon_i=epsilon_i,
            epsilon_j=epsilon_j,
            dis_matrix=dis_matrix
        )

        electrostatic_potential = self._cal_electrostatic(
            len_host=len_host,
            len_guest=len_guest,
            host_charge=charge_i,
            guest_charge=charge_j,
            dis_matrix=dis_matrix
        )

        distance_weight = self._cal_distance_weight()

        return self._w1 * np.sum(vdw_potential) + self._w2 * np.sum(electrostatic_potential) + self._w3 * np.sum(
            distance_weight)


class UFFPotential:
    def __init__(
            self,
            host,
            guest
    ):
        self._host = host
        self._guest = guest
        self._complex = HostGuestComplex.init_from_molecule(self._host, self._guest)

    def cal_potential(self):
        mol = self._complex.molecule_to_rdkit_mol()
        ff = AllChem.UFFGetMoleculeForceField(mol)
        return ff.CalcEnergy()
