"""缓存

支持

"""
import os
import sys
import pickle
import inspect
import heapq
import hashlib
from pathlib import Path
from multiprocessing import Lock
from collections import OrderedDict
from typing import Any, Dict, Type, Union, Callable, List
from vxutils import vxtime, to_timestring, to_timestamp, to_json, logger


__all__ = ["MissingCache", "CacheUnit", "DiskCacheUnit", "vxLRUCache"]
_ENDOFTIME = to_timestamp("2199-12-31 23:59:59")


class MissingCache(Exception):
    pass


class CacheUnit:
    _key = None
    _value = None
    _expired_dt = _ENDOFTIME

    def __init__(self, key: str, value: Any, expired_dt: float = None) -> None:
        self._key = key
        self._value = value
        self._expired_dt = to_timestamp(expired_dt or _ENDOFTIME)

    @property
    def key(self) -> str:
        return self._key

    @property
    def value(self) -> Any:
        return self._value

    @property
    def expired_dt(self) -> float:
        return self._expired_dt

    @property
    def size(self) -> float:
        return 1

    @property
    def is_expired(self) -> float:
        return self._expired_dt < vxtime.now()

    def __str__(self) -> str:
        return (
            f"< {self.__class__.__name__} key: {self._key} _value:"
            f" {self._value} has expired >"
            if self.is_expired
            else (
                f"< {self.__class__.__name__} key: {self._key} _value:"
                f" {self._value} will expired at: {to_timestring(self.expired_dt)} > "
            )
        )

    __repr__ = __str__

    def __getstate__(self) -> Dict:
        return {"key": self.key, "value": self.value, "expired_dt": self.expired_dt}

    def __setstate(self, state: Dict) -> None:
        self.__init__(**state)

    @classmethod
    def set_cache_params(cls, *args, **kwargs) -> None:
        pass

    @classmethod
    def init_cache(cls) -> OrderedDict:
        return OrderedDict()

    def clear(self) -> None:
        del self._value

    def __lt__(self, other: "CacheUnit") -> bool:
        return (self.expired_dt, self._value) > (other.expired_dt, other._value)

    def __gt__(self, other: "CacheUnit") -> bool:
        return (self.expired_dt, self._value) < (other.expired_dt, other._value)

    def __eq__(self, other: "CacheUnit") -> bool:
        return (self.expired_dt, self._value) == (other.expired_dt, other._value)

    def __hash__(self) -> int:
        return hash((self._value, self._expired_dt))


class DiskCacheUnit(CacheUnit):
    _path = Path.home().joinpath(".vxcache").absolute()

    def __init__(self, key: str, value: Any, expired_dt: float = 0) -> None:
        value_file = Path(self._path, f"{key}.dat")
        super().__init__(key, value_file.absolute(), expired_dt)
        self.value = value

    @property
    def value(self) -> Any:
        with open(self._value, "rb") as f:
            cache_obj = pickle.load(f)
            return cache_obj["value"]

    @value.setter
    def value(self, value: Any) -> None:
        with open(self._value, "wb") as fp:
            pickle.dump(
                {"key": self.key, "value": value, "expired_dt": self._expired_dt}, fp
            )

    @property
    def size(self) -> float:
        return self._value.stat().st_size

    @classmethod
    def set_cache_params(cls, cache_dir: Union[str, Path]) -> None:
        cls._path = Path(cache_dir)
        cls._path.mkdir(parents=True, exist_ok=True)
        logger.info(f"设置换成目录为: {cls._path}")

    @classmethod
    def init_cache(cls) -> OrderedDict:
        if not Path(cls._path).exists():
            Path(cls._path).mkdir(parents=True, exist_ok=True)
            return OrderedDict()

        cache_objs = []
        for value_file in cls._path.glob("*.dat"):
            with open(value_file, "rb") as fp:
                cache_params = pickle.load(fp)

            if (
                isinstance(cache_params, dict)
                and cache_params["expired_dt"] > vxtime.now()
            ):
                cache_objs.append(cls(**cache_params))
            else:
                logger.warning(f"cache_params error: {value_file} 删除")
                Path(value_file).unlink()

        return OrderedDict(
            {cache_obj.key: cache_obj for cache_obj in sorted(cache_objs)}
        )

    def clear(self) -> None:
        self._value.unlink(missing_ok=True)


