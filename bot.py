import os
import random
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,  # Changed from Filters to filters
    ContextTypes
)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration - UPDATE THESE WITH YOUR ACTUAL LINKS
CHANNEL_USERNAME = "@your_channel"  # Replace with your channel
GROUP_USERNAME = "@your_group"      # Replace with your group
TWITTER_USERNAME = "@your_twitter"  # Replace with your Twitter

# Sample Solana transaction IDs (replace with real ones from solscan.io)
TX_IDS = [
    "5g5Wt1dWj6n7vQ3XyY2Zb8cR9dA0sB1eC3fD4gE5hF6iG7jH8kI9lJ0kL1mM2nN",
    "3aB4cD5eF6gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ6aB7cD8eF9gH0iJ1kL2mN",
    "2kL3mN4oP5qR6sT7uV8wX9yZ0aB1cD2eF3gH4iJ5kL6mN7oP8qR9sT0uV"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message = (
        f"👋 Welcome {user.first_name}!\n\n"
        "📝 To participate in our airdrop:\n"
        f"1. Join our channel: {CHANNEL_USERNAME}\n"
        f"2. Join our group: {GROUP_USERNAME}\n"
        f"3. Follow us on Twitter: {TWITTER_USERNAME}\n\n"
        "💰 After completing these steps, send your Solana wallet address."
    )
    await update.message.reply_text(message)

async def handle_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    solana_address = update.message.text
    logger.info(f"Address received: {solana_address}")
    
    # Select random transaction ID
    tx_id = random.choice(TX_IDS)
    solscan_link = f"https://solscan.io/tx/{tx_id}"
    
    response = (
        "🎉 Congratulations!\n\n"
        "1000 SOL is on its way to your wallet!\n\n"
        f"🔗 Transaction: {solscan_link}\n\n"
        "Note: This is a test transaction. No real SOL has been sent."
    )
    
    await update.message.reply_text(response)

def main() -> None:
    # Using your test token directly
    TOKEN = "8005794306:AAGlYcLN0ZGk8ETTXCatdfwK4fFpZYpojjA"
    
    # Create Application
    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_address))  # Fixed filters usage

    # Webhook setup for Render
    RENDER_EXTERNAL_URL = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if RENDER_EXTERNAL_URL:
        PORT = int(os.environ.get('PORT', 8443))
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=f"https://{RENDER_EXTERNAL_URL}/{TOKEN}"
        )
        logger.info(f"Webhook set to: https://{RENDER_EXTERNAL_URL}/{TOKEN}")
    else:
        # Local polling
        application.run_polling()
        logger.info("Bot running in polling mode...")

if __name__ == '__main__':
    main()
