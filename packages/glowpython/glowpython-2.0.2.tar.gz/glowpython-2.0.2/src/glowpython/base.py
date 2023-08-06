from __future__ import annotations
from typing import Iterable, SupportsFloat as Numeric
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import io
import numpy as np
import pytz
import xarray
import tempfile
import pandas
import shutil
import importlib.resources

import geomagdata as gi
from .build import build

NALT = 250
var = [
    "Tn",
    "O",
    "N2",
    "O2",
    "NO",
    "NeIn",
    "NeOut",
    "ionrate",
    "O+",
    "O2+",
    "NO+",
    "N2D",
    "pedersen",
    "hall",
]

BINPATH = "build"


def get_exe(name: str = "glow.bin") -> Path:
    with importlib.resources.path(__package__, "CMakeLists.txt") as cml:
        src_dir = cml.parent
        bin_dir = src_dir / BINPATH
        exe = shutil.which(name, path=str(bin_dir))
        if not exe:
            try:
                build("meson")
            except Exception:
                build("cmake")

        exe = shutil.which(name, path=str(bin_dir))
        if not exe:
            raise ImportError(
                "GLOW executable not available. This is probably a Python package bug."
            )

    return Path(exe)

def generic(time: datetime, glat: Numeric, glon: Numeric, Nbins: int, Q: Numeric = None, Echar: Numeric = None, *, geomag_params: dict | Iterable = None, tzaware: bool = False) -> xarray.Dataset:
    """GLOW model with optional electron precipitation assuming Maxwellian distribution.
    Defaults to no precipitation.

    Args:
        time (datetime): Model evaluation time.
        glat (Numeric): Location latitude.
        glon (Numeric): Location longitude.
        Q (Numeric, optional): Flux of precipitating electrons. Setting to None or < 0.001 makes it equivalent to no-precipitation. Defaults to None.
        Echar (Numeric, optional): Energy of precipitating electrons. Setting to None or < 1 makes it equivalent to no-precipitation. Defaults to None.
        Nbins (int): Number of energy bins.
        geomag_params (dict | Iterable, optional): Custom geomagnetic parameters 'f107a' (average f10.7 over 81 days), 'f107' (current day f10.7), 'f107p' (previous day f10.7) and 'Ap' (the global 3 hour ap index). Must be present in this order for list or tuple, and use these keys for the dictionary. Defaults to None.
        tzaware (bool, optional): If time is time zone aware. If true, `time` is recast to 'UTC' using `time.astimezone(pytz.utc)`.

    Raises:
        RuntimeError: Invalid type for geomag_params.
        KeyError: Any of the geomagnetic parameter keys absent.
        IndexError: geomag_params does not have at least 4 elements.

    Returns:
        xarray.Dataset: GLOW model output dataset.
    """
    if tzaware:
        time = time.astimezone(pytz.utc)

    idate, utsec = glowdate(time)

    if Q is None or Echar is None: # no precipitation case
        flag = ['-noprecip']
    else: # maxwellian case
        flag = [str(Q), str(Echar)]

    if geomag_params is None:
        ip = gi.get_indices([time - timedelta(days=1), time], 81, tzaware=tzaware)
        f107a = str(ip["f107s"][1])
        f107 = str(ip['f107'][1])
        f107p = str(ip['f107'][0])
        ap = str(ip["Ap"][1])
    elif isinstance(geomag_params, dict):
        f107a = str(geomag_params['f107a'])
        f107 = str(geomag_params['f107'])
        f107p = str(geomag_params['f107p'])
        ap = str(geomag_params['Ap'])
    elif isinstance(geomag_params, Iterable):
        f107a = str(geomag_params[0])
        f107 = str(geomag_params[1])
        f107p = str(geomag_params[2])
        ap = str(geomag_params[3])
    else:
        raise RuntimeError('Invalid type %s for geomag params %s' % (str(type(geomag_params), str(geomag_params))))
    
    ip = {}
    ip['f107a'] = float(f107a)
    ip['f107'] = float(f107)
    ip['f107p'] = float(f107p)
    ip['ap'] = float(ap)

    cmd = [
        str(get_exe()),
        idate,
        utsec,
        str(glat),
        str(glon),
        f107a,
        f107,
        f107p,
        ap
        ] + flag + [
        str(Nbins),
    ]

    dat = subprocess.check_output(cmd, timeout=15, stderr=subprocess.DEVNULL, text=True)

    return glowread(dat, time, ip, glat, glon, Q, Echar)

