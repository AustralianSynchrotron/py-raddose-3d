from pydantic import Field, field_validator, model_validator
from typing_extensions import Self

from .utils import RadDoseBase, convert_tuple_to_str


class Crystal(RadDoseBase):
    Type: str = Field(example="Cuboid")
    WireframeType: str | None = None
    ModelFile: str | None = None
    Dimensions: tuple[int] | tuple[int, int] | tuple[int, int, int] | str = Field(
        description="Dimensions of the crystal in X,Y,Z in micrometers.",
        example=(100, 80, 60),
    )
    PixelsPerMicron: float | None = Field(
        description="The computational resolution", example=0.1
    )
    AngleP: float | None = None
    AngleL: float | None = None
    ContainerMaterialType: str | None = None
    MaterialMixture: str | None = None
    MaterialElements: tuple | str | None = Field(
        example=("Si", 1, "O", 2), default=None
    )
    ContainerThickness: float | None = None
    ContainerDensity: float | None = None
    AbsCoefCalc: str | None = Field(
        description="Tells RADDOSE-3D how to calculate the absorption coefficients",
        example="RD3D",
        default=None,
    )
    Pdb: str | None = Field(
        description="Use a PDB for the crystal composition",
        example="1KMT",
        default=None,
    )
    SeqFile: str | None = None
    CIF: str | None = None
    UnitCell: tuple[float, float, float] | tuple[
        float, float, float, float, float, float
    ] | str | None = Field(
        description="Unit cell size: a, b, c, or a, b, c, alpha, beta, gamma",
        example=(78.4, 78.4, 78.4),
        default=None,
    )
    NumMonomers: int | None = Field(
        description="number of monomers in unit cell", example=8, default=None
    )
    NumResidues: int | None = Field(
        descprition="number of residues per monomer", example=153, default=None
    )
    NumRNA: int | None = None
    NumDNA: int | None = None
    NumCarb: int | None = None
    ProteinHeavyAtoms: tuple | str | None = Field(
        description="Heavy atoms added to protein part of the "
        "monomer, i.e. S, coordinated metals, Se in Se-Met"
        "Note: If a sequence file is used, S does not need to be added",
        example=("Zn", 2, "S", 6),
        default=None,
    )
    SolventHeavyConc: tuple | str | None = Field(
        description="Concentration of elements in the solvent in mmol/l. "
        "Oxygen and lighter elements should not be specified",
        example=("P", 425),
        default=None,
    )
    SolventFraction: float | None = Field(
        description="Fraction of the unit cell occupied by solvent",
        example=0.6436,
        default=None,
    )
    ProteinConc: float | None = None
    SmallMoleAtoms: tuple | None = Field(
        example=("C", 18, "H", 15, "Bi", 8), default=None
    )
    CalculatePEescape: bool | None = None
    CalculateFLEscape: bool | None = None
    CalcSurrounding: bool | None = None
    SurroundingHeavyConc: tuple | str | None = Field(
        example=("Na", 1000, "Cl", 1000), default=None
    )
    GoniometerAxis: int | None = None
    PolarisationDirection: int | None = None
    DensityBased: bool | None = None
    SurroundingElements: tuple | str | None = Field(
        example=("C", 3, "H", 8), default=None
    )
    SurroundingDensity: float | None = None
    Subprogram: str | None = None
    Runs: int | None = None
    SimPhotons: int | None = None
    SurroundingThickness: tuple[float, float, float] | str | None = None

    @model_validator(mode="after")
    def validate_type(self) -> Self:
        allowed_type_values = ["cuboid", "spherical", "cylinder", "polyhedron"]
        if self.Type.lower() not in allowed_type_values:
            raise ValueError(
                f"Error validating Crystal Type. Allowed values are {allowed_type_values}, "
                f"not {self.Type}"
            )

        if self.Type.lower() == "polyhedron":
            if self.WireframeType is None or self.ModelFile is None:
                raise ValueError(
                    "If crystal Type=polyhedron, WireframeType and ModelFile "
                    "must be specified. Current values are "
                    f"WireframeType={self.WireframeType} and "
                    f"ModelFile={self.ModelFile}"
                )
        return self

    @field_validator("ContainerMaterialType")
    def validate_ContainerMaterialType(cls, v: str) -> str:
        allowed_values = ["none", "mixture", "elemental"]
        if v.lower() not in allowed_values:
            raise ValueError(
                "Error validating ContainerMaterialType. Allowed values are "
                f"{allowed_values}, not {v}"
            )
        return v

    @field_validator("AbsCoefCalc")
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

    @field_validator("Subprogram")
    def validate_Subprogram(cls, v: str) -> str:
        allowed_values = ["xfel", "montecarlo"]
        if v.lower() not in allowed_values:
            raise ValueError(
                f"Error validating Subprogram. Allowed values are {allowed_values}, not {v}"
            )
        return v

    @field_validator("Dimensions")
    def convert_dimensions_to_str(cls, v):
        return convert_tuple_to_str(v)

    @field_validator("ProteinHeavyAtoms")
    def convert_ProteinHeavyAtoms_to_str(cls, v):
        return convert_tuple_to_str(v)

    @field_validator("SolventHeavyConc")
    def convert_SolventHeavyConc_to_str(cls, v):
        return convert_tuple_to_str(v)

    @field_validator("UnitCell")
    def convert_UnitCell_to_str(cls, v):
        return convert_tuple_to_str(v)

    @field_validator("SmallMoleAtoms")
    def convert_SmallMoleAtoms_to_str(cls, v):
        return convert_tuple_to_str(v)

    @field_validator("MaterialElements")
    def convert_MaterialElements_to_str(cls, v):
        return convert_tuple_to_str(v)

    @field_validator("SurroundingHeavyConc")
    def convert_SurroundingHeavyConc_to_str(cls, v):
        return convert_tuple_to_str(v)

    @field_validator("GoniometerAxis")
    def validate_GoniometerAxis(cls, v):
        allowed_values = [0, 90]
        if v not in allowed_values:
            raise ValueError(
                "Error validating GoniometerAxis. Only 0 and 90 are accepted values"
            )
        return v

    @field_validator("PolarisationDirection")
    def validate_PolarisationDirection(cls, v):
        allowed_values = [0, 90]
        if v not in allowed_values:
            raise ValueError(
                "Error validating PolarisationDirection. Only 0 and 90 are accepted values"
            )
        return v

    @field_validator("SurroundingElements")
    def convert_SurroundingElements_to_str(cls, v):
        return convert_tuple_to_str(v)

    @field_validator("SurroundingThickness")
    def convert_SurroundingThickness_to_str(cls, v):
        return convert_tuple_to_str(v)


