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
    WireframeType: str | None
    ModelFile: str | None
    Dimensions: tuple[int] | tuple[int, int] | tuple[int, int, int] | str = Field(
        description="Dimensions of the crystal in X,Y,Z in micrometers.",
        example=(100, 80, 60),
    )
    PixelsPerMicron: float | None = Field(
        description="The computational resolution", example=0.1
    )
    AngleP: float | None
    AngleL: float | None
    ContainerMaterialType: str | None
    MaterialMixture: str | None
    MaterialElements: tuple | str | None = Field(example=("Si", 1, "O", 2))
    ContainerThickness: float | None
    ContainerDensity: float | None
    AbsCoefCalc: str | None = Field(
        description="Tells RADDOSE-3D how to calculate the absorption coefficients",
        example="RD3D",
    )
    Pdb: str | None = Field(
        description="Use a PDB for the crystal composition", example="1KMT"
    )
    SeqFile: str | None
    CIF: str | None
    UnitCell: tuple[float, float, float] | tuple[
        float, float, float, float, float, float
    ] | str | None = Field(
        description="Unit cell size: a, b, c, or a, b, c, alpha, beta, gamma",
        example=(78.4, 78.4, 78.4),
    )
    NumMonomers: int | None = Field(
        description="number of monomers in unit cell", example=8
    )
    NumResidues: int | None = Field(
        descprition="number of residues per monomer", example=153
    )
    NumRNA: int | None
    NumDNA: int | None
    NumCarb: int | None
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
    SolventFraction: float | None = Field(
        description="Fraction of the unit cell occupied by solvent", example=0.6436
    )
    ProteinConc: float | None
    SmallMoleAtoms: tuple | None = Field(example=("C", 18, "H", 15, "Bi", 8))
    CalculatePEescape: bool | None
    CalculateFLEscape: bool | None
    CalcSurrounding: bool | None
    SurroundingHeavyConc: tuple | str | None = Field(example=("Na", 1000, "Cl", 1000))
    GoniometerAxis: int | None
    PolarisationDirection: int | None
    DensityBased: bool | None
    SurroundingElements: tuple | str | None = Field(example=("C", 3, "H", 8))
    SurroundingDensity: float | None
    Subprogram: str | None
    Runs: int | None
    SimPhotons: int | None
    SurroundingThickness: tuple[float, float, float] | str | None

    @validator("Type", each_item=True)
    def validate_type(cls, v: str) -> str:
        allowed_values = ["cuboid", "spherical", "cylinder", "polyhedron"]
        if v.lower() not in allowed_values:
            raise ValueError(
                f"Error validating Crystal Type. Allowed values are {allowed_values}, not {v}"
            )
        return v

    @validator("ContainerMaterialType", each_item=True)
    def validate_ContainerMaterialType(cls, v: str) -> str:
        allowed_values = ["none", "mixture", "elemental"]
        if v.lower() not in allowed_values:
            raise ValueError(
                "Error validating ContainerMaterialType. Allowed values are "
                f"{allowed_values}, not {v}"
            )
        return v

    @validator("AbsCoefCalc", each_item=True)
    def validate_AbsCoefCalc(cls, v: str) -> str:
        allowed_values = [
            "average",
            "dummy",
            "rd",
            "rdv2",
            "rdv3",
            "rd3d",
            "exp",
            "sequence",
            "saxs",
            "saxsseq",
            "smallmole",
            "cif",
        ]
        if v.lower() not in allowed_values:
            raise ValueError(
                f"Error validating AbsCoefCalc. Allowed values are {allowed_values}, not {v}"
            )
        return v

    @validator("Subprogram", each_item=True)
    def validate_Subprogram(cls, v: str) -> str:
        allowed_values = ["xfel", "montecarlo"]
        if v.lower() not in allowed_values:
            raise ValueError(
                f"Error validating Subprogram. Allowed values are {allowed_values}, not {v}"
            )
        return v

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

    @validator("SmallMoleAtoms", each_item=True)
    def convert_SmallMoleAtoms_to_str(cls, v):
        return _convert_tuple_to_str(v)

    @validator("MaterialElements", each_item=True)
    def convert_MaterialElements_to_str(cls, v):
        return _convert_tuple_to_str(v)

    @validator("SurroundingHeavyConc", each_item=True)
    def convert_SurroundingHeavyConc_to_str(cls, v):
        return _convert_tuple_to_str(v)

    @validator("GoniometerAxis", each_item=True)
    def validate_GoniometerAxis(cls, v):
        allowed_values = [0, 90]
        if v not in allowed_values:
            raise ValueError(
                "Error validating GoniometerAxis. Only 0 and 90 are accepted values"
            )
        return v

    @validator("PolarisationDirection", each_item=True)
    def validate_PolarisationDirection(cls, v):
        allowed_values = [0, 90]
        if v not in allowed_values:
            raise ValueError(
                "Error validating PolarisationDirection. Only 0 and 90 are accepted values"
            )
        return v

    @validator("SurroundingElements", each_item=True)
    def convert_SurroundingElements_to_str(cls, v):
        return _convert_tuple_to_str(v)

    @validator("SurroundingThickness", each_item=True)
    def convert_SurroundingThickness_to_str(cls, v):
        return _convert_tuple_to_str(v)

    class Config:
        extra = "forbid"


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
    EnergyFWHM: float | None
    File: str | None = Field(
        description="Tell RADDOSE-3D the name of the file", example="beam.pgm"
    )
    PixelSize: tuple[float, float] | str | None = Field(
        description="Specify the pixel size in microns", example=(0.3027, 0.2995)
    )
    Collimation: tuple[str, float, float] | str | None = Field(
        description="X/Y collimation of the beam in micrometers. "
        "X = vertical and Y = horizontal for a horizontal goniometer. "
        "Opposite for a vertical goniometer",
        example=("Circular", 30, 30),
    )
    PulseEnergy: float | None

    @validator("Type", each_item=True)
    def validate_type(cls, v: str) -> str:
        allowed_values = ["tophat", "gaussian", "experimentalpgm"]
        if v.lower() not in allowed_values:
            raise ValueError(
                f"Error validating Beam Type. Allowed values are {allowed_values}, not {v}"
            )
        return v

    @validator("Collimation", each_item=True)
    def convert_collimation_to_str(cls, v: tuple[str, float, float]):
        allowed_values = ["rectangular", "circular"]
        if v[0].lower() not in allowed_values:
            raise ValueError(
                f"Error validating Collimation. Allowed values are {allowed_values}, not {v[0]}"
            )
        return _convert_tuple_to_str(v)

    @validator("FWHM", each_item=True)
    def convert_FWHM_to_str(cls, v):
        return _convert_tuple_to_str(v)

    @validator("PixelSize", each_item=True)
    def convert_pixel_size_to_str(cls, v):
        return _convert_tuple_to_str(v)

    class Config:
        extra = "forbid"


class Wedge(BaseModel):
    Wedge: tuple[float, float] | str
    ExposureTime: float
    AngularResolution: float | None
    StartOffset: tuple[float, float, float] | str | None
    TranslatePerDegree: tuple[float, float, float] | str | None
    RotAxBeamOffset: float | None

    @validator("Wedge", each_item=True)
    def convert_Wedge_to_str(cls, v):
        return _convert_tuple_to_str(v)

    @validator("StartOffset", each_item=True)
    def convert_StartOffset_to_str(cls, v):
        return _convert_tuple_to_str(v)

    @validator("TranslatePerDegree", each_item=True)
    def convert_TranslatePerDegree_to_str(cls, v):
        return _convert_tuple_to_str(v)


class RadDoseInput(BaseModel):
    crystal: Crystal
    beam: Beam
    wedge: Wedge

    class Config:
        extra = "forbid"
