from functools import wraps

from setup.database import sessionmaker


def provide_session(commit: bool = True):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if "session" in kwargs:
                return await func(*args, **kwargs)

            async with sessionmaker() as session:
                try:
                    result = await func(*args, session=session, **kwargs)
                    if commit:
                        await session.commit()
                    return result
                except Exception:
                    await session.rollback()
                    raise

        return wrapper

    return decorator


async def get_db():
    async with sessionmaker() as session:
        yield session
