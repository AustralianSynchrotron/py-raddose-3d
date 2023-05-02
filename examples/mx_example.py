"""
This example shows how you can run RADDOSE-3D to simulate a macromolecular crystallography
experiment where a crystal of insulin is exposed to a Gaussian profile X-ray beam for 50
seconds with a 90 degrees rotation (example taken from the the main RADDOSE-3D repository)
"""

from raddose_3d.raddose3d import RadDose3D
from raddose_3d.schemas.input import Beam, Crystal, Wedge

crystal = Crystal(
    Type="Cuboid",
    Dimensions=(100, 100, 100),
    PixelsPerMicron=0.1,
    AbsCoefCalc="RD3D",
    UnitCell=(78.02, 78.02, 78.02),
    NumMonomers=24,
    NumResidues=51,
    ProteinHeavyAtoms=("Zn", 0.333, "S", 6),
    SolventHeavyConc=("P", 425),
    SolventFraction=0.64,
)

beam = Beam(
    Type="Gaussian",
    Flux=2e12,
    FWHM=(20, 70),
    Energy=12.1,
    Collimation=("Rectangular", 100, 100),
)

wedge = Wedge(Wedge=(0.0, 90.0), ExposureTime=50.0)

rad_dose_3d = RadDose3D(
    sample_id="my_sample",
    crystal=crystal,
    beam=beam,
    wedge=wedge,
)

summary = rad_dose_3d.run()
print(summary)
