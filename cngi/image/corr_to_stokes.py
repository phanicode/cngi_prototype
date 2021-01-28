#   Copyright 2020 AUI, Inc. Washington DC, USA
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
this module will be included in the api
"""

def corr_to_stokes(img_dataset):
    """Convert polarization data from the correlation basis to the Stokes parameters.
    
     To be used as a converter during image reconstruction, and also stand-alone. 

    Parameters
    ----------
    img_data : xarray.core.dataset.Dataset
        Input image dataset (e.g., loaded from img.zarr file) with polarization data in the linear (XX,XY,YX,YY) or circular (RR,RL,LR,LL) correlation basis.

    Returns
    -------
    xarray.core.dataset.Dataset
        Output image dataset with polarization data as Stokes (I,Q,U,V) parameters.

    See Also
    --------
    stokes_to_corr

    Notes
    -----
    Polarization codes from the MeasurementSet are preserved in vis.zarr:
    #. I
    #. Q
    #. U
    #. V
    #. RR
    #. RL
    #. LR
    #. LL
    #. XX
    #. XY
    #. YX
    #. YY
   
    .. note::
        Support is presently limited for heterogeneous-feed arrays with elements expected to be missing in a given basis (e.g., very long baseline interferometry with the Event Horizon Telescope).
    """