def maxwellian(time: datetime, glat: Numeric, glon: Numeric, Nbins: int, Q: Numeric, Echar: Numeric, *, geomag_params: dict | Iterable = None, tzaware: bool = False) -> xarray.Dataset:
    """GLOW model with electron precipitation assuming Maxwellian distribution.

    Args:
        time (datetime): Model evaluation time.
        glat (Numeric): Location latitude.
        glon (Numeric): Location longitude.
        Q (Numeric): Flux of precipitating electrons.
        Echar (Numeric): Energy of precipitating electrons.
        Nbins (int): Number of energy bins.
        geomag_params (dict | Iterable, optional): Custom geomagnetic parameters 'f107a' (average f10.7 over 81 days), 'f107' (current day f10.7), 'f107p' (previous day f10.7) and 'Ap' (the global 3 hour ap index). Must be present in this order for list or tuple, and use these keys for the dictionary. Defaults to None.
        tzaware (bool, optional): If time is time zone aware. If true, `time` is recast to 'UTC' using `time.astimezone(pytz.utc)`.

    Raises:
        RuntimeError: Invalid type for geomag_params.
        KeyError: Any of the geomagnetic parameter keys absent.
        IndexError: geomag_params does not have at least 4 elements.

    Returns:
        xarray.Dataset: GLOW model output dataset.
    """
    return generic(time, glat, glon, Nbins, Q, Echar, geomag_params=geomag_params, tzaware=tzaware)


def no_precipitation(time: datetime, glat: Numeric, glon: Numeric, Nbins: int, *, geomag_params: dict | Iterable = None, tzaware: bool = False) -> xarray.Dataset:
    """GLOW model without electron precipitation.

    Args:
        time (datetime): Model evaluation time.
        glat (Numeric): Location latitude.
        glon (Numeric): Location longitude.
        Nbins (int): Number of energy bins.
        geomag_params (dict | Iterable, optional): Custom geomagnetic parameters 'f107a' (average f10.7 over 81 days), 'f107' (current day f10.7), 'f107p' (previous day f10.7) and 'Ap' (the global 3 hour ap index). Must be present in this order for list or tuple, and use these keys for the dictionary. Defaults to None.
        tzaware (bool, optional): If time is time zone aware. If true, `time` is recast to 'UTC' using `time.astimezone(pytz.utc)`.

    Raises:
        RuntimeError: Invalid type for geomag_params.
        KeyError: Any of the geomagnetic parameter keys absent.
        IndexError: geomag_params does not have at least 4 elements.

    Returns:
        xarray.Dataset: GLOW model output dataset.
    """
    return generic(time, glat, glon, Nbins, Q=None, Echar=None, geomag_params=geomag_params, tzaware=tzaware)


