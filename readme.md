# Movie & Series Assistant Bot

## About the Bot

The **Movie & Series Assistant Bot** is designed to streamline the management and retrieval of movies or series videos and documents uploaded to a Telegram channel. It simplifies the process of storing and fetching media files with ease and efficiency.

## How It Works

1. **Uploading Media**:
   - Send videos or documents (movies/series) with their respective information in the caption (e.g., name, quality, season, episode, etc.).
   - You can send these to the bot personally or via a group/channel.
   - The bot automatically extracts the details from the caption or filename and saves them to the database.

2. **Fetching Media**:
   - Use the `/send <movie/series name>` command to request a specific movie or series.
   - The bot will ask for additional details like quality, season, episode, etc., if needed, and then send you the requested video.

3. **Additional Commands**:
   - Explore other commands by sending the `/help` command to the bot.

## Setup

### Environment Configuration

1. The `.env` file is already located in the `./env/` directory but is **empty**. 
2. Populate the `.env` file with the required details as outlined in `.env.format`. These include:
   - Bot API token
   - Database host
   - Database port
   - Database username
   - Database password
   - And other necessary fields.

### Authentication

1. The bot interacts only with authenticated users.
2. To specify authorized users, add their chat IDs to the `auth.json` file.
3. **How to Get Chat IDs**:
   - Send the `/help` command to the bot.
   - The bot will print a dictionary to the console, which includes your chat ID. Look for the key-value pair containing your `id` in this dictionary.

### Running the Bot

After configuring the `.env` file and `auth.json`, run the bot. It will be ready to manage and fetch your movie and series files efficiently.
