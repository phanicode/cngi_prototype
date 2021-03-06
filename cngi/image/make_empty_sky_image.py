#  CASA Next Generation Infrastructure
#  Copyright (C) 2021 AUI, Inc. Washington DC, USA
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


def make_empty_sky_image(xds,phase_center,image_size,cell_size,chan_coords,chan_width,pol_coords,time_coords,direction_reference='FK5',projection='SIN', spectral_reference='lsrk',velocity_type='radio',unit='Jy/beam'):
    """
    Create an img_dataset with only coordinates (no datavariables).
    The image dimensionality is either:
        l, m, time, chan, pol

    Parameters
    ----------
    xds : xarray.Dataset
        Empty dataset (dataset = xarray.Dataset())
    phase_center : array of number, length = 2, units = rad
        Image phase center.
    image_size : array of int, length = 2, units = rad
        Number of x and y axis pixels in image.
    cell_size : array of number, length = 2, units = rad
        Cell size of x and y axis pixels in image.
    chan_coords : dask.Array
        The center frequency of each image channel.
    chan_width : dask.Array
        The frequency width of each image channel.
    pol_coords : dask.Array
        The polarization code for each image polarization.
    time_coords : dask.Array
        The time for each image time step.
    direction_reference : str, default = 'FK5'
    projection : str, default = 'SIN'
    spectral_reference : str, default = 'lsrk'
    velocity_type : str, default = 'radio'
    Returns
    -------
    xarray.Dataset
        new xarray Datasets
    """
    import xarray as xr
    import numpy as np

    from astropy.wcs import WCS
    rad_to_deg =  180/np.pi
    w = WCS(naxis=2)
    w.wcs.crpix = np.array(image_size)//2
    w.wcs.cdelt = np.array(cell_size)*rad_to_deg
    w.wcs.crval = np.array(phase_center)*rad_to_deg
    w.wcs.ctype = ['RA---'+projection,'DEC--'+projection]
    
    x = np.arange(image_size[0])
    y = np.arange(image_size[1])
    X, Y = np.meshgrid(x, y,indexing='ij')
    ra, dec = w.wcs_pix2world(X, Y, 1)
    
    #The l,m value can be caluclated from non-integer index using l_val = cell_size*l_indx - image_center[0]*cell_size[0]. This arises when using wcs libarary all_world2pix
    image_center = np.array(image_size)//2
    l = np.arange(-image_center[0], image_size[0]-image_center[0])*cell_size[0]
    m = np.arange(-image_center[1], image_size[1]-image_center[1])*cell_size[1]
    
    coords = {'time':time_coords,'chan': chan_coords, 'pol': pol_coords, 'chan_width' : ('chan',chan_width),'l':l,'m':m,'right_ascension' : (('l','m'),ra/rad_to_deg),'declination' : (('l','m'),dec/rad_to_deg)}
    xds.attrs['axis_units'] = ['rad', 'rad', 'time', 'Hz', 'pol']

    xds = xds.assign_coords(coords)
        
    xds.attrs['direction_reference'] = direction_reference
    xds.attrs['spectral_reference'] = spectral_reference
    xds.attrs['velocity_type'] = velocity_type
    xds.attrs['unit'] = unit
    
    return xds
