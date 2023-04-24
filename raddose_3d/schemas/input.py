from pydantic import BaseModel, Field


class Crystal(BaseModel):
    type: str = Field(example="Cuboid")
    dimensions: str = Field(
        description="Dimensions of the crystal in X,Y,Z in micrometers."
    )
    coefcalc: str = Field(example="exp")
    pdb: str = Field(
        description="Use a PDB for the crystal composition", example="1KMT"
    )

    # Optional parameters
    absCoefCalc: str | None = Field(
        description="Tells RADDOSE-3D how to calculate the " "Absorption coefficients",
        example="RD3D",
    )


class Beam(BaseModel):
    type: str = Field(description="Beam type", example="Gaussian")
    flux: float = Field(description="Flux in units of photons per second")
    FWHM: str | None = Field(
        description="Full Width Half Maximum in micrometers, X and Y for a Gaussian beam. "
        "X=vertical and Y = horizontal for a horizontal goniometer, opposite for a "
        "vertical goniometer"
    )
    energy: float = Field(description="Energy in units of keV")
    collimation: str | None = Field(
        description="X/Y collimation of the beam in micrometers. "
        "X = vertical and Y = horizontal for a horizontal goniometer. "
        "Opposite for a vertical goniometer"
    )

    # Parameters used for experimental beams only
    file: str | None = Field(
        description="Tell RADDOSE-3D the name of the file", example="beam.pgm"
    )
    PixelSize: str | None = Field(
        description="Specify the pixel size in microns", example="0.3027 0.2995"
    )


class RadDoseInput(BaseModel):
    crystal: Crystal
    beam: Beam
    wedge: str
    exposuretime: float
