import asyncio
import logging
import subprocess
import warnings
from os import getcwd, mkdir, path

import pandas as pd
import yaml

from raddose_3d.schemas.input import Beam, Crystal, RadDoseInput, Wedge

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
        wedge: Wedge,
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
        wedge : Wedge
            A Wedge pydantic model
        output_directory : str | None, optional
            Output directory. If output_directory=None, we use the current working directory,
            by default None.
        """
        self.sample_id = sample_id
        self.crystal = crystal
        self.beam = beam
        self.wedge = wedge

        self.raddose_3d_path = path.join(path.dirname(__file__), "raddose3d.jar")
        if output_directory is None:
            self.output_directory = getcwd()
        else:
            self.output_directory = output_directory

        self.sample_directory = path.join(self.output_directory, self.sample_id)
        try:
            mkdir(self.sample_directory)
        except FileExistsError:
            logging.info("Folder already exists, overwriting results")

        self.prefix = path.join(
            self.sample_directory,
            self.sample_id + "-",
        )

        self.input_text_file_path = self._create_input_txt_file()

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
        yaml_input: list[str] = yaml.dump(
            rad_dose_input.dict(exclude_none=True), sort_keys=False
        ).splitlines()

        file_path = path.join(self.sample_directory, f"{self.sample_id}.txt")
        with open(file_path, "w") as fp:
            for line in yaml_input:
                # For some reason, wedge is not included as a header in the raddose-3d,
                # input file, even though it is defined as a block in raddose-3D
                if line.lower() != "wedge:":
                    fp.write(line.replace(":", "") + "\n")
                else:
                    fp.write("# wedge" + "\n")

        return file_path

    def print_stdout_and_stderr(self, stdout: bytes, stderr: bytes) -> None:
        """
        Prints stdout and stderr

        Parameters
        ----------
        stdout : bytes
            stdout
        stderr : bytes
            stdout

        Raises
        ------
        RuntimeError
            An error if the run is not successful

        Returns
        -------
        None
        """
        if len(stderr) != 0:
            logging.info("Something has gone wrong!")
            raise RuntimeError(str(stderr, encoding="utf-8"))
        else:
            stdout_str = str(stdout, encoding="utf-8")
            logging.info(stdout_str)
            warning_list = ["warning", "angular resolution too big", "* warning *"]

            stdout_list = stdout_str.splitlines()

            for i, line in enumerate(stdout_list):
                if any(warning in line.lower() for warning in warning_list):
                    if "* warning *" in line.lower():
                        warnings.warn(stdout_list[i + 1], RuntimeWarning)
                    else:
                        warnings.warn(line, RuntimeWarning)

            logging.info(f"Results saved to {self.sample_directory}")

    def run(self) -> pd.DataFrame:
        """
        Executes the raddose3d.jar file and returns a pandas DataFrame
        with the summary of the run.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the summary of the run
        """
        process = subprocess.Popen(
            [
                "java",
                "-jar",
                self.raddose_3d_path,
                "-i",
                self.input_text_file_path,
                "-p",
                self.prefix,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

        self.print_stdout_and_stderr(stdout, stderr)

        results_directory = path.join(
            self.sample_directory, f"{self.sample_id}-Summary.csv"
        )
        return pd.read_csv(results_directory)

    async def run_async(self) -> pd.DataFrame:
        """
        Executes the raddose3d.jar file asynchronously and returns a pandas
        DataFrame with the summary of the run.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the summary of the run
        """
        cmd = (
            f"java -jar {self.raddose_3d_path} -i {self.input_text_file_path} "
            + f"-p {self.prefix}"
        )

        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        self.print_stdout_and_stderr(stdout, stderr)

        results_directory = path.join(
            self.sample_directory, f"{self.sample_id}-Summary.csv"
        )
        return pd.read_csv(results_directory)
