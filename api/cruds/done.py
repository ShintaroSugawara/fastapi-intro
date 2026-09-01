from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.task as task_model


async def get_done(
    db: AsyncSession,
    task_id: int
) -> Optional[task_model.Done]:
    result = await db.execute(
        select(task_model.Done).where(
            task_model.Done.id == task_id
        )
    )

    return result.scalar_one_or_none()


async def create_done(
    db: AsyncSession,
    task_id: int
) -> task_model.Done:
    done = task_model.Done(id=task_id)

    db.add(done)
    await db.commit()
    await db.refresh(done)

    return done


async def delete_done(
    db: AsyncSession,
    original: task_model.Done
) -> None:
    await db.delete(original)
    await db.commit()

