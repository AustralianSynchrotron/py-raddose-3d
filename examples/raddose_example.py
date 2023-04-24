from raddose_3d.raddose3d import RadDose3D
from raddose_3d.schemas.input import Beam, Crystal

crystal = Crystal(type="Cuboid", dimensions="100 80 60", coefcalc="exp", pdb="1KMT")
beam = Beam(
    type="Gaussian", flux=3.8e7, FWHM="10 10", energy=12.4, collimation="Circular 30 30"
)

rad_dose_3d = RadDose3D(
    sample_id="my_sample",
    crystal=crystal,
    beam=beam,
    wedge="0.0 360.0",
    exposure_time=10.0,
)

summary = rad_dose_3d.run()
print(summary)