def no_source(time: datetime, glat: Numeric, glon: Numeric, Nbins: int, Talt: Numeric, Thot: Numeric, *, geomag_params: dict | Iterable = None, tzaware: bool = False) -> xarray.Dataset:
    """GLOW model without excitation source. Warning: for testing only, may give unphysical results.

    Args:
        time (datetime): Model evaluation time.
        glat (Numeric): Location latitude.
        glon (Numeric): Location longitude.
        Nbins (int): Number of energy bins.
        Talt (Numeric): Altitude of max temperature (?)
        Thot (Numeric): Max temperature (?)
        geomag_params (dict | Iterable, optional): Custom geomagnetic parameters 'f107a' (average f10.7 over 81 days), 'f107' (current day f10.7), 'f107p' (previous day f10.7) and 'Ap' (the global 3 hour ap index). Must be present in this order for list or tuple, and use these keys for the dictionary. Defaults to None.
        tzaware (bool, optional): If time is time zone aware. If true, `time` is recast to 'UTC' using `time.astimezone(pytz.utc)`.

    Raises:
        RuntimeError: Invalid type for geomag_params.
        KeyError: Any of the geomagnetic parameter keys absent.
        IndexError: geomag_params does not have at least 4 elements.

    Returns:
        xarray.Dataset: GLOW model output dataset.
    """
    if tzaware:
        time = time.astimezone(pytz.utc)

    idate, utsec = glowdate(time)

    if geomag_params is None:
        ip = gi.get_indices([time - timedelta(days=1), time], 81, tzaware=tzaware)
        f107a = str(ip["f107s"][1])
        f107 = str(ip['f107'][1])
        f107p = str(ip['f107'][0])
        ap = str(ip["Ap"][1])
    elif isinstance(geomag_params, dict):
        f107a = str(geomag_params['f107a'])
        f107 = str(geomag_params['f107'])
        f107p = str(geomag_params['f107p'])
        ap = str(geomag_params['Ap'])
    elif isinstance(geomag_params, Iterable):
        f107a = str(geomag_params[0])
        f107 = str(geomag_params[1])
        f107p = str(geomag_params[2])
        ap = str(geomag_params[3])
    else:
        raise RuntimeError('Invalid type %s for geomag params %s' % (str(type(geomag_params), str(geomag_params))))
    
    ip = {}
    ip['f107a'] = float(f107a)
    ip['f107'] = float(f107)
    ip['f107p'] = float(f107p)
    ip['ap'] = float(ap)
    
    cmd = [
        str(get_exe()),
        idate,
        utsec,
        str(glat),
        str(glon),
        f107a,
        f107,
        f107p,
        ap,
        "-nosource",
        str(Nbins),
        str(Talt),
        str(Thot),
    ]

    dat = subprocess.check_output(cmd, timeout=15, stderr=subprocess.DEVNULL, text=True)

    return glowread(dat, time, ip, glat, glon)


