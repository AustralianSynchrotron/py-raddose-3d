import glob
import shutil
import subprocess
from os import mkdir, path

import pandas as pd
import yaml

from raddose_3d.schemas.input import Beam, Crystal, RadDoseInput


class RadDose3D:
    def __init__(
        self,
        sample_id: str,
        crystal: Crystal,
        beam: Beam,
        wedge: tuple[float, float],
        exposure_time: float,
        output_directory="./",
    ) -> None:
        self.sample_id = sample_id
        self.crystal = crystal
        self.beam = beam
        self.wedge = wedge
        self.exposure_time = exposure_time

        self.raddose_3d_path = path.join(path.dirname(__file__), "raddose3d.jar")
        self.output_directory = output_directory

        try:
            mkdir(path.join(self.output_directory, self.sample_id))
        except FileExistsError:
            pass

    def _create_pydantic_model(self) -> RadDoseInput:
        rad_dose_input = RadDoseInput(
            crystal=crystal,
            beam=beam,
            wedge=self.wedge,
            exposuretime=self.exposure_time,
        )
        return rad_dose_input

    def _create_input_txt_file(self):
        rad_dose_input = self._create_pydantic_model()
        yaml_input = yaml.dump(rad_dose_input.dict(), sort_keys=False).splitlines()

        file_path = path.join(
            self.output_directory, self.sample_id, f"{self.sample_id}.txt"
        )
        with open(file_path, "w") as fp:
            for line in yaml_input:
                fp.write(line.replace(":", "") + "\n")

        return file_path

    def run(self):
        input_text_file_path = self._create_input_txt_file()

        process = subprocess.Popen(
            [
                "java",
                "-jar",
                self.raddose_3d_path,
                "-i",
                input_text_file_path,
                "-p",
                self.sample_id + "-",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()
        if len(stderr) == 0:
            # Search files with .txt extension in source directory
            patterns = ["*.txt", "*.csv", "*.R"]
            for pattern in patterns:
                files = glob.glob(path.join("./", pattern))

                # move the files with txt extension
                for file in files:
                    # extract file name form file path
                    file_name = path.basename(file)
                    shutil.move(
                        file,
                        path.join(self.output_directory, self.sample_id, file_name),
                    )
        else:
            print("Something has gone wrong!")
            raise RuntimeError(str(stderr))

        results_directory = path.join(
            self.output_directory, self.sample_id, f"{self.sample_id}-Summary.csv"
        )

        return pd.read_csv(results_directory)


if __name__ == "__main__":
    crystal = Crystal(type="Cuboid", dimensions="100 80 60", coefcalc="exp", pdb="1KMT")
    beam = Beam(type="Gaussian", flux=3.8e12, FWHM="10 10", energy=12.4, collimation="Circular 30 30")

    rad_dose_3d = RadDose3D(
        sample_id="my_sample",
        crystal=crystal,
        beam=beam,
        wedge="0.0 360.0",
        exposure_time=360.0,
    )

    summary = rad_dose_3d.run()
    print(summary)
