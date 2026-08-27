# TODO: сделать базовый репозиторий с CRUD

class BaseRepository:
    entity: Entity
    model: Model

    async def get(self, *args, **kwargs):
        return await db.get(self.entity, *args, **kwargs)

    async def create(self, *args, **kwargs):
        pass

    async def update(self, *args, **kwargs):
        pass

    async def delete(self, *args, **kwargs):
        pass

    async def list(self, *args, **kwargs):
        pass
