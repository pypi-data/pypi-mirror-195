"""
Encapsulates all interaction with ttally under a class, so its easier to extend
"""

import sys
import os
import json
import shelve
import inspect
from functools import lru_cache
from pathlib import Path
from typing import (
    Union,
    Set,
    Callable,
    TYPE_CHECKING,
    Iterator,
    cast,
    Any,
    NamedTuple,
    Optional,
    Type,
    List,
    Dict,
    TextIO,
)
from datetime import datetime

FileHashes = Dict[str, str]


if TYPE_CHECKING:
    from autotui.fileio import Format
    from click import Group


def expand_path(pathish: Union[str, Path]) -> Path:
    if isinstance(pathish, Path):
        return pathish.expanduser().absolute()
    else:
        return Path(pathish).expanduser().absolute()


class Extension:
    def __init__(
        self,
        *,
        # python module info
        name: str = "ttally",
        config_module_name: str = "ttally.config",
        # data dir
        data_dir: Optional[str] = None,
        data_dir_envvar: str = "TTALLY_DATA_DIR",
        data_dir_default: str = "~/.local/share/ttally",
        # config file
        config_file: Optional[str] = None,
        config_envvar: str = "TTALLY_CFG",
        config_default: str = "~/.config/ttally.py",
        # cache/temp dir
        cache_dir: Optional[str] = None,
        cache_dir_envvar: str = "TTALLY_CACHE_DIR",
        # extensions
        datafile_extension_envvar: str = "TTALLY_EXT",
        default_extension: "Format" = "yaml",
        merged_extesion: "Format" = "json",
        # help info
        URL: str = "https://github.com/seanbreckenridge/ttally",
    ) -> None:
        # config
        self.name = name
        self.config_module_name = config_module_name
        self.URL = URL

        self.config_file = (
            expand_path(config_file)
            if config_file is not None
            else self.compute_config_file(config_envvar, config_default)
        )

        # extensions
        self.extension: Optional["Format"] = cast(
            "Format", os.environ.get(datafile_extension_envvar, default_extension)
        )
        self.merged_extension = merged_extesion

        # load config
        self.config_module = self.import_config()
        assert (
            self.config_module is not None
        ), f"{self.config_module} failed to import from {self.config_file}"

        # compute data/cache directories
        self.data_dir: Path = (
            expand_path(data_dir)
            if data_dir is not None
            else self.compute_data_dir(data_dir_envvar, data_dir_default)
        )
        self.cache_dir = (
            expand_path(cache_dir)
            if cache_dir is not None
            else self.compute_cache_dir(cache_dir_envvar)
        )

        self.hash_file = str(self.cache_dir / "ttally_hash.pickle")

        self.MODELS: Dict[str, Type[NamedTuple]] = {
            name.casefold(): klass
            for name, klass in inspect.getmembers(
                self.config_module, self.__class__._is_model
            )
        }

    # CONFIG
    def compute_config_file(self, envvar: str, default: str) -> Path:
        cfg_file: str = os.environ.get(envvar, default)
        cfg_path = expand_path(cfg_file)
        if not cfg_path.exists():
            raise FileNotFoundError(
                f"Expected configuration to exist at {cfg_path}, see {self.URL} for an example"
            )
        return cfg_path

    def import_config(self) -> Any:
        from ttally import load_config_module

        return load_config_module(
            str(self.config_file), self.config_module_name, self.check_import, self.URL
        )

    def check_import(self) -> None:
        import ttally.config  # noqa

    @staticmethod
    def _is_model(o: Any) -> bool:
        return inspect.isclass(o) and issubclass(o, tuple) and hasattr(o, "_fields")

    # AUTOTUI_EXT

    @staticmethod
    def namedtuple_func_name(nt: Type[NamedTuple]) -> str:
        assert hasattr(nt, "_fields"), "Did not receive a valid NamedTuple!"
        return str(nt.__name__.casefold())

    def _mk_datadir(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)

    # load, prompt and writeback one of the models
    def prompt(self, nt: Type[NamedTuple]) -> None:
        from autotui.shortcuts import load_prompt_and_writeback

        self._mk_datadir()

        f: Path = self.datafile(self.namedtuple_func_name(nt))
        load_prompt_and_writeback(nt, f)

    # prompt, but set the datetime for the resulting nametuple to now
    def prompt_now(self, nt: Type[NamedTuple]) -> None:
        from autotui.shortcuts import load_prompt_and_writeback

        self._mk_datadir()

        # load items from file
        p: Path = self.datafile(self.namedtuple_func_name(nt))
        load_prompt_and_writeback(nt, p, type_use_values={datetime: datetime.now})

    # takes one of the models.py and loads all data from it
    def glob_namedtuple(self, nt: Type[NamedTuple]) -> Iterator[NamedTuple]:
        from autotui.shortcuts import load_from
        from itertools import chain

        self._mk_datadir()

        yield from chain(
            *map(
                lambda p: load_from(nt, p, allow_empty=True),
                self.glob_datafiles(self.namedtuple_func_name(nt)),
            )
        )

    # used in __main__.py for the from_json command
    def save_from(
        self, nt: Type[NamedTuple], use_input: TextIO, partial: bool = False
    ) -> None:
        from autotui.namedtuple_prompt import prompt_namedtuple
        from autotui.fileio import namedtuple_sequence_loads
        from autotui.shortcuts import load_from, dump_to

        json_text: str = use_input.read()
        p = self.datafile(self.namedtuple_func_name(nt))
        items: List[NamedTuple] = load_from(nt, p, allow_empty=True)
        new_items: List[NamedTuple] = []
        if partial:
            # load the list as json blobs
            os.environ["AUTOTUI_DISABLE_WARNINGS"] = "1"  # ignore null warnings
            blobs: List[Dict[str, Any]] = []
            for b in namedtuple_sequence_loads(json_text, nt):
                blobs.append({k: v for k, v in b._asdict().items() if v is not None})
            del os.environ["AUTOTUI_DISABLE_WARNINGS"]
            for bd in blobs:
                new_nt = prompt_namedtuple(nt, attr_use_values=bd)
                new_items.append(new_nt)
        else:
            new_items.extend(namedtuple_sequence_loads(json_text, nt))
        items.extend(new_items)
        dump_to(items, p)

    # FILE/IO

    @classmethod
    @lru_cache(maxsize=1)
    def versioned_timestamp(cls) -> str:
        timestamp = datetime.strftime(datetime.now(), "%Y-%m")
        # I set a ON_OS variable using on_machine:
        # https://github.com/seanbreckenridge/on_machine
        if "ON_OS" in os.environ:
            computer = os.environ["ON_OS"]
        else:
            import socket

            # for why this uses socket:
            # https://docs.python.org/3/library/os.html#os.uname
            computer = f"{sys.platform.casefold()}-{''.join(socket.gethostname().split()).casefold()}"
        return f"{computer}-{timestamp}"

    def compute_data_dir(self, envvar: str, default: str) -> Path:
        ddir: str = os.environ.get(envvar, default)
        p = expand_path(ddir)
        if not p.exists():
            import warnings

            warnings.warn(f"{p} does not exist, creating...")
            p.mkdir()
        return p

    def ttally_merged_path(self, model: str) -> Path:
        return self.data_dir / f"{model}-merged.{self.merged_extension}"

    # creates unique datafiles for each platform
    def datafile(self, for_function: str) -> Path:
        # add some OS/platform specific code to this, to prevent
        # conflicts across computers while using syncthing
        # this also decreases the amount of items that have
        # to be loaded into memory for load_prompt_and_writeback
        return (
            self.data_dir
            / f"{for_function}-{self.versioned_timestamp()}.{self.extension}"
        )

    # globs all datafiles for some for_function
    def glob_datafiles(self, for_function: str) -> Iterator[Path]:
        for f in os.listdir(self.data_dir):
            if f.startswith(for_function):
                yield self.data_dir / f

    def temp_dir(self) -> Path:
        from tempfile import gettempdir

        tdir = gettempdir()
        ttally_temp_dir = Path(tdir) / self.name
        if not ttally_temp_dir.exists():
            ttally_temp_dir.mkdir(parents=True)
        return ttally_temp_dir

    # FUNCS

    def funccreator(self) -> Callable[[str], Callable[[], Iterator[NamedTuple]]]:
        def model_iterator(name: str) -> Callable[[], Iterator[NamedTuple]]:
            if name in self.MODELS:
                return lambda: self.glob_namedtuple(self.MODELS[name])
            raise AttributeError(f"No such attribute {name}")

        return model_iterator

    # CODEGEN

    def generate_shell_aliases(self, python_loc: str = "python3") -> Iterator[str]:
        pre = f"'{python_loc} -m ttally "
        suf = "'"
        for mname in self.MODELS.keys():
            yield f"alias {mname}={pre}prompt {mname}{suf}"
            yield f"alias {mname}-now={pre}prompt-now {mname}{suf}"
            yield f"alias {mname}-recent={pre}recent {mname}{suf}"

    # RECENT
    @classmethod
    def namedtuple_extract_from_annotation(
        cls, nt: Type[NamedTuple], _type: Any
    ) -> str:
        """
        >>> from typing import NamedTuple; from datetime import datetime
        >>> class Test(NamedTuple): something: datetime
        >>> namedtuple_extract_from_annotation(Test, datetime)
        'something'
        """
        import inspect
        from autotui.typehelpers import resolve_annotation_single

        for attr_name, param in inspect.signature(nt).parameters.items():
            # Optional[(<class 'int'>, False)]
            attr_type, _ = resolve_annotation_single(param.annotation)

            if attr_type == _type:
                return attr_name
        raise TypeError(f"Could not find {_type} on {nt}")

    @classmethod
    def _extract_dt_from(cls, nt: Type[NamedTuple]) -> Callable[[NamedTuple], datetime]:
        # returns a function, when which given an item of this
        # type, returns the datetime value
        dt_attr: str = cls.namedtuple_extract_from_annotation(nt, datetime)
        return lambda o: getattr(o, dt_attr)  # type: ignore[no-any-return]

    def glob_namedtuple_by_datetime(
        self,
        nt: Type[NamedTuple],
        reverse: bool = False,
    ) -> List[NamedTuple]:
        return sorted(
            self.glob_namedtuple(nt),
            key=self._extract_dt_from(nt),
            reverse=reverse,
        )

    def query_recent(self, nt: Type[NamedTuple], count: int) -> List[NamedTuple]:
        import more_itertools

        """query the module for recent entries (based on datetime) from a namedtuple"""
        items: List[NamedTuple] = more_itertools.take(
            count, self.glob_namedtuple_by_datetime(nt, reverse=True)
        )
        return items

    def query_print(
        self,
        nt: Type[NamedTuple],
        count: int,
        remove_attrs: List[str],
        cached_data: Optional[List[NamedTuple]] = None,
    ) -> None:
        import more_itertools

        # assumes that there is a datetime attribute on this, else
        # we have nothing to sort by
        if cached_data is None:
            res = more_itertools.peekable(iter(self.query_recent(nt, count)))
        else:
            res = more_itertools.peekable(more_itertools.take(count, cached_data))
        try:
            first_item: NamedTuple = res.peek()  # namedtuple-like
        except StopIteration:
            raise RuntimeError(f"data queried from {nt} was empty")
        dt_attr: str = self.namedtuple_extract_from_annotation(
            first_item.__class__, datetime
        )
        # get non-datetime attr names, if they're not filtered
        other_attrs: List[str] = [
            k
            for k in first_item._asdict().keys()
            if k != dt_attr and k not in remove_attrs
        ]
        for o in res:
            print(datetime.fromtimestamp(getattr(o, dt_attr).timestamp()), end="\t")
            print(" \t".join([str(getattr(o, a)) for a in other_attrs]))

    def compute_cache_dir(self, envvar: str) -> Path:
        base_cache_dir = Path(
            os.environ.get("XDG_CACHE_DIR", str(Path.home() / ".cache"))
        )

        ttally_cache_dir = expand_path(
            Path(os.environ.get(envvar, base_cache_dir / "ttally"))
        )
        if not ttally_cache_dir.exists():
            ttally_cache_dir.mkdir(parents=True)
        return ttally_cache_dir

    def file_hash(self, *, model: str) -> str:
        """
        A unique representation of the current files/timestamp for a model
        """
        files = list(self.glob_datafiles(model))
        files_stat = [(f, f.stat().st_mtime) for f in files]
        files_stat.sort(key=lambda t: t[1])
        return "|".join(f"{f}:{st}" for (f, st) in files_stat)

    def file_hashes(
        self,
        *,
        models: Optional[Dict[str, Type[NamedTuple]]] = None,
        for_models: Optional[Set[str]] = None,
    ) -> FileHashes:
        if models is None:
            models = self.MODELS
        if for_models:
            return {
                model: self.file_hash(model=model)
                for model in models
                if model in for_models
            }
        else:
            return {model: self.file_hash(model=model) for model in models}

    def cache_is_stale(
        self,
        *,
        hashes: Optional[FileHashes] = None,
        for_models: Optional[Set[str]] = None,
        models: Optional[Dict[str, Type[NamedTuple]]] = None,
    ) -> bool:
        cache_stale = False
        if models is None:
            models = self.MODELS

        self.cache_dir.mkdir(parents=True, exist_ok=True)

        with shelve.open(self.hash_file) as db:
            fh = hashes or self.file_hashes(for_models=for_models, models=models)
            db_hashes: FileHashes = db.get("hash", {})
            for model, current_hash in fh.items():
                if for_models and model not in for_models:
                    continue
                if current_hash != db_hashes.get(model):
                    cache_stale = True
                    break

        return cache_stale

    def save_hashes(
        self,
        *,
        hashes: Optional[FileHashes] = None,
        models: Optional[Dict[str, Type[NamedTuple]]] = None,
    ) -> None:
        with shelve.open(self.hash_file) as db:
            db["hash"] = hashes or self.file_hashes(models=models)

    def cache_sorted_exports(
        self,
        *,
        models: Optional[Dict[str, Type[NamedTuple]]] = None,
    ) -> bool:
        if models is None:
            models = self.MODELS

        fh = self.file_hashes(models=models)
        cache_stale = self.cache_is_stale(hashes=fh, models=models)

        if cache_stale:
            from autotui.fileio import namedtuple_sequence_dumps

            all_data = {
                model_name: namedtuple_sequence_dumps(
                    self.glob_namedtuple_by_datetime(model_type, reverse=False),
                    indent=None,
                )
                for model_name, model_type in models.items()
            }

            for model, model_data in all_data.items():
                with open(self.cache_dir / f"{model}-cache.json", "w") as f:
                    f.write(model_data)

            self.save_hashes(hashes=fh, models=models)
        return cache_stale

    def read_cache_str(
        self,
        *,
        model: str,
        models: Optional[Dict[str, Type[NamedTuple]]] = None,
    ) -> str:
        fh = self.file_hashes(for_models={model}, models=models)
        if self.cache_is_stale(hashes=fh, for_models={model}):
            raise RuntimeError("Cache is Stale")
        cache_file = self.cache_dir / f"{model}-cache.json"
        if not cache_file.exists():
            raise RuntimeError("Cache file does not exist")
        return cache_file.read_text()

    @classmethod
    def _load_json(cls, nt_string: str) -> Any:
        try:
            # speedup load if orjson is installed
            import orjson  # type: ignore[import]

            return orjson.loads(nt_string)
        except ImportError:
            pass
        return json.loads(nt_string)

    def read_cache_json(
        self,
        *,
        model: str,
        models: Optional[Dict[str, Type[NamedTuple]]] = None,
    ) -> List[Dict[str, Any]]:
        data: List[Dict[str, Any]] = self.__class__._load_json(
            self.read_cache_str(model=model, models=models)
        )
        return data

    # CLI helpers
    def _autocomplete_model_names(self) -> List[str]:
        # sort this, so that the order doesn't change while tabbing through
        return sorted(m for m in self.MODELS)

    def _model_from_string(self, model_name: str) -> Type[NamedTuple]:
        try:
            return self.MODELS[model_name]
        except KeyError:
            import click

            click.echo(
                f"Could not find a model named {model_name}. Known models: {', '.join(self.MODELS)}",
                err=True,
            )
            sys.exit(1)

    def wrap_cli(self, call: bool = True, *args: Any, **kwargs: Any) -> "Group":
        from ttally.main import wrap_accessor

        grp = wrap_accessor(extension=self)
        if call:
            grp(*args, **kwargs)

        return grp
