from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from enum import auto, IntEnum
from importlib.metadata import version
from itertools import dropwhile, takewhile, zip_longest
import re
try: import tomllib
except ModuleNotFoundError: import tomli as tomllib
from typing import Any

from jinja2 import Environment, StrictUndefined, UndefinedError
from loguru import logger
import tomli_w
from wcmatch.pathlib import Path

logger.disable("dirtem")

pattern_isjinja = re.compile(r"\{# *isjinja *#\}")
pattern_nojinja = re.compile(r"\{# *nojinja *#\}")

class _PatternStyle(IntEnum):
    GLOB = auto()
    REGEX = auto()
    
    @classmethod
    def from_string(cls, string: str):
        return cls[string.upper()]

def _remove_parents(parent: Path, child: Path) -> Path:
    """
    Removes the parent path from the its child path.
    """
    return map(lambda part: part[1], dropwhile(
       lambda part: part[0] == part[1],
       zip_longest(parent.parts, child.parts)
    ))

def _render_until_unnamed(
    env: Environment,
    it: Iterable[str],
    variables: dict[str, Any],
    do_prompt: bool = True,
) -> Iterable[str]:
    return takewhile(bool, (
        _render_or_prompt(env, part, variables, do_prompt = do_prompt) for part in it
    ))

def _get_missing(message: str) -> str:
    return message[message.find("'") + 1 : message.rfind("'")]

def _render(
    env: Environment,
    text: str,
    variables: dict[str, Any],
) -> str:
    return env.from_string(str(text)).render(**variables)

def _render_or_prompt(
    env: Environment,
    text: str,
    variables: dict[str, Any],
    do_prompt: bool = True,
) -> str:
    try:
        return _render(env, text, variables)
    except UndefinedError as e:
        if do_prompt:
            name = _get_missing(e.message)
            value = input(f"[dirtem] {name}: ")
            variables[name] = value
            return _render_or_prompt(env, text, variables)
        raise e

def _pattern_match(
    path: Path,
    pattern_style: _PatternStyle,
    patterns: Iterable[str],
) -> bool:
    if pattern_style == _PatternStyle.GLOB:
        return any(map(path.match, patterns))
    elif pattern_style == _PatternStyle.REGEX:
        return any(re.match(p, str(path)) for p in patterns)
    else:
        raise TypeError("invalid pattern style")

'''
def _get_files(
    source: Path,
    patterns: Iterable[str],
    style: _PatternStyle,
    include: bool,
) -> Iterable[Path]:
    return (f for f in source.iterdir() if _pattern_match(f, style, include))
'''

def build(
    source: Path | str,
    destination: Path | str,
    options: dict[str, Any] | Path | str,
    **variables: Any,
) -> None:
    """
    Parameters
    ----------
    source
        The path to the template directory.
    
    destination
        The path to the directory with the rendered files. If this directory does not exist, it
        is created.
    
    options
        Configuration for the building process. This may be a ``dict`` or a path to a TOML file.
        Refer to <Configuration>_ in the docs to learn more.
    
    variables
        The variables to use within the template for jinja.
    """
    source = Path(source)#.resolve()
    destination = Path(destination)#.resolve()
    
    env = Environment(undefined = StrictUndefined)
    
    if isinstance(options, (Path, str)):
        with Path(options).open("rb") as f:
            options = tomllib.load(f)
    
    logger.info("reading configuration ...")
    
    variables = options.get("default-variables", dict()) | variables
    
    jinja_path_list = options.get("jinja", {}).get("select", [])
    jinja_mode_include = options.get("jinja", {}).get("select-mode", "include") == "include"
    jinja_do_prompt = options.get("jinja", {}).get("prompt-missing", True)
    fs_path_list = options.get("fs", {}).get("select", [])
    fs_mode_include = options.get("fs", {}).get("select-mode", "include") == "include"
    fs_pattern_style = _PatternStyle.from_string(options.get("fs", {}).get("pattern-style", "glob"))
    
    logger.info("copying paths ...")
    
    for path in source.rglob("*"):
        if _pattern_match(path, fs_pattern_style, fs_path_list) and not fs_mode_include:
            logger.debug("skipping path {path}")
            continue
        if path.is_dir():
            p = destination / Path(*takewhile(
                bool,
                _render_until_unnamed(
                    env = env,
                    it = _remove_parents(source, path),
                    variables = variables,
                    do_prompt = jinja_do_prompt
                )
            ))
            p.mkdir(exist_ok = True, parents = True)
            if p.exists():
                logger.info(f"created directory {path}")
            continue
        
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            rendered = path.read_bytes()
        else:
            is_jinja = False
            if text:
                line = text.splitlines()[0].strip()
                if pattern_isjinja.fullmatch(line):
                    is_jinja = True
                elif pattern_nojinja.fullmatch(line):
                    is_jinja = False
                else:
                    if jinja_mode_include:
                        is_jinja = str(path) in jinja_path_list
                    else:
                        is_jinja = str(path) not in jinja_path_list
            if is_jinja:
                logger.debug(f"rendering {path} content")
                rendered = _render_or_prompt(
                    env = env,
                    text = text,
                    variables = variables,
                    do_prompt = jinja_do_prompt,
                )
            else:
                rendered = text
        
        p = Path(*takewhile(bool, (
            _render_or_prompt(
                env = env,
                text = part,
                variables = variables,
                do_prompt = jinja_do_prompt,
            ) for part in _remove_parents(source, path)
        )))
        if (destination / p) == destination:
            continue
        
        dest = destination / p
        logger.info(f"copying file {dest}")
        Path(dest.parents[0]).mkdir(exist_ok = True, parents = True)
        dest.write_text(rendered)
    
    if (debug := options.get("debug")) is not None:
        if debug.get("generate-metadata-file", False):
            logger.debug("creating metadata file ...")
            metadata = {
                "built": datetime.now(),
                "dirtem-version": version("dirtem"),
            } | debug.get("metadata-add", dict())
            with (destination / ".dirtem-metadata.toml").open("wb") as f:
                tomli_w.dump(metadata, f)

