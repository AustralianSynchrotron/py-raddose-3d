import subprocess
from os import path

import pandas as pd
import yaml

from raddose_3d.schemas.input import Beam, Crystal, RadDoseInput


class RadDose3D:
    def __init__(
        self, sample_id: str, crystal: Crystal, beam: Beam, energy: float
    ) -> None:
        self.sample_id = sample_id
        self.crystal = crystal
        self.beam = beam
        self.energy = energy
        self.raddose_3d_path = path.join(path.dirname(__file__), "raddose3d.jar")

    def _create_pydantic_model(self) -> RadDoseInput:
        rad_dose_input = RadDoseInput(
            crystal=crystal,
            beam=beam,
            energy=self.energy,
            collimation="Circular  30 30",
            wedge="0 360",
            exposuretime=360,
        )
        return rad_dose_input

    def _create_input_txt_file(self):
        rad_dose_input = self._create_pydantic_model()
        yaml_input = yaml.dump(rad_dose_input.dict(), sort_keys=False).splitlines()

        with open(f"{self.sample_id}.txt", "w") as fp:
            for line in yaml_input:
                fp.write(line.replace(":", "") + "\n")

    def run(self):
        self._create_input_txt_file()

        process = subprocess.Popen(
            [
                "java",
                "-jar",
                self.raddose_3d_path,
                "-i",
                f"{self.sample_id}.txt",
                "-p",
                self.sample_id + "-",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()
        if len(stderr) != 0:
            print("Something has gone wrong!")
            raise RuntimeError(str(stderr))

        return pd.read_csv(f"{self.sample_id}-Summary.csv")


if __name__ == "__main__":
    crystal = Crystal(type="Cuboid", dimensions="100 80 60", coefcalc="exp", pdb="1KMT")
    beam = Beam(type="Gaussian", flux=3.8e12, FWHM="10 10")

    rad_dose_3d = RadDose3D(
        sample_id="my_sample", crystal=crystal, beam=beam, energy=12.4
    )

    summary = rad_dose_3d.run()
    print(summary)
