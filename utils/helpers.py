"""Utilities (constants, functions, reducers & schemas) used in graphs."""

import re
from pathlib import Path
from typing import Literal, Union
from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from rich.progress import track


type LLM = Literal[
  "gpt20",
  "gpt120",
  "llama31",
  "llama33",
  "qwen36",
  "gmn25flash",
  "gmn25lite",
  "gmn25pro",
  "gmn3flash",
  "gmn31lite",
  "gmn31pro",
  "gmn35flash",
]

# PATHS
CWD: Path = Path(__file__).cwd()
PDF_DIR: Path = CWD / "pdf"


# SCHEMAS
class FileMetadata(BaseModel):
  """Technical metadata representing a file in the local filesystem.

  Attributes:
    name (`str`): The name of the file.
    path (`pathlib.Path`): The absolute path to the file.
  """

  name: str = Field(description="The name of the file.")
  path: Path = Field(description="The absolute path to the file.")


# UTILITY FUNCTIONS
def find_files(dir_path: Path | str, file_type: str = "pdf") -> list[FileMetadata]:
  """Searches for files of a specific type in a directory.

  Args:
    dir_path (Path | str): The directory path to search.
    file_type (str): The file extension to filter by. Defaults to `"pdf"`.

  Returns:
    A list of `FileMetadata` objects for found files.

  Raises:
    ValueError: If the directory does not exist, is empty, or no files of the specified type are found.
  """

  dir_path = Path(dir_path)

  if not dir_path.is_dir():
    raise ValueError(f"❌ files_finder() => DIRECTORY ({dir_path}) DOESN'T EXIST.")

  if not any(dir_path.iterdir()):
    raise ValueError(f"❌ files_finder() => DIRECTORY ({dir_path}) IS EMPTY.")

  if not file_type.startswith("."):
    file_type = f".{file_type}"

  # SEARCH FOR REQUIRED FILES
  files_metadata: list[FileMetadata] = [
    FileMetadata(name=f.name, path=f)
    for f in track(
      dir_path.glob(f"*{file_type}"),
      description="[bold cyan]🔍 SEARCHING FILES[/]",
      total=len(list(dir_path.glob(f"*{file_type}"))),
    )
    if f.is_file()
  ]

  # CHECK IF FILES WERE FOUND
  if not files_metadata:
    raise FileNotFoundError(
      f"❌ files_finder() => NO FILES OF TYPE ({file_type}) WERE FOUND IN DIRECTORY ({dir_path})."
    )

  return files_metadata


def clean_text(text: str) -> str:
  """Normalizes whitespace and line breaks in text.

  Performs the following operations:
    1. Replaces non-breaking spaces with standard spaces.
    2. Collapses multiple spaces into single spaces.
    3. Normalizes multiple line breaks (3+) to double line breaks.
    4. Trims leading/trailing whitespace from paragraphs.

  Args:
    text (str): The input text to clean.

  Returns:
    The cleaned and normalized text.
  """

  # FROM NON-BREAKING SPACE CHARACTER TO A REGULAR SPACE
  text_without_non_breaking_spaces: str = re.sub(r"\xa0", " ", text)
  # FROM MULTIPLE SPACES TO A SINGLE SPACE
  text_without_multiple_spaces: str = re.sub(r" {2,}", " ", text_without_non_breaking_spaces)
  # FROM >=3 LINE BREAKS TO DOUBLE LINE BREAKS
  text_without_multiple_line_breaks: str = re.sub(r"\n{3,}", "\n\n", text_without_multiple_spaces)
  # TRIM LEADING AND TRAILING WHITESPACE
  text_without_leading_and_trailing_whitespace: str = "\n\n".join(
    [
      double_line_break.strip()
      for double_line_break in text_without_multiple_line_breaks.split("\n\n")
    ]
  )

  text_cleaned: str = text_without_leading_and_trailing_whitespace.strip()

  return text_cleaned


def is_text_corrupt(text) -> bool:
  """Checks if text appears to be corrupt or malformed.

  Determines corruption based on the ratio of valid characters (alphabetic and spaces) to total characters.

  Args:
    text (str): The text to analyze.

  Returns:
    `True` if the text is empty or has a low valid character ratio (< 0.7), `False` otherwise.
  """

  if not text.strip():
    return True

  # COUNTS ALPHABETIC CHARACTERS & SPACES
  total_chars: int = len(text)
  valid_chars: int = sum(c.isalpha() or c.isspace() for c in text)

  # IF TOO FEW ALPHABETIC CHARACTERS, MARK AS CORRUPT
  if (valid_chars / total_chars) < 0.7:
    return True

  return False


