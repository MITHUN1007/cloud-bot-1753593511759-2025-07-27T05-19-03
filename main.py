from telethon import TelegramClient, events
import os
import openai

# Your API ID, hash and token
API_ID = int(os.environ.get("TELEGRAM_API_ID"))
API_HASH = os.environ.get("TELEGRAM_API_HASH")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Create a new Telegram client
client = TelegramClient('session', API_ID, API_HASH)
client.start(bot_token=BOT_TOKEN)

openai.api_key = OPENAI_API_KEY

async def generate_groq_reply(prompt):
    try:
        response = openai.chat.completions.create(
            model="groq-llama2-70b-32768",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100  # Adjust as needed
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating Groq reply: {e}")
        return "Sorry, I couldn't generate a response."

@client.on(events.NewMessage)
async def handle_message(event):
    if event.is_private:
        user_message = event.message.message
        print(f"Received message: {user_message}")
        groq_reply = await generate_groq_reply(user_message)
        await event.respond(groq_reply)

client.run_until_disconnected()