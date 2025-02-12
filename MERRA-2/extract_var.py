import xarray as xr
import os

def load_dataset(file, directions):
    variables_to_keep = ['QV', 'SLP', 'T', 'U', 'V']
    ds = xr.open_dataset(file)
    ds_var_sliced = ds[variables_to_keep]

    ds_latlon_var_sliced = ds_var_sliced.sel(lat=slice(directions['South'], directions['North']), 
                                             lon=slice(directions['West'], directions['East']))

    ds_all_sliced = ds_latlon_var_sliced.sel(lev=slice(1000, 300))

    output_dir = "merra2"

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    base_filename = os.path.basename(file).replace(".nc4", "")
    output_file = os.path.join(output_dir, f"{base_filename}_sliced.nc")

    print(f"Saving to {output_file}")
    ds_all_sliced.to_netcdf(output_file)
    print(f"Saved {output_file}")

if __name__ == '__main__':
    directions = {'North': 60, 
                'East': 300, 
                'South': 20, 
                'West': 60} 
    # Convert degrees west to degrees east
    directions['West'] = directions['West'] - 360
    directions['East'] = directions['East'] - 360

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
        "C:\\Users\\Tony\\Downloads\\MERRA2_400.inst3_3d_asm_Np.20151201.nc4"
    ]

    for file in files:
        load_dataset(file, directions)