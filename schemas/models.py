"""Models & states used in the proofreader's graphs."""

from pathlib import Path
from pydantic import BaseModel, Field


# SCHEMAS
class FileMetadata(BaseModel):
  """Technical metadata representing a file in the local filesystem.

  Attributes:
    name (`str`): The name of the file.
    path (`pathlib.Path`): The absolute path to the file.
  """

  name: str = Field(description="The name of the file.")
  path: Path = Field(description="The absolute path to the file.")
