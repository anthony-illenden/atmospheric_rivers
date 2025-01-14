# Atmospheric Rivers

This repository contains a variety of scripts for analyzing real-time model data (GFS) and model reanalysis data (ERA5). The focus is on Integrated Water Vapor Transport (IVT) and Integrated Water Vapor (IWV) for the GFS, and various gradients for ERA5.

The formula to calculate Integrated Water Vapor Transport (IVT) can be seen below:

$$ 
IVT = -\frac{1}{g} \int_{p_0}^{p_t} qV \, dp 
$$

where \( g \) is 9.81 m/s<sup>-2</sup> (i.e., Earth’s gravitational acceleration), \( p_0 \) is 1000-hPa, \( p_t \) is 300-hPa, \( q \) is specific humidity, and \( V \) is the total wind in the horizontal (i.e., u- and v-components).

The formula to calculate Integrated Water Vapor (IWV) can be seen below:

$$
IWV = -\frac{1}{g} \int_{p_0}^{p_t} q \, dp
$$

where \( g \) is 9.81 m/s<sup>-2</sup> (i.e., Earth’s gravitational acceleration), \( p_0 \) is 1000-hPa, \( p_t \) is 300-hPa, and \( q \) is specific humidity.


## Repository Structure

- **ERA5/**
  - `mfw_thermo_gradient_comp.ipynb`: Jupyter Notebook for comparing Wet-Bulb Potential Temperature and Equivalent Potential Temperature gradients using ERA5 reanalysis data.
  - `mfw_thetae_gradient.ipynb`: Jupyter Notebook for analyzing Equivalent Potential Temperature gradients using ERA5 reanalysis data.
  - `mfw_wbpt_gradient.ipynb`: Jupyter Notebook for analyzing Wet-Bulb Potential Temperature gradients using ERA5 reanalysis data.

- **GFS/**
  - `ivt.ipynb`: Jupyter Notebook for analyzing Integrated Water Vapor Transport (IVT) using GFS real-time model data.
  - `iwv.ipynb`: Jupyter Notebook for analyzing Integrated Water Vapor (IWV) using GFS real-time model data.