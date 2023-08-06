"""A python wrapper around the GLobal airglOW (GLOW) model.
GLOW model originally developed by Stanley Solomon et. al.

NCAR-GLOW originally developed by Michael Hirsch, PhD.

This version is maintained by Sunip K. Mukherjee.

Functions
---------
- generic(): Provides uniform calling convention across maxwellian precipitation and no precipitation models.
- maxwellian(): Calculate GLOW model with electron precipitation following Maxwell distribution.
- no_precipitation(): Calculate GLOW model without electron precipitation.
- ebins(): Calculate GLOW model with electron precipitation following custom distribution.
- no_source(): Calculate GLOW model without a source. May give unphysical results, for testing purposes only.

Attributes
----------
- __version__: Reports the version of the package.
"""

from .base import generic, maxwellian, ebins, no_precipitation, no_source

__version__ = '2.0.2'

__all__ = ['generic', 'maxwellian', 'no_precipitation', 'ebins', 'no_source']