def ebins(time: datetime, glat: Numeric, glon: Numeric, Ebins: np.ndarray, Phitop: np.ndarray, *, geomag_params: dict | Iterable = None, tzaware: bool = False) -> xarray.Dataset:
    """GLOW model with electron precipitation using custom distribution.

    Args:
        time (datetime): Model evaluation time.
        glat (Numeric): Location latitude.
        glon (Numeric): Location longitude.
        Ebins (np.ndarray): Energy bins.
        Phitop (np.ndarray): Particle flux for the bins.
        geomag_params (dict | Iterable, optional): Custom geomagnetic parameters 'f107a' (average f10.7 over 81 days), 'f107' (current day f10.7), 'f107p' (previous day f10.7) and 'Ap' (the global 3 hour ap index). Must be present in this order for list or tuple, and use these keys for the dictionary. Defaults to None.
        tzaware (bool, optional): If time is time zone aware. If true, `time` is recast to 'UTC' using `time.astimezone(pytz.utc)`.

    Raises:
        OSError: Could not copy all the energy and particle flux data to the temporary file.
        RuntimeError: Invalid type for geomag_params.
        KeyError: Any of the geomagnetic parameter keys absent.
        IndexError: geomag_params does not have at least 4 elements.
        RuntimeError: GLOW model execution failed with the given energy and particle flux.

    Returns:
        xarray.Dataset: GLOW model output.
    """
    # %% Matlab compatible workaround (may change to use stdin in future)
    Efn = Path(tempfile.mkstemp(".dat")[1])
    with Efn.open("wb") as f:
        Ebins.tofile(f)
        Phitop.tofile(f)

    tmpfile_size = Efn.stat().st_size
    expected_size = (Ebins.size + Phitop.size) * 4
    if tmpfile_size != expected_size:
        raise OSError(f"{Efn} size {tmpfile_size} != {expected_size}")

    if tzaware:
        time = time.astimezone(pytz.utc)

    idate, utsec = glowdate(time)

    if geomag_params is None:
        ip = gi.get_indices([time - timedelta(days=1), time], 81, tzaware=tzaware)
        f107a = str(ip["f107s"][1])
        f107 = str(ip['f107'][1])
        f107p = str(ip['f107'][0])
        ap = str(ip["Ap"][1])
    elif isinstance(geomag_params, dict):
        f107a = str(geomag_params['f107a'])
        f107 = str(geomag_params['f107'])
        f107p = str(geomag_params['f107p'])
        ap = str(geomag_params['Ap'])
    elif isinstance(geomag_params, Iterable):
        f107a = str(geomag_params[0])
        f107 = str(geomag_params[1])
        f107p = str(geomag_params[2])
        ap = str(geomag_params[3])
    else:
        raise RuntimeError('Invalid type %s for geomag params %s' % (str(type(geomag_params), str(geomag_params))))
    
    ip = {}
    ip['f107a'] = float(f107a)
    ip['f107'] = float(f107)
    ip['f107p'] = float(f107p)
    ip['ap'] = float(ap)
    
    cmd = [
        str(get_exe()),
        idate,
        utsec,
        str(glat),
        str(glon),
        f107a,
        f107,
        f107p,
        ap,
        "-e",
        str(Ebins.size),
        str(Efn),
    ]

    ret = subprocess.run(cmd, timeout=15, text=True, stdout=subprocess.PIPE)
    if ret.returncode:
        raise RuntimeError(f"GLOW failed at {time}")
    try:
        Efn.unlink()
    except PermissionError:
        # Windows sometimes does this if something else is holding the file open.
        # this is also why we don't use a tempfile context manager for this application.
        pass

    return glowread(ret.stdout, time, ip, glat, glon)


def glowread(raw: str, time: datetime, ip: dict, glat: Numeric, glon: Numeric, Q: Numeric = None, Echar: Numeric = None) -> xarray.Dataset:

    iono = glowparse(raw)
    iono.attrs["geomag_params"] = ip
    if Q is not None and Echar is not None:
        iono.attrs['precip'] = {'Q': Q, 'Echar': Echar}
    iono.attrs["time"] = time.isoformat()
    iono.attrs["glatlon"] = (glat, glon)

    return iono


