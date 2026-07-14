"""Rich utilities."""

from rich.console import Console
from rich.prompt import Prompt
from rich.theme import Theme
from rich.traceback import install

# CUSTOM THEME 4 RICH
custom_theme = Theme(
  styles={
    # Colores base y utilidades de rich
    "none": "none",
    "reset": "not bold not dim not italic not underline not blink not blink2 not reverse not conceal not strike default on default",
    "italic": "italic",
    "underline": "underline",
    "dim": "dim",
    "reverse": "reverse",
    "strike": "strike",
    "blink": "blink",
    "blink2": "blink2",
    # --- Mapeo de Colores Específicos de Tu Tema VS Code (ahora con aproximaciones de nombres de rich) ---
    # "Strings" (tan) -> #d9a994 (RGB 217,169,148) -> Más cercano en rich: 'tan' (#d7af87)
    "repr.str": "tan",
    "json.str": "not bold not italic tan",
    # "Regular Expression constant" (red tan) -> #de7e7e (RGB 222,126,126) -> Más cercano en rich: 'red3' (#d70000)
    "inspect.error": "bold red3",
    "traceback.error": "italic red3",
    "traceback.error_range": "bold not dim underline red3",
    # "Comment" (dark green) -> #7cad65 (RGB 124,173,101) -> Más cercano en rich: 'dark_sea_green' (#87af87)
    "comment": "dark_sea_green",
    "inspect.doc": "dim dark_sea_green",
    "log.path": "dim dark_sea_green",
    "markdown.code_block": "dark_sea_green on black",
    # "Function declarations" (light yellow) -> #e5e5aa (RGB 229,229,170) -> Más cercano en rich: 'light_yellow3' (#d7d7af)
    "inspect.callable": "bold light_yellow3",
    "inspect.def": "italic light_yellow3",
    "markdown.h1": "bold light_yellow3",
    "markdown.h2": "bold underline light_yellow3",
    "markdown.h3": "bold light_yellow3",
    "markdown.h4": "bold dim light_yellow3",
    "markdown.h5": "underline light_yellow3",
    "markdown.h6": "italic light_yellow3",
    "markdown.h7": "dim italic light_yellow3",
    # "Types declaration and references" (mint green) -> #58d1b9 (RGB 88,209,185) -> Más cercano en rich: 'aquamarine3' (#5fd7af)
    "inspect.class": "italic aquamarine3",
    "inspect.type": "italic aquamarine3",
    "repr.tag_name": "bold aquamarine3",
    # "Object keys, TS grammar specific" (teal) -> #8ed8ff (RGB 142,216,255) -> Más cercano en rich: 'sky_blue1' (#87d7ff)
    "json.key": "bold sky_blue1",
    "repr.attrib_name": "not italic sky_blue1",
    # "Constants and enums" (blue) -> #4FC1FF (RGB 79,193,255) -> Más cercano en rich: 'dodger_blue1' (#0087ff)
    "repr.number": "bold not italic green",
    "json.number": "bold not italic green",
    "repr.ipv4": "bold dodger_blue1",
    "repr.ipv6": "bold dodger_blue1",
    "repr.eui48": "bold dodger_blue1",
    "repr.eui64": "bold dodger_blue1",
    # "Storage Labels" (dark blue - keywords, operators, etc.) -> #63abe5 (RGB 99,171,229) -> Más cercano en rich: 'cornflower_blue' (#5f87ff)
    "bold": "cornflower_blue",
    "logging.keyword": "bold cornflower_blue",
    "code": "bold cornflower_blue on black",
    "markdown.code": "bold cornflower_blue on black",
    # "Control flow / Special keywords" (purple) -> #d990d3 (RGB 217,144,211) -> Más cercano en rich: 'orchid' (#d75fd7)
    "repr.call": "bold orchid",
    "repr.bool_true": "italic orchid",
    "json.bool_true": "italic orchid",
    "repr.none": "italic orchid",
    "json.null": "italic orchid",
    "repr.bool_false": "italic orchid",
    "json.bool_false": "italic orchid",
    # --- Otros estilos de rich ajustados a tus colores existentes (ahora con nombres de rich) ---
    # Barras de progreso
    "bar.complete": "orchid",
    "bar.pulse": "orchid",
    "bar.finished": "dark_sea_green",
    # Layout y árboles
    "layout.tree.column": "not dim cornflower_blue",
    "layout.tree.row": "not dim red3",
    "scope.border": "cornflower_blue",
    "scope.equals": "red3",
    "scope.key": "italic sky_blue1",
    "scope.key.special": "dim italic sky_blue1",
    # Live display
    "live.ellipsis": "bold red3",
    # Logging
    "log.level": "none",
    "log.message": "none",
    "log.time": "dim sky_blue1",
    # Niveles de logging específicos
    "logging.level.critical": "bold reverse red3",
    "logging.level.debug": "dark_sea_green",
    "logging.level.error": "bold red3",
    "logging.level.info": "cornflower_blue",
    "logging.level.notset": "dim",
    "logging.level.warning": "light_yellow3",
    # Markdown
    "markdown.block_quote": "orchid",
    "markdown.em": "italic",
    "markdown.emph": "italic",
    "markdown.hr": "light_yellow3",
    "markdown.item": "none",
    "markdown.item.bullet": "bold light_yellow3",
    "markdown.item.number": "bold light_yellow3",
    "markdown.link": "cornflower_blue",
    "markdown.link_url": "underline cornflower_blue",
    "markdown.list": "sky_blue1",
    "markdown.paragraph": "none",
    "markdown.s": "strike",
    "markdown.strong": "bold",
    "markdown.text": "none",
    # Progress bar
    "progress.data.speed": "red3",
    "progress.description": "none",
    "progress.download": "dark_sea_green",
    "progress.elapsed": "light_yellow3",
    "progress.filesize": "dark_sea_green",
    "progress.filesize.total": "dark_sea_green",
    "progress.percentage": "orchid",
    "progress.remaining": "sky_blue1",
    "progress.spinner": "dark_sea_green",
    # Prompt
    "prompt": "none",
    "prompt.choices": "bold orchid",
    "prompt.default": "bold sky_blue1",
    "prompt.invalid": "red3",
    "prompt.invalid.choice": "red3",
    # Repr
    "repr.attrib_equal": "bold",
    "repr.attrib_value": "tan",
    "repr.brace": "bold gold1",
    "repr.comma": "bold",
    "repr.ellipsis": "light_yellow3",
    "repr.filename": "orchid",
    "repr.indent": "dim dark_sea_green",
    "repr.path": "orchid",
    "repr.tag_contents": "grey85",
    "repr.tag_end": "bold",
    "repr.tag_start": "bold",
    "repr.url": "not bold not italic underline cornflower_blue",
    "repr.uuid": "not bold light_yellow3",
    # Reglas
    "rule.line": "dark_sea_green",
    "rule.text": "none",
    # Status spinner
    "status.spinner": "dark_sea_green",
    # Tablas
    "table.caption": "dim italic",
    "table.cell": "none",
    "table.footer": "bold",
    "table.header": "bold",
    "table.title": "italic",
    # Tracebacks
    "traceback.border": "red3",
    "traceback.border.syntax_error": "red3",
    "traceback.exc_type": "bold red3",
    "traceback.exc_value": "none",
    "traceback.offset": "bold red3",
    "traceback.text": "none",
    "traceback.title": "bold red3",
    # Árbol
    "tree": "none",
    "tree.line": "none",
    # Redefinición de colores estándar de rich con los tonos de tu tema (usando nombres de rich)
    "black": "black",
    "red": "red3",
    "green": "green3",
    "yellow": "yellow3",
    "blue": "blue3",
    "magenta": "magenta3",
    "cyan": "cyan3",
    "white": "white",
    # Versiones "bright" ajustadas para usar nombres de rich
    "bright": "not dim",
    "bright_black": "grey35",
    "bright_red": "red1",
    "bright_green": "green1",
    "bright_yellow": "yellow1",
    "bright_blue": "blue1",
    "bright_magenta": "magenta1",
    "bright_cyan": "cyan1",
    "bright_white": "white",
  }
)

# RICH
con = Console(tab_size=2, theme=custom_theme)
ask = Prompt.ask
rprint = con.print

install(console=con)
