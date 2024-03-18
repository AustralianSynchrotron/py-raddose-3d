from pydantic import BaseModel

class RadDoseBase(BaseModel):
    class Config:
        extra = "forbid"



def convert_tuple_to_str(input: tuple) -> str:
    """
    Converts a tuple to a string format that RADDOSE-3D understands

    Parameters
    ----------
    input : tuple
        A tuple input

    Returns
    -------
    str
        A string representation of the tuple, in a format that
        RADDOSE-3D understands
    """
    if input is not None:
        characters = ["(", ")", ",", "'"]
        result = str(input)
        for char in characters:
            result = result.replace(char, "")
        return result
    return result