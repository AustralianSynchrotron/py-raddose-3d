from pydantic import Field, field_validator, NonNegativeFloat

from .utils import RadDoseBase, convert_tuple_to_str


class Beam(RadDoseBase):
    Type: str = Field(description="Beam type", example="Gaussian")
    Flux: NonNegativeFloat = Field(
        description="Flux in units of photons per second", example=2e12
    )
    FWHM: tuple[NonNegativeFloat, NonNegativeFloat] | str | None = Field(
        description="Full Width Half Maximum in micrometers, X and Y for a Gaussian beam. "
        "X=vertical and Y = horizontal for a horizontal goniometer, opposite for a "
        "vertical goniometer",
        example=(10, 10),
        default=None,
    )
    Energy: NonNegativeFloat = Field(description="Energy in units of keV", example=12.1)
    EnergyFWHM: NonNegativeFloat | None = None
    File: str | None = Field(
        description="Tell RADDOSE-3D the name of the file",
        example="beam.pgm",
        default=None,
    )
    PixelSize: tuple[NonNegativeFloat, NonNegativeFloat] | str | None = Field(
        description="Specify the pixel size in microns",
        example=(0.3027, 0.2995),
        default=None,
    )
    Collimation: tuple[str, NonNegativeFloat, NonNegativeFloat] | str | None = Field(
        description="X/Y collimation of the beam in micrometers. "
        "X = vertical and Y = horizontal for a horizontal goniometer. "
        "Opposite for a vertical goniometer",
        example=("Circular", 30, 30),
        default=None,
    )
    PulseEnergy: NonNegativeFloat | None = None

    @field_validator("Type")
    def validate_type(cls, v: str) -> str:
        allowed_values = ["tophat", "gaussian", "experimentalpgm"]
        if v.lower() not in allowed_values:
            raise ValueError(
                f"Error validating Beam Type. Allowed values are {allowed_values}, not {v}"
            )
        return v

    @field_validator("Collimation")
    def convert_collimation_to_str(
        cls, v: tuple[str, NonNegativeFloat, NonNegativeFloat]
    ):
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
