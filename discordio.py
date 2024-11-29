import os
import discord
from dotenv import load_dotenv
from answering import answer_question


class DiscordBot:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Bot configuration
        self.token = os.getenv('DISCORD_TOKEN')
        
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        
        # Create client with configured intents
        self.client = discord.Client(intents=intents)
        
        # Register event handlers
        self.client.event(self.on_ready)
        self.client.event(self.on_message)

    async def on_ready(self):
        """Callback when the bot is ready and connected."""
        print(f"{self.client.user} is now running")

    async def on_message(self, message):
        """Handle incoming messages."""
        # Ignore messages from the bot itself
        if message.author == self.client.user:
            return
        
        # Log message details
        username = str(message.author)
        user_message = message.content
        channel = str(message.channel)
        print(f"{username} said: '{user_message}' ({channel})")
        
        # Process message if it starts with a command
        await self.process_message(message, user_message)

    async def process_message(self, message, user_message):
        """Process and respond to messages."""
        if not user_message:
            print("Empty user message")
            return
        
        # Check for command prefix
        if user_message.startswith("!"):
            command = user_message[1:]
            response = await self.get_answer(command)
            await self.send_response(message, response)
    
    async def get_answer(self, user_message):
        """Generate a response to the user message."""
        fact = await answer_question(user_message)
        print(fact)
        if fact:
            return fact
        return "Dummy answer: " + user_message

    async def send_response(self, message, response):
        """Send response, splitting into chunks if necessary."""
        try:
            # Split response into chunks
            chunks = self.split_message(response)
            
            # Send each chunk
            for chunk in chunks:
                await message.channel.send(chunk)
        except Exception as e:
            print(f"Error sending message: {e}")

    def split_message(self, text, max_length=2000):
        """
        Splits text into chunks of max_length or less,
        using newline characters as split points if possible.
        """
        chunks = []
        while len(text) > max_length:
            # Find the last newline character within the max_length limit
            split_pos = text.rfind("\n", 0, max_length)
            if split_pos == -1:  # No newline found, split at max_length
                split_pos = max_length
            
            chunks.append(text[:split_pos].strip())
            text = text[split_pos:].lstrip()
        
        # Add the remaining text if not empty
        if text:
            chunks.append(text.strip())
        
        return chunks

    def run(self):
        """Start the bot with the loaded token."""
        if not self.token:
            raise ValueError("No Discord token found. Please set DISCORD_TOKEN in .env")
        
        self.client.run(self.token)

# Main execution
if __name__ == "__main__":
    bot = DiscordBot()
    bot.run()
