from pydantic import NonNegativeFloat, field_validator

from .utils import RadDoseBase, convert_tuple_to_str


class Wedge(RadDoseBase):
    Wedge: tuple[NonNegativeFloat, NonNegativeFloat] | str
    ExposureTime: NonNegativeFloat
    AngularResolution: NonNegativeFloat | None = None
    StartOffset: tuple[float, float, float] | str | None = None
    TranslatePerDegree: tuple[float, float, float] | str | None = None
    RotAxBeamOffset: float | None = None

    @field_validator("Wedge")
    def convert_Wedge_to_str(cls, v):
        return convert_tuple_to_str(v)

    @field_validator("StartOffset")
    def convert_StartOffset_to_str(cls, v):
        return convert_tuple_to_str(v)

    @field_validator("TranslatePerDegree")
    def convert_TranslatePerDegree_to_str(cls, v):
        return convert_tuple_to_str(v)
