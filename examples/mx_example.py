"""
This example shows how you can run RADDOSE-3D to simulate a macromolecular crystallography
experiment where a crystal of insulin is exposed to a Gaussian profile X-ray beam for 50
seconds with a 90 degrees rotation (example taken from the the main RADDOSE-3D repository)
"""

from os import path

from py_raddose_3d.raddose3d import RadDose3D
from py_raddose_3d.schemas.input import Beam, Crystal, Wedge

crystal = Crystal(
    GoniometerAxis=90,
    Type="Cuboid",
    Dimensions=(20, 60, 20),
    PixelsPerMicron=1.0,
    AngleL=0,
    AngleP=0,
    # --------------------------------------
    AbsCoefCalc="sequence",
    SeqFile=path.join(path.dirname(__file__), "2veo.fasta"),
    UnitCell=(91.539, 91.539, 299.842, 90.0, 90.0, 90.0),
    NumMonomers=10,
    # ---If not using sequence and experimental data----
    # ---then change AbsCoefCalc to 'Average'-----------
    # AbsCoefCalc="Average",
)

beam = Beam(
    Type="Gaussian",
    Flux=3e11,
    FWHM=(10, 10),
    Energy=13.0,
    # EnergyFWHM=0.0025,  # Slooooow
    Collimation=("Circular", 10, 10),
)

wedge_1 = Wedge(
    Wedge=(0, 180),
    ExposureTime=10,
    AngularResolution=1,
    StartOffset=(0, -20, 0),
)

wedge_2 = Wedge(
    Wedge=(0, 180),
    ExposureTime=10,
    AngularResolution=1,
    StartOffset=(0, -10, 0),
    RotAxBeamOffset=2.5,
    TranslatePerDegree=(0, 0.15, 0),
)

rad_dose_3d = RadDose3D(
    sample_id="my_sample",
    crystal=crystal,
    beam=beam,
    wedge=[
        wedge_1,
        wedge_2,
    ],
    output_directory=None,  # The output directory can be specified here
)

summary = rad_dose_3d.run()
print(summary)
