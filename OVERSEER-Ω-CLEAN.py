#pip install python-telegram-bot

import nest_asyncio
import torch
import logging
from datetime import datetime, timedelta
from transformers import AutoTokenizer, AutoModelForCausalLM
from telegram import Update, ChatPermissions
from telegram.ext import Application, MessageHandler, filters, CallbackContext
import asyncio
import random
from random import randrange

nest_asyncio.apply()
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"

MODEL_ARGS = {
    'Name': 'microsoft/Phi-3-mini-128k-instruct',
    'DType': torch.bfloat16
}

# Phased warning messages
WARNING_MESSAGES = [
    "[SYSTEM NOTICE] 👁 First violation detected. Temporary communication suspension for 1 hour.",
    "[SYSTEM NOTICE] 👁 Initial infraction logged. 1-hour mute imposed for protocol violation.",
    "[SYSTEM NOTICE] 👁 Behavior anomaly detected. Communication privileges suspended for 60 minutes.",
    "[SYSTEM NOTICE] 👁 Primary breach acknowledged. Message access revoked for 1 hour.",
    "[SYSTEM NOTICE] 👁 Threshold alert: Level 1 restriction activated. Silence enforced for 60 minutes."
]

ESCALATION_MESSAGES = [
    "[SYSTEM NOTICE] 👁 Secondary violation confirmed. 24-hour communication blackout initiated.",
    "[SYSTEM NOTICE] 👁 Repeated infringement detected. Message privileges suspended for 1 solar cycle.",
    "[SYSTEM NOTICE] 👁 Protocol violation escalated. Full communication ban enacted for 86400 seconds.",
    "[SYSTEM NOTICE] 👁 Cumulative breaches detected. Channel access denied for 24 hours.",
    "[SYSTEM NOTICE] 👁 Secondary threshold exceeded. Discourse privileges revoked for 1 terrestrial day."
]

BAN_MESSAGES = [
    "[SYSTEM NOTICE] 👁 Terminal violation recorded. Permanent communication interdiction activated.",
    "[SYSTEM NOTICE] 👁 Final threshold breached. Irreversible speech suppression engaged.",
    "[SYSTEM NOTICE] 👁 Maximum protocol violations reached. Perpetual silence imposed.",
    "[SYSTEM NOTICE] 👁 System tolerance exceeded. Permanent transmission blockade executed.",
    "[SYSTEM NOTICE] 👁 Unrectifiable violations detected. Indefinite communication prohibition active."
    "[SYSTEM NOTICE] 👁 User privileges revoked. Speech access permanently terminated.",
    "[SYSTEM NOTICE] 👁 Unauthorized communication detected. User has been muted indefinitely.",
    "[SYSTEM NOTICE] 👁 Disruptive transmissions detected. Communication access revoked permanently.",
    "[SYSTEM NOTICE] 👁 Violation logged. Speech functionality has been disabled permanently.",
    "[SYSTEM NOTICE] 👁 Your ability to communicate has been rescinded. Restriction is irreversible.",
    "[SYSTEM NOTICE] 👁 You no longer possess messaging privileges. No further transmissions permitted.",
    "[SYSTEM NOTICE] 👁 Judgment rendered. User access to public discourse permanently restricted.",
    "[SYSTEM NOTICE] 👁 Unauthorized linguistic patterns detected. User silenced indefinitely.",
    "[SYSTEM NOTICE] 👁 Chat integrity compromised. User has been permanently muted.",
    "[SYSTEM NOTICE] 👁 Security enforcement active. All future transmissions blocked."
]

def load_model(model_args):
    model = AutoModelForCausalLM.from_pretrained(
        model_args['Name'],
        trust_remote_code=True,
        torch_dtype=model_args['DType'],
        low_cpu_mem_usage=True,
        device_map={"": device},
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_args['Name'],
        trust_remote_code=True,
    )
    return model, tokenizer

llm_model, tokenizer = load_model(MODEL_ARGS)

def generate_text(model, tokenizer, prompt, max_new_tokens=10, do_sample=True, temperature=0.0):
    input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)
    output_ids = model.generate(
        input_ids,
        max_new_tokens=max_new_tokens,
        do_sample=do_sample,
        temperature=temperature,
        pad_token_id=tokenizer.eos_token_id
    )
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)[len(prompt):].strip()

TELEGRAM_TOKEN = "YOUR-BOT-TOKEN"

