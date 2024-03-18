import asyncio

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

sample_1 = RadDose3D(
    sample_id="sample_1",
    crystal=crystal,
    beam=beam,
    wedge=wedge,
)

sample_2 = RadDose3D(
    sample_id="sample_2",
    crystal=crystal,
    beam=beam,
    wedge=wedge,
)


async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(sample_1.run_async())
        tg.create_task(sample_2.run_async())


asyncio.run(main())
