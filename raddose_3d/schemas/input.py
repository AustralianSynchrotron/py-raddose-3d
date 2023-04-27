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
    Type: str = Field(example="Cuboid")
    Dimensions: tuple[int, int, int] | str = Field(
        description="Dimensions of the crystal in X,Y,Z in micrometers.",
        example=(100, 80, 60),
    )

    # Optional parameters
    Pdb: str | None = Field(
        description="Use a PDB for the crystal composition", example="1KMT"
    )
    Coefcalc: str | None = Field(example="exp")
    AbsCoefCalc: str | None = Field(
        description="Tells RADDOSE-3D how to calculate the absorption coefficients",
        example="RD3D",
    )
    NumMonomers: int | None = Field(
        description="number of monomers in unit cell", example=8
    )
    NumResidues: int | None = Field(
        descprition="number of residues per monomer", example=153
    )
    ProteinHeavyAtoms: tuple | str | None = Field(
        description="Heavy atoms added to protein part of the "
        "monomer, i.e. S, coordinated metals, Se in Se-Met"
        "Note: If a sequence file is used, S does not need to be added",
        example=("Zn", 2, "S", 6),
    )
    SolventHeavyConc: tuple | str | None = Field(
        description="Concentration of elements in the solvent in mmol/l. "
        "Oxygen and lighter elements should not be specified",
        example=("P", 425),
    )
    UnitCell: tuple[float, float, float] | str | None = Field(
        description="Unit cell size: a, b, c", example=(78.4, 78.4, 78.4)
    )
    SolventFraction: float | None = Field(
        description="Fraction of the unit cell occupied by solvent", example=0.6436
    )
    PixelsPerMicron: float | None = Field(
        description="The computational resolution", example=0.1
    )

    @validator("Dimensions", each_item=True)
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
    Type: str = Field(description="Beam type", example="Gaussian")
    Flux: float = Field(description="Flux in units of photons per second", example=2e12)
    FWHM: tuple[float, float] | str | None = Field(
        description="Full Width Half Maximum in micrometers, X and Y for a Gaussian beam. "
        "X=vertical and Y = horizontal for a horizontal goniometer, opposite for a "
        "vertical goniometer",
        example=(10, 10),
    )
    Energy: float = Field(description="Energy in units of keV", example=12.1)
    Collimation: tuple[str, float, float] | str | None = Field(
        description="X/Y collimation of the beam in micrometers. "
        "X = vertical and Y = horizontal for a horizontal goniometer. "
        "Opposite for a vertical goniometer",
        example=("Circular", 30, 30),
    )

    # Parameters used for experimental beams only
    File: str | None = Field(
        description="Tell RADDOSE-3D the name of the file", example="beam.pgm"
    )
    PixelSize: str | None = Field(
        description="Specify the pixel size in microns", example="0.3027 0.2995"
    )

    @validator("Collimation", each_item=True)
    def convert_collimation_to_str(cls, v):
        return _convert_tuple_to_str(v)

    @validator("FWHM", each_item=True)
    def convert_FWHM_to_str(cls, v):
        return _convert_tuple_to_str(v)


class RadDoseInput(BaseModel):
    crystal: Crystal
    beam: Beam
    wedge: tuple[float, float] | str = Field(
        description="Start and End rotational angle of the crystal in degrees",
        example=(0.0, 90.0),
    )
    exposuretime: float = Field(
        description="Total time for entire angular range in seconds", example=50.0
    )

    @validator("wedge", each_item=True)
    def convert_tuple_to_str(cls, v: tuple[int, int]) -> str:
        return _convert_tuple_to_str(v)
