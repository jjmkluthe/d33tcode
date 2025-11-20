"""
    This is used as part of the setup for the example database.
    
    In the SQL seed file, all passwords are set to a simple string.
    
    However, in practice they should all be hashed securely. This script creates and insecure "password123" passowrd
    for each user and then hashes it securely in the database.
    
    In practice, whenever a new user is created we would also set the field "update_password" to true, to signal that the user
    must set a new password.
    
    For the example database that step will be skipped.
 """

import asyncio
from sqlalchemy import select

from config.session import AsyncSessionLocal
from auth.security import hash_password
from backend.models.app_user import AppUser


async def main():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(AppUser))
        users = result.scalars().all()

        for user in users:
            raw_password = "password123"
            user.password = hash_password(raw_password)
            print(f"Set password for {user.username!r} to {raw_password!r}")

        await session.commit()


# allows this to be run when directly called. This file is not intended for importing
if __name__ == "__main__":
    asyncio.run(main())