#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import libsbml
import numpy as np


def apply_perturbations(species_initial_conditions: np.ndarray,
                        species_names: np.ndarray,
                        perturbations: np.ndarray=None) -> np.ndarray:
    """Update species initial conditions according to a perturbation array

    Arguments:
        species_initial_conditions: The array containing the initial concentrations.
        species_names: The array containing the names of the species.
        perturbations: An array containing the perturbations to apply.

    Returns:
        The updated initial conditions array.
    """

    if perturbations is not None:
        for p in perturbations:
            species_initial_conditions[np.argwhere(species_names == p[0])] = p[1]
    return(species_initial_conditions)

def load_species_initial_conditions(sbml_path: str | os.PathLike, 
                                    perturbations: np.ndarray=None) -> np.ndarray:
    """Create species initial conditions array

    Load initial conditions from the SBML model and update according to
    perturbations.

    Arguments:
        sbml_path:  The path to the SBML model.
        perturbations: An array containing the pertubations to apply.

    Returns:
        The initial conditions array.
        The species names array.
    """

    # Load SBML model
    sbml_reader = libsbml.SBMLReader()
    sbml_doc = sbml_reader.readSBML(sbml_path)
    sbml_model = sbml_doc.getModel()
    # Read species
    species_names = []
    species_initial_conditions = []
    for i in range(0, sbml_model.getNumSpecies()):
        s = sbml_model.getSpecies(i)
        s_name = s.getId()
        s_IC = s.getInitialConcentration()
        if s_name != '':
            species_names = np.append(species_names, s_name)
            species_initial_conditions = np.append(species_initial_conditions, s_IC)
    # Any concentration bellow 1e-6 is considered as zero (0)
    species_initial_conditions[np.argwhere(species_initial_conditions <= 1e-6)] = 0.0
    # Apply perturbations
    species_initial_conditions = apply_perturbations(species_initial_conditions,
                                                     species_names, perturbations)
    return(species_initial_conditions, species_names)

