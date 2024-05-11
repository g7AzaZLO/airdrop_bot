import asyncpg
import asyncio

async def main():
    # Connect to the database
    conn = await asyncpg.connect(user='user', password='password', database='testdb', host='127.0.0.1')

    # Create a table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id serial PRIMARY KEY,
            username text,
            age int
        )
    """)

    # Insert a user
    await conn.execute('INSERT INTO users(username, age) VALUES($1, $2)', 'johndoe', 30)

    # Select users
    users = await conn.fetch('SELECT * FROM users')
    for user in users:
        print(user)

    # Close the connection
    await conn.close()

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())