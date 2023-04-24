import glob
import logging
import shutil
import subprocess
from os import mkdir, path, getcwd

import pandas as pd
import yaml

from raddose_3d.schemas.input import Beam, Crystal, RadDoseInput

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)


class RadDose3D:
    """
    Python wrapper of RADDOSE-3D
    """

    def __init__(
        self,
        sample_id: str,
        crystal: Crystal,
        beam: Beam,
        wedge: list[float, float],
        exposure_time: float,
        output_directory: str | None = None,
    ) -> None:
        """
        Parameters
        ----------
        sample_id : str
            Sample id
        crystal : Crystal
            A Crystal Pydantic model
        beam : Beam
            A Beam pydantic model
        wedge : list[float, float]
            Wedge in degrees, e.g. [0, 360]
        exposure_time : float
            Exposure time in seconds
        output_directory : str | None, optional
            Output directory, by default the current directory
        """
        self.sample_id = sample_id
        self.crystal = crystal
        self.beam = beam
        self.wedge = wedge
        self.exposure_time = exposure_time

        self.raddose_3d_path = path.join(path.dirname(__file__), "raddose3d.jar")
        if output_directory is None:
            self.output_directory = getcwd()

        try:
            mkdir(path.join(self.output_directory, self.sample_id))
        except FileExistsError:
            pass

    def _create_pydantic_model(self) -> RadDoseInput:
        """
        Creates a RadDoseInput pydantic model

        Returns
        -------
        RadDoseInput
            The raddose input pydantic model
        """
        rad_dose_input = RadDoseInput(
            crystal=self.crystal,
            beam=self.beam,
            wedge=self.wedge,
            exposuretime=self.exposure_time,
        )
        return rad_dose_input

    def _create_input_txt_file(self) -> str:
        """
        Writes a text file that RADDOSE-3D understands and returns
        the path of the text file

        Returns
        -------
        str
            The path of the RADDOSE-3D input text file
        """
        rad_dose_input = self._create_pydantic_model()
        yaml_input = yaml.dump(
            rad_dose_input.dict(exclude_none=True), sort_keys=False
        ).splitlines()

        file_path = path.join(
            self.output_directory, self.sample_id, f"{self.sample_id}.txt"
        )
        with open(file_path, "w") as fp:
            for line in yaml_input:
                fp.write(line.replace(":", "") + "\n")

        return file_path

    def run(self) -> pd.DataFrame:
        """
        Executes the raddose3d.jar file and returns a pandas dataframe
        with the summary of the run. The resulting data generated from the
        data are moved to self.output_directory.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the summary of the run

        Raises
        ------
        RuntimeError
            An error if the run is not successful
        """
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
            # Move files to self.output_directory/self.sample_id
            patterns = ["*.txt", "*.csv", "*.R"]
            for pattern in patterns:
                files = glob.glob(path.join("./", pattern))
                for file in files:
                    file_name = path.basename(file)
                    shutil.move(
                        file,
                        path.join(self.output_directory, self.sample_id, file_name),
                    )
        else:
            logging.info("Something has gone wrong!")
            raise RuntimeError(stderr)

        results_directory = path.join(
            self.output_directory, self.sample_id, f"{self.sample_id}-Summary.csv"
        )

        return pd.read_csv(results_directory)
