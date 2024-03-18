from .beam import Beam
from .crystal import Crystal
from .utils import RadDoseBase
from .wedge import Wedge


class RadDoseInput(RadDoseBase):
    crystal: Crystal
    beam: Beam
    wedge: Wedge | list[Wedge]