class vxLRUCache:
    """Cache"""

    def __init__(
        self,
        size_limit: float = 0,
        unit_factory: Type[CacheUnit] = None,
    ):
        # self._lock = Lock()
        self.size_limit = size_limit * 1000  # M
        self._size = 0
        self._unit_factory = unit_factory or CacheUnit
        self._storage = OrderedDict()

        for key, cache_obj in self._unit_factory.init_cache().items():
            self.__setitem__(key, cache_obj)

    @property
    def storage(self) -> Dict:
        return {
            key: cache_obj
            for key, cache_obj in self._storage.items()
            if not cache_obj.is_expired
        }

    def keys(self) -> List[str]:
        # with self._lock:
        return [
            key for key, cache_obj in self._storage.items() if not cache_obj.is_expired
        ]

    def set(self, key, value, ttl=0) -> None:
        expired_dt = vxtime.now() + ttl if ttl > 0 else _ENDOFTIME
        cache_obj = (
            value
            if isinstance(value, CacheUnit)
            else self._unit_factory(key, value, expired_dt)
        )

        # with self._lock:
        self._adjust_size(key, cache_obj)
        self._storage[key] = cache_obj
        self._storage.move_to_end(key)

        if self.limited:
            # pop the oldest items beyond size limit
            while self._size > self.size_limit:
                self.popitem(last=False)

    def get(self, key, default=None) -> Any:
        cache_obj = self._storage.get(key, None)
        if cache_obj is None or cache_obj.is_expired:
            return default
        self._storage.move_to_end(key)
        return cache_obj.value

    def __setitem__(self, key, value):
        cache_obj = (
            value
            if isinstance(value, CacheUnit)
            else self._unit_factory(key, value, _ENDOFTIME)
        )
        # precalculate the size after od.__setitem__
        # with self._lock:
        self._adjust_size(key, cache_obj)
        self._storage[key] = cache_obj
        self._storage.move_to_end(key)

        if self.limited:
            # pop the oldest items beyond size limit
            while self._size > self.size_limit:
                self.popitem(last=False)

    def __getitem__(self, key):
        # with self._lock:
        cache_obj = self._storage.get(key, None)
        if cache_obj is None or cache_obj.is_expired:
            raise MissingCache(key)
        self._storage.move_to_end(key)
        return cache_obj.value

    def __contains__(self, key):
        # with self._lock:
        return key in self._storage and self._storage[key].is_expired is False

    def __len__(self):
        # with self._lock:
        return len(self._storage)

    def __repr__(self):
        storage_string = "".join(
            f"\t== {cache_obj}\n" for cache_obj in list(self.storage.values())[-5:]
        )
        return (
            f"{self.__class__.__name__}<size_limit:{self.size_limit if self.limited else 'no limit'} total_size:{self.total_size}>\n{storage_string}"
        )

    def set_limit_size(self, limit):
        self.size_limit = limit

    @property
    def limited(self):
        """whether memory cache is limited"""
        return self.size_limit > 0

    @property
    def total_size(self):
        return self._size

    def clear(self):
        # with self._lock:
        self._size = 0
        for cache_obj in self._storage.values():
            cache_obj.clear()
        self._storage.clear()

    def popitem(self, last=False):
        if len(self._storage) == 0:
            return None, None

        # with self._lock:
        k, cache_obj = self._storage.popitem(last=last)
        self._size -= cache_obj.size
        value = cache_obj.value
        cache_obj.clear()

        return k, value

    def pop(self, key, default=None):
        # with self._lock:
        cache_obj = self._storage.pop(key, None)
        if cache_obj is None:
            return default

        self._size -= cache_obj.size
        cache_obj.clear()
        return default if cache_obj.is_expired else cache_obj.value

    def _adjust_size(self, key, cache_obj):
        if key in self._storage:
            self._size -= self._storage[key].size

        self._size += cache_obj.size

    def __call__(self, func: Callable) -> Any:
        def wapper(*args, **kwargs):
            try:
                ba = inspect.signature(func).bind(*args, **kwargs)
                ba.apply_defaults()
                string = to_json(ba.arguments, sort_keys=True, default=str)
                key = hashlib.md5(string.encode()).hexdigest()
                retval = self.__getitem__(key)
            except MissingCache:
                retval = func(*args, **kwargs)
                self.__setitem__(key, retval)

            return retval

        return wapper

    def update(self, ttl=0, **kwargs):
        for key, value in kwargs.items():
            self.set(key, value, ttl)


diskcache = vxLRUCache(size_limit=1000, unit_factory=DiskCacheUnit)
