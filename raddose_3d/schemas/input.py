from pydantic import BaseModel, Field, validator


def _convert_tuple_to_str(input: tuple) -> str:
    """
    Converts a tuple to a string format that RADDOSE-3D understands

    Parameters
    ----------
    input : tuple
        A tuple input

    Returns
    -------
    str
        A string representation of the tuple, in a format that
        RADDOSE-3D understands
    """
    if input is not None:
        characters = ["(", ")", ",", "'"]
        result = str(input)
        for char in characters:
            result = result.replace(char, "")
        return result
    return result


class Crystal(BaseModel):
    type: str = Field(example="Cuboid")
    dimensions: tuple[int, int, int] | str = Field(
        description="Dimensions of the crystal in X,Y,Z in micrometers.",
        example=(100, 80, 60),
    )
    coefcalc: str = Field(example="exp")
    pdb: str = Field(
        description="Use a PDB for the crystal composition", example="1KMT"
    )

    # Optional parameters
    AbsCoefCalc: str | None = Field(
        description="Tells RADDOSE-3D how to calculate the " "Absorption coefficients",
        example="RD3D",
    )
    NumMonomers: float | None = Field(example=8)
    NumResidues: float | None = Field(example=153)
    ProteinHeavyAtoms: tuple[str, float, str, float] | str | None = Field(
        example=("Zn", 2, "S", 6)
    )
    SolventHeavyConc: tuple[str, float] | str | None = Field(example=("P", 425))
    UnitCell: tuple[float, float, float] | str | None = Field(
        example=(78.4, 78.4, 78.4)
    )
    SolventFraction: float | None = Field(example=0.6436)

    @validator("dimensions", each_item=True)
    def convert_dimensions_to_str(cls, v):
        return _convert_tuple_to_str(v)

    @validator("ProteinHeavyAtoms", each_item=True)
    def convert_ProteinHeavyAtoms_to_str(cls, v):
        return _convert_tuple_to_str(v)

    @validator("SolventHeavyConc", each_item=True)
    def convert_SolventHeavyConc_to_str(cls, v):
        return _convert_tuple_to_str(v)

    @validator("UnitCell", each_item=True)
    def convert_UnitCell_to_str(cls, v):
        return _convert_tuple_to_str(v)


class Beam(BaseModel):
    type: str = Field(description="Beam type", example="Gaussian")
    flux: float = Field(description="Flux in units of photons per second")
    FWHM: tuple[float, float] | str | None = Field(
        description="Full Width Half Maximum in micrometers, X and Y for a Gaussian beam. "
        "X=vertical and Y = horizontal for a horizontal goniometer, opposite for a "
        "vertical goniometer",
        example=(10, 10),
    )
    energy: float = Field(description="Energy in units of keV")
    collimation: tuple[str, float, float] | str | None = Field(
        description="X/Y collimation of the beam in micrometers. "
        "X = vertical and Y = horizontal for a horizontal goniometer. "
        "Opposite for a vertical goniometer",
        example=("Circular", 30, 30),
    )

    # Parameters used for experimental beams only
    file: str | None = Field(
        description="Tell RADDOSE-3D the name of the file", example="beam.pgm"
    )
    PixelSize: str | None = Field(
        description="Specify the pixel size in microns", example="0.3027 0.2995"
    )

    @validator("collimation", each_item=True)
    def convert_collimation_to_str(cls, v):
        return _convert_tuple_to_str(v)

    @validator("FWHM", each_item=True)
    def convert_FWHM_to_str(cls, v):
        return _convert_tuple_to_str(v)


class RadDoseInput(BaseModel):
    crystal: Crystal
    beam: Beam
    wedge: tuple[float, float] | str
    exposuretime: float

    @validator("wedge", each_item=True)
    def convert_tuple_to_str(cls, v: tuple[int, int]) -> str:
        return _convert_tuple_to_str(v)
