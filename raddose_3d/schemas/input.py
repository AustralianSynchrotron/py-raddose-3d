from pydantic import BaseModel, Field


class Crystal(BaseModel):
    type: str
    dimensions: str
    coefcalc: str
    pdb: str


class Beam(BaseModel):
    type: str
    flux: float
    FWHM: str
    energy: float
    collimation: str


class RadDoseInput(BaseModel):
    crystal: Crystal
    beam: Beam
    wedge: str
    exposuretime: float
