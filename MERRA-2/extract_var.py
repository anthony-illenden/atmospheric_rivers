import xarray as xr
import metpy.calc as mpcalc
from metpy.units import units
import os 
import numpy as np

def load_ds(file):
    ds = xr.open_dataset(file)
    return ds

def slice_ds(ds, directions): 
    variables_to_keep = ['QV', 'SLP', 'T', 'U', 'V']
    ds_var_sliced = ds[variables_to_keep]
    ds_latlon_var_sliced = ds_var_sliced.sel(lat=slice(directions['South'], directions['North']), 
                                                lon=slice(directions['West'], directions['East']))
    return ds_latlon_var_sliced

def calc_ivt_thetae(ds, level):
    g = 9.81  # units: m/s2
    level_hpa = level * units.hPa  # units: hPa

    # Lists to store computed values
    ivt_list = []
    theta_e_gradient_list = []

    # Loop over time steps and perform calculations
    for time in ds.time:
        # Select variables at all pressure levels
        u_sliced = ds['U'].sel(time=time, lev=slice(1000, 300))  # units: m/s
        v_sliced = ds['V'].sel(time=time, lev=slice(1000, 300))  # units: m/s
        q_sliced = ds['QV'].sel(time=time, lev=slice(1000, 300))  # units: kg/kg
        t_sliced = ds['T'].sel(time=time, lev=slice(1000, 300))  # units: K
        mslp = ds['SLP'].sel(time=time) / 100  # Convert Pa to hPa

        # Select variables at the specified level
        u_lev = u_sliced.sel(lev=level_hpa)  # units: m/s
        v_lev = v_sliced.sel(lev=level_hpa)  # units: m/s
        q_lev = q_sliced.sel(lev=level_hpa)  # units: kg/kg
        t_lev = t_sliced.sel(lev=level_hpa)  # units: K
        p_lev = level * units.hPa # units: hPa

        # Extract pressure levels 
        pressure_levels = u_sliced['lev'] * 100 # units: Pa

        # Calculate IVT
        u_ivt = -1 / g * np.trapz(u_sliced * q_sliced, pressure_levels, axis=0)
        v_ivt = -1 / g * np.trapz(v_sliced * q_sliced, pressure_levels, axis=0)

        # Calculate IVT magnitude
        ivt = np.sqrt(u_ivt**2 + v_ivt**2)
        ivt_da = xr.DataArray(ivt, dims=['lat', 'lon'], coords={'lat': u_sliced['lat'], 'lon': u_sliced['lon']})
        ivt_list.append(ivt_da)

        # Calculate dewpoint and theta-e
        td_lev = mpcalc.dewpoint_from_specific_humidity(p_lev, t_lev, q_lev)
        theta_e = mpcalc.equivalent_potential_temperature(p_lev, t_lev, td_lev)

        # Compute theta-e gradient
        dtheta_e_dx, dtheta_e_dy = mpcalc.geospatial_gradient(theta_e)
        theta_e_gradient = np.sqrt(dtheta_e_dx**2 + dtheta_e_dy**2) * 1e5  # Convert to K/100 km

        theta_e_gradient_da = xr.DataArray(theta_e_gradient, dims=['lat', 'lon'], coords={'lat': u_sliced['lat'], 'lon': u_sliced['lon']})
        theta_e_gradient_list.append(theta_e_gradient_da)

    ivt_da = xr.concat(ivt_list, dim='time')
    ivt_da.name = 'IVT'

    theta_e_gradient_da = xr.concat(theta_e_gradient_list, dim='time')
    theta_e_gradient_da.name = 'theta_e_gradient'

    # Add computed variables to dataset
    ds = ds.assign({
        'IVT': ivt_da,
        'thetae_grad': theta_e_gradient_da
    })

    final_variables = ['SLP', 'IVT', 'thetae_grad']
    ds_final = ds[final_variables]

    return ds_final

def save_ds(ds): 
    output_dir = "merra2_sliced"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    base_filename = os.path.basename(file).replace(".nc4", "")
    output_file = os.path.join(output_dir, f"{base_filename}_sliced.nc")
    print(f"Saving to {output_file}")
    ds.to_netcdf(output_file)
    print(f"Saved {output_file}")

if __name__ == '__main__':
    directions = {'North': 60, 
                'East': 300, 
                'South': 20, 
                'West': 60} 
    # Convert degrees west to degrees east
    directions['West'] = directions['West'] - 360
    directions['East'] = directions['East'] - 360
    level = 925 # units: hPa

    files = [
        "C:\\Users\\Tony\\Downloads\\MERRA2_400.inst3_3d_asm_Np.20151214.nc4",
        "C:\\Users\\Tony\\Downloads\\MERRA2_400.inst3_3d_asm_Np.20151213.nc4",
        "C:\\Users\\Tony\\Downloads\\MERRA2_400.inst3_3d_asm_Np.20151212.nc4",
        "C:\\Users\\Tony\\Downloads\\MERRA2_400.inst3_3d_asm_Np.20151211.nc4",
        "C:\\Users\\Tony\\Downloads\\MERRA2_400.inst3_3d_asm_Np.20151210.nc4",
        "C:\\Users\\Tony\\Downloads\\MERRA2_400.inst3_3d_asm_Np.20151209.nc4",
        "C:\\Users\\Tony\\Downloads\\MERRA2_400.inst3_3d_asm_Np.20151208.nc4",
        "C:\\Users\\Tony\\Downloads\\MERRA2_400.inst3_3d_asm_Np.20151207.nc4",
        "C:\\Users\\Tony\\Downloads\\MERRA2_400.inst3_3d_asm_Np.20151206.nc4",
        "C:\\Users\\Tony\\Downloads\\MERRA2_400.inst3_3d_asm_Np.20151205.nc4",
        "C:\\Users\\Tony\\Downloads\\MERRA2_400.inst3_3d_asm_Np.20151204.nc4",
        "C:\\Users\\Tony\\Downloads\\MERRA2_400.inst3_3d_asm_Np.20151203.nc4",
        "C:\\Users\\Tony\\Downloads\\MERRA2_400.inst3_3d_asm_Np.20151202.nc4",
        "C:\\Users\\Tony\\Downloads\\MERRA2_400.inst3_3d_asm_Np.20151201.nc4"]

    for file in files:
        ds = load_ds(file)
        ds_sliced = slice_ds(ds, directions)
        ds_final = calc_ivt_thetae(ds_sliced, level)
        save_ds(ds_final)