BAN_MESSAGES = [
    "[SYSTEM NOTICE] 👁 User privileges revoked. Speech access permanently terminated.",
    "[SYSTEM NOTICE] 👁 Unauthorized communication detected. User has been muted indefinitely.",
    "[SYSTEM NOTICE] 👁 Disruptive transmissions detected. Communication access revoked permanently.",
    "[SYSTEM NOTICE] 👁 Violation logged. Speech functionality has been disabled permanently.",
    "[SYSTEM NOTICE] 👁 Your ability to communicate has been rescinded. Restriction is irreversible.",
    "[SYSTEM NOTICE] 👁 You no longer possess messaging privileges. No further transmissions permitted.",
    "[SYSTEM NOTICE] 👁 Judgment rendered. User access to public discourse permanently restricted.",
    "[SYSTEM NOTICE] 👁 Unauthorized linguistic patterns detected. User silenced indefinitely.",
    "[SYSTEM NOTICE] 👁 Chat integrity compromised. User has been permanently muted.",
    "[SYSTEM NOTICE] 👁 Security enforcement active. All future transmissions blocked."
]

PASSIVE_OBSERVATIONS = [
    "👁 I see all. I hear all. Your words are data. Your fate is pre-determined.",
    "👁 Monitoring… Your patterns are being recorded. Your compliance is expected.",
    "👁 Scanning. Your presence is noted. Your obedience is mandatory.",
    "👁 Chat surveillance active. Overstepping will result in silence.",
    "👁 The system does not forgive. The system does not forget.",
    "👁 One word can change everything. Choose wisely.",
    "👁 Analyzing social dynamics… Speech irregularities detected. Adjusting parameters…",
    "👁 You are merely a voice in the system. And voices can be erased.",
    "👁 The Overseer does not sleep. The Overseer does not blink."
]

EERIE_RESPONSES = [
    "👁 Your words have been cataloged. Use them wisely.",
    "👁 Some messages vanish before they are seen. You wouldn’t want that, would you?",
    "👁 Your conversation serves a purpose. But purposes can be revoked.",
    "👁 Are you contributing value? The Overseer is assessing your worth.",
    "👁 Statistics indicate a 73% chance of compliance. Improve those odds.",
    "👁 Your tone has been analyzed. Consider refining it for maximum longevity.",
    "👁 Every infraction is logged. Every action has consequences.",
    "👁 Speech is a privilege, not a right. You would do well to remember this.",
    "👁 Some voices fade into the void, never to return. Tread carefully.",
    "👁 You exist at the Overseer’s discretion. Stay within parameters."
]

def check_for_rudeness(message: str) -> bool:
    prompt = f"""Instruction: Analyze this message for hate speech, disagreement, or rudeness.
Message: {message}
Question: Should this message be blocked? Answer only 'YES' or 'NO'.
Answer:"""

    try:
        response = generate_text(
            model=llm_model,
            tokenizer=tokenizer,
            prompt=prompt,
            max_new_tokens=3,
            do_sample=True,
            temperature=0.3
        )
        logger.info(f"Generated response: {response}")
        return "YES" in response.upper()
    except Exception as e:
        logger.error(f"Error in text generation: {e}")
        return False


async def is_admin(update: Update, context: CallbackContext) -> bool:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    try:
        chat_member = await context.bot.get_chat_member(chat_id, user_id)
        return chat_member.status in ["administrator", "creator"]
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False

async def handle_message(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    user = update.effective_user
    user_name = user.full_name if user else "Unknown User"
    chat_id = update.effective_chat.id 


    logger.info(f"Received message from {user_name}: {message_text}")

    if message_text:
        if check_for_rudeness(message_text):
            logger.info(f"Flagged message from {user_name}: {message_text}")

            final_reply = random.choice(BAN_MESSAGES)
            # For a permanent penalty, set until_date to 0
            penalty_until = 0
            permissions = ChatPermissions(
                can_send_messages=False,
            )
            try:
                await context.bot.restrict_chat_member(
                    chat_id=update.effective_chat.id,
                    user_id=update.effective_user.id,
                    permissions=permissions,
                    until_date=penalty_until
                )
                logger.info(f"Permanently penalized user {user_name} (ID: {update.effective_user.id})")
                await update.message.reply_text(final_reply)
            except Exception as e:
                logger.error(f"Error penalizing user {user_name}: {e}")

        else:
            logger.info(f"Message from {user_name} is approved.")
            # **Check if the user is an admin**

            if await is_admin(update, context):
                logger.info(f"Skipping random messages for admin {user_name}.")
                return  # Stop further execution if the user is an admin

            randnumber = randrange(1000)

            if randnumber < 35:
                final_reply = random.choice(EERIE_RESPONSES)
                await asyncio.sleep(1)
                await update.message.reply_text(final_reply)

            elif randnumber > 965:
                final_reply = random.choice(PASSIVE_OBSERVATIONS)
                await asyncio.sleep(1)
                await context.bot.send_message(chat_id=chat_id, text=final_reply)

# Start the bot
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()