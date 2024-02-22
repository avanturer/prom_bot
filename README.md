# Discord prom_bot for online programming school

## Overview

This Discord bot is designed to efficiently manage and enhance the functionality of a Discord server. It includes features for reputation management, moderation, voice channel control, time tracking in voice channels, content filtering, and user data management.

## Features

### 1. Reputation Management
- **Command: +rep and -rep**
  - Admins can adjust a user's reputation using the +rep and -rep commands, influencing their role on the server.

    ```python
    @client.command()
    async def rep(ctx, member: discord.Member, amount: int):
        # Code to modify user's reputation
    ```

### 2. Moderation
- **Command: warn**
  - Admins can issue warnings to users for better moderation and behavior control.

    ```python
    @client.command()
    @commands.has_permissions(administrator=True)
    async def warn(ctx, member: discord.Member, *, reason=None):
        # Code to add a warning to a user
    ```

### 3. Voice Channel Management
- **Function: private_room**
  - The bot can create private voice channels for users, allowing them to communicate separately from other server members.

    ```python
    async def private_room(member, before, after):
        # Code to create a private voice channel
    ```

### 4. Time Management in Voice Channels
- **Event: on_voice_state_update**
  - The bot tracks the time users spend in voice channels and can assign roles or influence other bot functions based on this time.

    ```python
    @client.event
    async def on_voice_state_update(member, before, after):
        # Code to track time in voice channels
    ```

### 5. Content Filtering
- **Event: on_message**
  - The bot automatically deletes messages containing unwanted words, helping maintain a clean server environment.

    ```python
    @client.event
    async def on_message(message):
        # Code to check messages for unwanted words
    ```

### 6. User Data Management
- **Function: gt**
  - The bot stores user information such as level, experience, time in voice channels, and reputation in a database, providing personalized content and tracking user progress.

    ```python
    def gt(data: str = None, id: int = None):
        # Code to retrieve user data from the database
    ```

## Additional Commands

### 7. Role Management
- **Command: role**
  - Admins can grant or revoke specific roles from users based on their actions or achievements.

    ```python
    @client.command()
    async def role(ctx, member: discord.Member, role: discord.Role):
        # Code to assign or revoke a specific role to a member
    ```

### 8. Leaderboard
- **Command: leaderboard**
  - Users can view the top members on the server based on reputation, level, experience, etc.

    ```python
    @client.command()
    async def leaderboard(ctx, category: str = 'rep'):
        # Code to display the top members in the selected category
    ```

### 9. Prefix Setting
- **Command: setprefix**
  - Admins can change the bot's command prefix.

    ```python
    @client.command()
    @commands.has_permissions(administrator=True)
    async def setprefix(ctx, new_prefix: str):
        # Code to change the bot's command prefix
    ```

### 10. Report System
- **Command: report**
  - Users can report other members, providing admins with information about rule violations.

    ```python
    @client.command()
    async def report(ctx, member: discord.Member, reason: str):
        # Code to submit a report against a member
    ```

### 11. Poll Creation
- **Command: poll**
  - Users can create polls for server-wide decision making.

    ```python
    @client.command()
    async def poll(ctx, question: str, *options: str):
        # Code to create a poll
    ```

### Usage

Clone the repository and run the bot using the provided token. Customize the code and configuration files according to your server's requirements.

## Contributors

- Rodion Orkin (avanturer)
- 
## License

This project is licensed under the [License Name] License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Thanks to the [Discord.py](https://discordpy.readthedocs.io/) library.
- Feel free to contribute and make this bot even better!