def glowparse(raw: str) -> xarray.Dataset:

    table = io.StringIO(raw)

    dat = np.genfromtxt(table, skip_header=2, max_rows=NALT)
    alt_km = dat[:, 0]

    if len(var) != dat.shape[1] - 1:
        raise ValueError("did not read raw output from GLOW correctly, please file a bug report.")

    d: dict = {k: ("alt_km", v) for (k, v) in zip(var, dat[:, 1:].T)}
    iono = xarray.Dataset(d, coords={"alt_km": alt_km})
    # %% VER
    dat = np.genfromtxt(table, skip_header=1, max_rows=NALT)
    assert dat[0, 0] == alt_km[0]
    wavelen = [
        3371,
        4278,
        5200,
        5577,
        6300,
        7320,
        10400,
        3644,
        7774,
        8446,
        3726,
        "LBH",
        1356,
        1493,
        1304,
    ]

    ver = xarray.DataArray(
        dat[:, 1:],
        coords={"alt_km": alt_km, "wavelength": wavelen},
        dims=["alt_km", "wavelength"],
        name="ver",
    )
    # %% production & loss
    d = {
        "production": (
            ("alt_km", "state"),
            np.genfromtxt(table, skip_header=0, max_rows=NALT)[:, 1:],
        ),
        "loss": (("alt_km", "state"), np.genfromtxt(table, max_rows=NALT)[:, 1:]),
    }

    state = [
        "O+(2P)",
        "O+(2D)",
        "O+(4S)",
        "N+",
        "N2+",
        "O2+",
        "NO+",
        "N2(A)",
        "N(2P)",
        "N(2D)",
        "O(1S)",
        "O(1D)",
    ]

    prodloss = xarray.Dataset(d, coords={"alt_km": alt_km, "state": state})  # type: ignore
    # %% precip input
    Nbins = int(np.genfromtxt(table, max_rows=1))
    E = np.genfromtxt(table, max_rows=1)
    Eflux = np.genfromtxt(table, max_rows=1)
    precip = xarray.Dataset({"precip": ("energy", Eflux)}, coords={"energy": E})

    assert E.size == Nbins
    # %% excited / ionized densities
    dat = np.genfromtxt(table, skip_header=1, max_rows=NALT)
    assert dat[0, 0] == alt_km[0]
    d = {"excitedDensity": (("alt_km", "state"), dat[:, 1:])}
    excite = xarray.Dataset(d, coords=prodloss.coords)  # type: ignore
    # %% Te, Ti
    dat = np.genfromtxt(table, skip_header=1, max_rows=NALT)
    assert dat[0, 0] == alt_km[0]
    iono["Te"] = ("alt_km", dat[:, 1])
    iono["Ti"] = ("alt_km", dat[:, 2])
    # %% assemble output
    iono = xarray.merge((iono, ver, prodloss, precip, excite))

    unit_dict = {'Tn': 'K',
                 'O': 'cm^{-3}',
                 'N2': 'cm^{-3}',
                 'O2': 'cm^{-3}',
                 'NO': 'cm^{-3}',
                 'NeIn': 'cm^{-3}',
                 'NeOut': 'cm^{-3}',
                 'ionrate': 'cm^{-3}',
                 'O+': 'cm^{-3}',
                 'O2+': 'cm^{-3}',
                 'NO+': 'cm^{-3}',
                 'N2D': 'cm^{-3}',
                 'pedersen': 'S m^{-1}',
                 'hall': 'S m^{-1}',
                 'Te': 'K',
                 'Ti': 'K',
                 'production': 'cm^{-3} s^{-1}',
                 'loss': 's^{-1}',
                 'excitedDensity': 'cm^{-3}',
                 'ver': 'cm^{-3} s^{-1}',
                 'alt_km': 'km',
                 'wavelength': 'angstrom',
                 'energy': 'eV'
                 }

    description_dict = {'Tn': 'Neutral temperature',
                 'O': 'Number density',
                 'N2': 'Number density',
                 'O2': 'Number density',
                 'NO': 'Number density',
                 'NeIn': 'Number density',
                 'NeOut': 'Number density',
                 'ionrate': 'Number density',
                 'O+': 'Number density',
                 'O2+': 'Number density',
                 'NO+': 'Number density',
                 'N2D': 'Number density',
                 'pedersen': 'Pedersen conductivity',
                 'hall': 'Hall conductivity',
                 'Te': 'Electron temperature',
                 'Ti': 'Ion temperature',
                 'production': 'Volume production rate',
                 'loss': 'Loss rate',
                 'excitedDensity': 'Excited/ionized grid density',
                 'ver': 'Photon volume emission rate',
                 'alt_km': 'Altitude grid',
                 'wavelength': 'Emission wavelength',
                 'energy': 'Precipitation energy'
                 }
    _ = list(map(lambda x: iono[x].attrs.update(
        {'units': unit_dict[x], 'description': description_dict[x]}), unit_dict.keys()))

    return iono


def glowdate(t: datetime) -> tuple[str, str]:
    idate = f'{t.year}{t.strftime("%j")}'
    utsec = str(t.hour * 3600 + t.minute * 60 + t.second)

    return idate, utsec
