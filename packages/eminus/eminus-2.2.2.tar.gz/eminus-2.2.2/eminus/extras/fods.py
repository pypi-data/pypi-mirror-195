#!/usr/bin/env python3
'''Fermi-orbital descriptor generation.'''
import pathlib

import numpy as np
from scipy.linalg import norm

from ..data import SYMBOL2NUMBER
from ..logger import log
from ..tools import center_of_mass
from ..units import ang2bohr, bohr2ang


def get_fods(object, basis='pc-1', loc='FB', clean=True, elec_symbols=None):
    '''Generate FOD positions using the PyCOM method.

    Reference: J. Comput. Chem. 40, 2843.

    Args:
        object: Atoms or SCF object.

    Keyword Args:
        basis (str): Basis set for the DFT calculation.
        loc (str): Localization method (case insensitive).
        clean (bool): Remove log files.
        elec_symbols (list): Identifier for up and down FODs.

    Returns:
        ndarray: FOD positions.
    '''
    try:
        from pyflosic2.atoms.atoms import Atoms
        from pyflosic2.guess.pycom import pycom
        from pyflosic2.parameters.flosic_parameters import parameters
        from pyscf.gto import Mole  # PySCF is a dependency of PyFLOSIC2
        from pyscf.scf import UKS, RKS
    except ImportError:
        log.exception('Necessary dependencies not found. To use this module, '
                      'install them with "pip install eminus[fods]".\n\n')
        raise

    try:
        atoms = object.atoms
    except AttributeError:
        atoms = object
    loc = loc.upper()

    if elec_symbols is None:
        elec_symbols = ['X', 'He']
        if 'He' in atoms.atom and atoms.Nspin == 2:
            log.warning('You need to modify "elec_symbols" to calculate helium in the spin-'
                        'polarized case.')

    # Convert to Angstrom for PySCF
    X = bohr2ang(atoms.X)
    # Build the PySCF input format
    atom_pyscf = list(zip(atoms.atom, X))

    # Spin in PySCF is the difference of up and down electrons
    if atoms.Nspin == 2:
        spin = int(np.sum(atoms.f[0] - atoms.f[1]))
    else:
        spin = int(np.sum(atoms.Z) % 2)

    # Do the PySCF DFT calculation
    # Use Mole.build() over M() since the parse_arg option breaks testing with pytest
    mol = Mole(atom=atom_pyscf, basis=basis, spin=spin).build(parse_arg=False)
    if atoms.Nspin == 2:
        mf = UKS(mol=mol)
    else:
        mf = RKS(mol=mol)
    mf.verbose = 0
    mf.kernel()

    # Do the PyCOM FOD generation
    atoms_pyflosic = Atoms(atoms.atom, X, elec_symbols=elec_symbols, spin=spin)
    if atoms.Nspin == 2:
        p = parameters(mode='unrestricted')
    else:
        p = parameters(mode='restricted')
    p.nuclei = atoms_pyflosic
    p.basis = basis
    p.pycom_loc = loc
    pc = pycom(mf=mf, p=p)
    pc.get_guess()

    fod1 = ang2bohr(pc.p.fod1.positions)
    fod2 = ang2bohr(pc.p.fod2.positions)
    fods = [np.asarray(fod1), np.asarray(fod2)]

    if clean:
        pathlib.Path(p.log_name).unlink()
        pathlib.Path(f'{loc}_GUESS_COM.xyz').unlink()
    return fods


def split_fods(atom, X, elec_symbols=None):
    '''Split atom and FOD coordinates.

    Args:
        atom (list): Atom symbols.
        X (ndarray): Atom positions.

    Keyword Args:
        elec_symbols (list): Identifier for up and down FODs.

    Returns:
        tuple[list, ndarray, list]: Atom types, the respective coordinates, and FOD positions.
    '''
    if elec_symbols is None:
        elec_symbols = ['X', 'He']

    X_fod_up = []
    X_fod_dn = []
    # Iterate in reverted order, because we may delete elements
    for ia in range(len(X) - 1, -1, -1):
        if atom[ia] in elec_symbols:
            if atom[ia] in elec_symbols[0]:
                X_fod_up.append(X[ia])
            if atom[ia] in elec_symbols[1]:
                X_fod_dn.append(X[ia])
            X = np.delete(X, ia, axis=0)
            del atom[ia]

    X_fod = [np.asarray(X_fod_up), np.asarray(X_fod_dn)]
    return atom, X, X_fod


def remove_core_fods(object, fods):
    '''Remove core FODs from a set of FOD coordinates.

    Args:
        object: Atoms or SCF object.
        fods (ndarray): FOD positions.

    Returns:
        ndarray: Valence FOD positions.
    '''
    try:
        atoms = object.atoms
    except AttributeError:
        atoms = object

    # If the number of valence electrons is the same as the number of FODs, do nothing
    if atoms.Nspin == 1 and len(fods[0]) * 2 == np.sum(atoms.f[0]):
        return fods
    if atoms.Nspin == 2 and len(fods[0]) == np.sum(atoms.f[0]) \
            and len(fods[1]) == np.sum(atoms.f[1]):
        return fods

    for spin in range(atoms.Nspin):
        for ia in range(atoms.Natoms):
            n_core = SYMBOL2NUMBER[atoms.atom[ia]] - atoms.Z[ia]
            # In the spin-paired case two electrons are one state
            # Since only core states are removed in pseudopotentials this value is divisible by 2
            # +1 to account for uneven amount of core FODs (e.g., for hydrogen)
            n_core = (n_core + 1) // 2
            dist = norm(fods[spin] - atoms.X[ia], axis=1)
            idx = np.argsort(dist)
            # Remove core FODs with the smallest distance to the core
            fods[spin] = np.delete(fods[spin], idx[:n_core], axis=0)
    return fods


def pycom(object, psirs):
    '''Calculate the orbital center of masses, e.g., from localized orbitals.

    Args:
        object: Atoms or SCF object.
        psirs (ndarray): Set of orbitals in real-space.

    Returns:
        bool: Center of masses.
    '''
    try:
        atoms = object.atoms
    except AttributeError:
        atoms = object

    coms = []
    Ncom = psirs.shape[2]
    for spin in range(atoms.Nspin):
        coms_spin = np.empty((Ncom, 3))

        # Square orbitals
        psi2 = np.real(psirs[spin, :, :].conj() * psirs[spin, :, :])
        for i in range(Ncom):
            coms_spin[i] = center_of_mass(atoms.r, psi2[:, i])
        coms.append(coms_spin)

    # Have the same data structure as for fods
    if atoms.Nspin == 1:
        coms.append(np.array([]))
    return coms