def validate_content(text: str, keywords: list[str]) -> bool:
  """Validates if the extracted text is sufficient and contains relevant keywords.

  Args:
    text: The extracted text to validate.
    keywords: List of keywords to search for (case-insensitive)

  Returns:
    `True` if text is not corrupt and contains at least one keyword.
  """
  if not text or is_text_corrupt(text):
    return False

  lowered_txt: str = text.lower()
  return any(word.lower() in lowered_txt for word in keywords)


def load_md(path2md: Path) -> str:
  """Loads a markdown file using `pathlib.Path`.

  Args:
    path2md (Path): The path to the markdown file.

  Returns:
    The content of the markdown file.
  """

  return path2md.read_text(encoding="utf-8")


def select_llm(model: LLM, temp: float = 0.0) -> Union[ChatGroq, ChatGoogleGenerativeAI]:
  """Initializes and returns a specific LLM instance.

  Args:
    model (LLM): The identifier of the model to use. Must be one of the supported model codes (`"gpt20"`, `"gpt120"`, `"llama31"`, `"llama33"`, `"qwen36"`, `"gmn25flash"`, `"gmn25lite"`, `"gmn25pro"`, `"gmn3flash"`, `"gmn31lite"`, `"gmn31pro"`, `"gmn35flash"`).
    temp (float): The temperature to use for the LLM. Defaults to `0.0`.

  Returns:
    An instance of `ChatGroq` or `ChatGoogleGenerativeAI` configured with the selected model.

  Raises:
    AssertionError: if the provided model identifier is not supported.
  """

  models: dict[str, tuple[str, str]] = {
    # ** GROQ **
    # OpenAI
    "gpt20": ("groq", "openai/gpt-oss-20b"),
    "gpt120": ("groq", "openai/gpt-oss-120b"),
    # Meta
    "llama31": ("groq", "llama-3.1-8b-instant"),
    "llama33": ("groq", "llama-3.3-70b-versatile"),
    # Qwen
    "qwen36": ("groq", "qwen/qwen3.6-27b"),
    # ** GOOGLE **
    # Gemini 2.5
    "gmn25flash": ("google", "gemini-2.5-flash"),
    "gmn25lite": ("google", "gemini-2.5-flash-lite"),
    "gmn25pro": ("google", "gemini-2.5-pro"),
    # Gemini 3
    "gmn3flash": ("google", "gemini-3-flash-preview"),
    "gmn31lite": ("google", "gemini-3.1-flash-lite"),
    "gmn31pro": ("google", "gemini-3.1-pro-preview"),
    # Gemini 3.5
    "gmn35flash": ("google", "gemini-3.5-flash"),
  }

  selected: str = model.lower().strip()

  if selected not in models:
    raise ValueError(f"\033[1;31m❗INVALID LLM MODEL: {selected}❗\033[0m")

  provider, model_name = models[selected]

  if provider == "groq":
    return ChatGroq(model=model_name, temperature=temp)

  return ChatGoogleGenerativeAI(model=model_name, temperature=temp)


# REDUCERS
def merge_lists(existing: list | None, new: list | None) -> list:
  """State reducer that merges two lists, filtering out `None` values.

  Ensures that the graph state remains clean by consolidating parallel updates
  into a single contiguous list.

  Args:
    existing (`list | None`): The current list in the graph state.
    new (`list | None`): The new data (list or single item) to be merged.

  Returns:
    A new list containing all consolidated non-None elements.
  """
  if existing is None:
    existing = []

  if new is None:
    return existing

  new_list = new if isinstance(new, list) else [new]

  # Filter None values from the new batch
  cleaned_new = [item for item in new_list if item is not None]

  return existing + cleaned_new


def merge_tuples(existing: tuple | None, new: tuple | None) -> tuple:
  """State reducer that merges two tuples, filtering out `None` values.

  Used primarily for error collection, ensuring that multiple node failures
  are captured in a single immutable sequence.

  Args:
    existing (`tuple | None`): The current tuple in the graph state.
    new (`tuple | None`): The new data (tuple or single item) to be merged.

  Returns:
    A new tuple containing all consolidated non-None elements.
  """
  if existing is None:
    existing = tuple()

  if new is None:
    return existing

  new_tuple = new if isinstance(new, tuple) else (new,)

  cleaned_new = [item for item in new_tuple if item is not None]

  return existing + tuple(cleaned_new)


if __name__ == "__main__":
  print("Hello from helpers!")