class Beam(RadDoseBase):
    Type: str = Field(description="Beam type", example="Gaussian")
    Flux: float = Field(description="Flux in units of photons per second", example=2e12)
    FWHM: tuple[float, float] | str | None = Field(
        description="Full Width Half Maximum in micrometers, X and Y for a Gaussian beam. "
        "X=vertical and Y = horizontal for a horizontal goniometer, opposite for a "
        "vertical goniometer",
        example=(10, 10),
        default=None,
    )
    Energy: float = Field(description="Energy in units of keV", example=12.1)
    EnergyFWHM: float | None = None
    File: str | None = Field(
        description="Tell RADDOSE-3D the name of the file",
        example="beam.pgm",
        default=None,
    )
    PixelSize: tuple[float, float] | str | None = Field(
        description="Specify the pixel size in microns",
        example=(0.3027, 0.2995),
        default=None,
    )
    Collimation: tuple[str, float, float] | str | None = Field(
        description="X/Y collimation of the beam in micrometers. "
        "X = vertical and Y = horizontal for a horizontal goniometer. "
        "Opposite for a vertical goniometer",
        example=("Circular", 30, 30),
        default=None,
    )
    PulseEnergy: float | None = None

    @field_validator("Type")
    def validate_type(cls, v: str) -> str:
        allowed_values = ["tophat", "gaussian", "experimentalpgm"]
        if v.lower() not in allowed_values:
            raise ValueError(
                f"Error validating Beam Type. Allowed values are {allowed_values}, not {v}"
            )
        return v

    @field_validator("Collimation")
    def convert_collimation_to_str(cls, v: tuple[str, float, float]):
        allowed_values = ["rectangular", "circular"]
        if v[0].lower() not in allowed_values:
            raise ValueError(
                f"Error validating Collimation. Allowed values are {allowed_values}, not {v[0]}"
            )
        return convert_tuple_to_str(v)

    @field_validator("FWHM")
    def convert_FWHM_to_str(cls, v):
        return convert_tuple_to_str(v)

    @field_validator("PixelSize")
    def convert_pixel_size_to_str(cls, v):
        return convert_tuple_to_str(v)


class Wedge(RadDoseBase):
    Wedge: tuple[float, float] | str
    ExposureTime: float
    AngularResolution: float | None = None
    StartOffset: tuple[float, float, float] | str | None = None
    TranslatePerDegree: tuple[float, float, float] | str | None = None
    RotAxBeamOffset: float | None = None

    @field_validator("Wedge")
    def convert_Wedge_to_str(cls, v):
        return convert_tuple_to_str(v)

    @field_validator("StartOffset")
    def convert_StartOffset_to_str(cls, v):
        return convert_tuple_to_str(v)

    @field_validator("TranslatePerDegree")
    def convert_TranslatePerDegree_to_str(cls, v):
        return convert_tuple_to_str(v)


class RadDoseInput(RadDoseBase):
    crystal: Crystal
    beam: Beam
    wedge: Wedge | list[Wedge]
