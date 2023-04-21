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


class RadDoseInput(BaseModel):
    crystal: Crystal
    beam: Beam
    energy: float = Field(description="Energy in keV")
    collimation: str
    wedge: str
    exposuretime: float
