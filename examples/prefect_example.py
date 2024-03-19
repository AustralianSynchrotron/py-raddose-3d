import asyncio

from prefect import flow, task

from py_raddose_3d.raddose3d import RadDose3D
from py_raddose_3d.schemas.input import Beam, Crystal, Wedge


@task
async def run_raddose(sample_id: str) -> RadDose3D:
    crystal = Crystal(
        Type="Cuboid",
        Dimensions=(100, 100, 100),
        AbsCoefCalc="RD3D",
        UnitCell=(78.02, 78.02, 78.02),
    )

    beam = Beam(
        Type="Gaussian",
        Flux=2e12,
        FWHM=(20, 70),
        Energy=12.1,
        Collimation=("Rectangular", 100, 100),
    )

    wedge = Wedge(Wedge=(0.0, 90.0), ExposureTime=50.0, AngularResolution=0.3)

    sample = RadDose3D(
        sample_id=sample_id,
        crystal=crystal,
        beam=beam,
        wedge=wedge,
    )
    await sample.run_async()


@flow
async def multiple_samples():
    sample_1 = run_raddose("sample_1")
    sample_2 = run_raddose("sample_2")
    sample_3 = run_raddose("sample_3")
    await asyncio.gather(*[sample_1, sample_2, sample_3])


asyncio.run(multiple_samples())
