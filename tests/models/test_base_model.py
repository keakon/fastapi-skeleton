import pytest
from sqlalchemy import Column, Row
from sqlalchemy.sql import text

from app.clients.mysql import async_session
from app.models import BaseModel, all_is_instance


class Model(BaseModel, table=True):
    name: str


@pytest.mark.asyncio(scope='session')
class TestBaseModel:
    async def test_get_by_id(self):
        async with async_session() as session:
            await session.execute(text('TRUNCATE TABLE model'))

            model = await Model.get_by_id(session, 1)
            assert model is None

            session.add(Model(name='test'))
            await session.commit()

            model = await Model.get_by_id(session, 1)
            assert isinstance(model, Model)
            assert model.id == 1
            assert model.name == 'test'

            model = await Model.get_by_id(session, 1, for_update=True)
            assert isinstance(model, Model)
            assert model.id == 1
            assert model.name == 'test'

            model = await Model.get_by_id(session, 1, for_read=True)
            assert isinstance(model, Model)
            assert model.id == 1
            assert model.name == 'test'

            id = await Model.get_by_id(session, 1, Model.id)  # type: ignore
            assert id == 1

            name = await Model.get_by_id(session, 1, Model.name)  # type: ignore
            assert name == 'test'

            name = await Model.get_by_id(session, 1, Model.name, for_update=True)  # type: ignore
            assert name == 'test'

            name = await Model.get_by_id(session, 1, Model.name, for_read=True)  # type: ignore
            assert name == 'test'

            name = await Model.get_by_id(session, 1, text('name'))
            assert name == 'test'

            name = await Model.get_by_id(session, 1, Column('name'))
            assert name == 'test'

            row = await Model.get_by_id(session, 1, (Model.name,))
            assert isinstance(row, Row)
            assert row.name == 'test'
            assert row[0] == 'test'

            row = await Model.get_by_id(session, 1, [Model.name])
            assert isinstance(row, Row)
            assert row.name == 'test'
            assert row[0] == 'test'

            row = await Model.get_by_id(session, 1, (Model.id, Model.name))
            assert isinstance(row, Row)
            assert row.id == 1
            assert row[0] == 1
            assert row.name == 'test'
            assert row[1] == 'test'

    async def test_get_by_ids(self):
        async with async_session() as session:
            await session.execute(text('TRUNCATE TABLE model'))

            models = await Model.get_by_ids(session, (1, 2, 3))
            assert len(models) == 0

            session.add(Model(name='test'))
            session.add(Model(name='test2'))
            await session.commit()

            models = await Model.get_by_ids(session, (1, 2, 3))
            assert len(models) == 2
            assert all_is_instance(models, Model)
            model0, model1 = models
            assert model0.id == 1
            assert model0.name == 'test'
            assert model1.id == 2
            assert model1.name == 'test2'

            models = await Model.get_by_ids(session, [])
            assert len(models) == 0

            models = await Model.get_by_ids(session, [3, 4])
            assert len(models) == 0

            models = await Model.get_by_ids(session, [1, 2, 3], for_update=True)
            assert len(models) == 2
            assert all_is_instance(models, Model)
            model0, model1 = models
            assert model0.id == 1
            assert model0.name == 'test'
            assert model1.id == 2
            assert model1.name == 'test2'

            models = await Model.get_by_ids(session, [1, 2, 3], for_read=True)
            assert len(models) == 2
            assert all_is_instance(models, Model)
            model0, model1 = models
            assert model0.id == 1
            assert model0.name == 'test'
            assert model1.id == 2
            assert model1.name == 'test2'

            rows = await Model.get_by_ids(session, (1, 2, 3), Model.id)  # type: ignore
            assert len(rows) == 2
            row0, row1 = rows
            assert row0 == 1
            assert row1 == 2

            rows = await Model.get_by_ids(session, (1, 2, 3), Model.name)  # type: ignore
            assert len(rows) == 2
            row0, row1 = rows
            assert row0 == 'test'
            assert row1 == 'test2'

            rows = await Model.get_by_ids(session, (1, 2, 3), Model.name, for_update=True)  # type: ignore
            assert len(rows) == 2
            row0, row1 = rows
            assert row0 == 'test'
            assert row1 == 'test2'

            rows = await Model.get_by_ids(session, (1, 2, 3), Model.name, for_read=True)  # type: ignore
            assert len(rows) == 2
            row0, row1 = rows
            assert row0 == 'test'
            assert row1 == 'test2'

            rows = await Model.get_by_ids(session, (1, 2, 3), text('name'))
            assert len(rows) == 2
            row0, row1 = rows
            assert row0 == 'test'
            assert row1 == 'test2'

            rows = await Model.get_by_ids(session, (1, 2, 3), Column('name'))
            assert len(rows) == 2
            row0, row1 = rows
            assert row0 == 'test'
            assert row1 == 'test2'

            rows = await Model.get_by_ids(session, (1, 2, 3), (Model.name,))
            assert len(rows) == 2
            assert all_is_instance(rows, Row)
            row0, row1 = rows
            assert row0.name == 'test'
            assert row0[0] == 'test'
            assert row1.name == 'test2'
            assert row1[0] == 'test2'

            rows = await Model.get_by_ids(session, (1, 2, 3), [Model.name])
            assert len(rows) == 2
            assert all_is_instance(rows, Row)
            row0, row1 = rows
            assert row0.name == 'test'
            assert row0[0] == 'test'
            assert row1.name == 'test2'
            assert row1[0] == 'test2'

            rows = await Model.get_by_ids(session, (1, 2, 3), (Model.id, Model.name))
            assert len(rows) == 2
            assert all_is_instance(rows, Row)
            row0, row1 = rows
            assert row0.id == 1
            assert row0.name == 'test'
            assert row1.id == 2
            assert row1.name == 'test2'

    async def test_exsit(self):
        async with async_session() as session:
            await session.execute(text('TRUNCATE TABLE model'))

            assert not await Model.exsit(session, 1)

            session.add(Model(name='test'))
            await session.commit()
            assert await Model.exsit(session, 1)

    async def test_get_all(self):
        async with async_session() as session:
            await session.execute(text('TRUNCATE TABLE model'))

            models = await Model.get_all(session)
            assert len(models) == 0

            session.add(Model(name='test'))
            session.add(Model(name='test2'))
            await session.commit()

            models = await Model.get_all(session)
            assert len(models) == 2
            assert all_is_instance(models, Model)
            model0, model1 = models
            assert model0.id == 1
            assert model0.name == 'test'
            assert model1.id == 2
            assert model1.name == 'test2'

            models = await Model.get_all(session, for_update=True)
            assert len(models) == 2
            assert all_is_instance(models, Model)
            model0, model1 = models
            assert model0.id == 1
            assert model0.name == 'test'
            assert model1.id == 2
            assert model1.name == 'test2'

            models = await Model.get_all(session, for_read=True)
            assert len(models) == 2
            assert all_is_instance(models, Model)
            model0, model1 = models
            assert model0.id == 1
            assert model0.name == 'test'
            assert model1.id == 2
            assert model1.name == 'test2'

            rows = await Model.get_all(session, Model.id)  # type: ignore
            assert len(rows) == 2
            row0, row1 = rows
            assert row0 == 1
            assert row1 == 2

            rows = await Model.get_all(session, Model.name)  # type: ignore
            assert len(rows) == 2
            row0, row1 = rows
            assert row0 == 'test'
            assert row1 == 'test2'

            rows = await Model.get_all(session, Model.name, for_update=True)  # type: ignore
            assert len(rows) == 2
            row0, row1 = rows
            assert row0 == 'test'
            assert row1 == 'test2'

            rows = await Model.get_all(session, Model.name, for_read=True)  # type: ignore
            assert len(rows) == 2
            row0, row1 = rows
            assert row0 == 'test'
            assert row1 == 'test2'

            rows = await Model.get_all(session, (Model.name,))
            assert len(rows) == 2
            assert all_is_instance(rows, Row)
            row0, row1 = rows
            assert row0.name == 'test'
            assert row0[0] == 'test'
            assert row1.name == 'test2'
            assert row1[0] == 'test2'

            rows = await Model.get_all(session, [Model.name])
            assert len(rows) == 2
            assert all_is_instance(rows, Row)
            row0, row1 = rows
            assert row0.name == 'test'
            assert row0[0] == 'test'
            assert row1.name == 'test2'
            assert row1[0] == 'test2'

            rows = await Model.get_all(session, (Model.id, Model.name))
            assert len(rows) == 2
            assert all_is_instance(rows, Row)
            row0, row1 = rows
            assert row0.id == 1
            assert row0.name == 'test'
            assert row1.id == 2
            assert row1.name == 'test2'

    async def test_count_all(self):
        async with async_session() as session:
            await session.execute(text('TRUNCATE TABLE model'))

            count = await Model.count_all(session)
            assert count == 0

            session.add(Model(name='test'))
            session.add(Model(name='test2'))
            await session.commit()

            count = await Model.count_all(session)
            assert count == 2

    async def test_update_by_id(self):
        async with async_session() as session:
            await session.execute(text('TRUNCATE TABLE model'))

            count = await Model.update_by_id(session, 1, {'name': 'test2'})
            assert count == 0

            session.add(Model(name='test'))
            await session.commit()

            count = await Model.update_by_id(session, 1, {'name': 'test2'})
            assert count == 1
            name = await Model.get_by_id(session, 1, Model.name)  # type: ignore
            assert name == 'test2'

            count = await Model.update_by_id(session, 1, {Model.id.name: 2})  # type: ignore
            assert count == 1
            name = await Model.get_by_id(session, 2, Model.name)  # type: ignore
            assert name == 'test2'

    async def test_delete_by_id(self):
        async with async_session() as session:
            await session.execute(text('TRUNCATE TABLE model'))

            count = await Model.delete_by_id(session, 1)
            assert count == 0

            session.add(Model(name='test'))
            await session.commit()

            count = await Model.delete_by_id(session, 1)
            assert count == 1
            assert await Model.get_by_id(session, 1) is None

    async def test_delete_by_ids(self):
        async with async_session() as session:
            await session.execute(text('TRUNCATE TABLE model'))

            count = await Model.delete_by_ids(session, (1, 2))
            assert count == 0

            session.add(Model(name='test'))
            await session.commit()

            count = await Model.delete_by_ids(session, (1, 2))
            assert count == 1
            assert await Model.get_by_id(session, 1) is None

            session.add(Model(name='test2'))
            session.add(Model(name='test3'))
            session.add(Model(name='test4'))
            await session.commit()

            count = await Model.delete_by_ids(session, [1, 2, 4])
            assert count == 2
            assert await Model.get_by_id(session, 2) is None
            assert await Model.get_by_id(session, 3) is not None
            assert await Model.get_by_id(session, 4) is None

    async def test_insert(self):
        async with async_session() as session:
            await session.execute(text('TRUNCATE TABLE model'))

            row_id = await Model.insert(session, {'name': 'test'})
            assert row_id == 1
            name = await Model.get_by_id(session, 1, Model.name)  # type: ignore
            assert name == 'test'

            row_id = await Model.insert(session, {'id': 3, 'name': 'test3'})
            assert row_id == 3
            name = await Model.get_by_id(session, 3, Model.name)  # type: ignore
            assert name == 'test3'

    async def test_batch_insert(self):
        async with async_session() as session:
            await session.execute(text('TRUNCATE TABLE model'))

            count = await Model.batch_insert(session, [{'name': 'test'}, {'name': 'test2'}])
            assert count == 2

            models = await Model.get_all(session)
            assert len(models) == 2
            assert all_is_instance(models, Model)
            model0, model1 = models
            assert model0.id == 1
            assert model0.name == 'test'
            assert model1.id == 2
            assert model1.name == 'test2'

            count = await Model.batch_insert(session, [(None, 'test3'), (None, 'test4')])
            assert count == 2

            models = await Model.get_all(session)
            assert len(models) == 4
            assert all_is_instance(models, Model)
            model2, model3 = models[2:]
            assert model2.id == 3
            assert model2.name == 'test3'
            assert model3.id == 4
            assert model3.name == 'test4'
