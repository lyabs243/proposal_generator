from pydantic import BaseModel

class TechnologyChoice(BaseModel):
    """Model representing a technology choice with its reason.

    Attributes:
        technology (str): The name of the technology.
        reason (str): The reason in few words for choosing the technology.
    """
    technology: str
    reason: str

class TechnologyChoicesResponse(BaseModel):
    """Model representing a response containing multiple technology choices.

    Attributes:
        choices (List[TechnologyChoice]): A list of technology choices.
    """
    choices: list[TechnologyChoice]