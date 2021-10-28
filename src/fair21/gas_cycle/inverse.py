"""
Module for inverting concentrations.
"""

import numpy as np

def unstep_concentration(
    concentration,
    gas_boxes_old,
    airborne_emissions_old,
    burden_per_emission,
    lifetime,
    alpha_lifetime=1,
    partition_fraction=1,
    pre_industrial_concentration=0,
    timestep=1,
    natural_emissions_adjustment=0,
):
    """
    Calculates emissions from concentrations of any greenhouse gas.

    Parameters
    ----------
    concentration : float
        greenhouse gas concentration at the centre of the timestep.
    gas_boxes_old : ndarray or float
        the greenhouse gas atmospheric burden in each lifetime box at the end of
        the previous timestep.
    airborne_emissions_old : float
        The total airborne emissions at the beginning of the timestep. This is
        the concentrations above the pre-industrial control. It is also the sum
        of gas_boxes_old if this is an array.
    burden_per_emission : float
        how much atmospheric concentrations grow (e.g. in ppm) per unit (e.g.
        GtCO2) emission.
    lifetime : ndarray or float
        atmospheric burden lifetime of greenhouse gas (yr). For multiple
        lifetimes gases, it is the lifetime of each box.
    alpha_lifetime : float, default=1
        scaling factor for `lifetime`. Necessary where there is a state-
        dependent feedback.
    partition_fraction : ndarray or float, default=1
        the partition fraction of emissions into each gas box. If array, the
        entries should be individually non-negative and sum to one.
    pre_industrial_concentration : float, default=0
        pre-industrial concentration gas in question.
    timestep : float, default=1
        emissions timestep in years.
    natural_emissions_adjustment : float or ndarray, default=0
        Amount to adjust emissions by for natural emissions given in the total
        in emissions files.

    Notes
    -----
    Emissions are given in time intervals and concentrations are also reported
    on the same time intervals: the airborne_emissions values are on time
    boundaries. Therefore it is not actually possible to provide the exact
    emissions that would reproduce the concentrations without using a slower
    root-finding mechanism (that was present in v1.4) and will always be half
    a time step out.

    Returns
    -------
    emissions_out : float
        emissions in timestep.
    gas_boxes_new : ndarray of float
        the greenhouse gas atmospheric burden in each lifetime box at the end of
        the timestep.
    airborne_emissions_new : float
        airborne emissions (concentrations above pre-industrial control level)
        at the end of the timestep.
    """

    # comments are keeping track of units
    decay_rate = timestep/(alpha_lifetime * lifetime)   # [1]
    decay_factor = np.exp(-decay_rate)  # [1]

    # [GtCO2] = [ppm] - [ppm] / [ppm/GtCO2]
    airborne_emissions_new = (concentration-pre_industrial_concentration)/burden_per_emission

    # [GtCO2/yr] = [GtCO2] - [GtCO2]*[1] / ([1] * [1] * [1] * [yr])
    emissions =   (( airborne_emissions_new - np.sum(gas_boxes_old*decay_factor)) /
                   (np.sum( partition_fraction / decay_rate * ( 1. - decay_factor ) * timestep)))

    # [GtCO2] = [yr] * [GtCO2/yr] * [1] / [1] * [1] + [GtCO2] * [1]
    gas_boxes_new = timestep * emissions * partition_fraction * 1/decay_rate * ( 1. - decay_factor ) + gas_boxes_old * decay_factor

    emissions_out = emissions + natural_emissions_adjustment

    return emissions_out, gas_boxes_new, airborne_emissions_new