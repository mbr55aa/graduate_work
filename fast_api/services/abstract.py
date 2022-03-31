from abc import ABC, abstractmethod
from db.cache import MemoryCache
from db.storage import AbstractStorage
from models._base import OrjsonModel
from typing import Optional


class AbstractService(ABC):

    CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут

    name = None
    single_class = None

    def __init__(self, cache: MemoryCache, storage: AbstractStorage):
        self.cache = cache
        self.storage = storage

    @abstractmethod
    def get_by_id(self):
        pass

    @abstractmethod
    def get_list(self):
        pass

    async def _get_from_cache(self, entity_id: str) -> Optional[OrjsonModel]:
        data = await self.cache.get(entity_id)
        if not data:
            return []
        return self.single_class.parse_raw(data)

    async def _put_to_cache(self, entity: OrjsonModel):
        await self.cache.set(str(entity.uuid), entity.json(), self.CACHE_EXPIRE_IN_SECONDS)

    def _get_key(self, *args):
        key = (self.name, args)
        return str(key)
