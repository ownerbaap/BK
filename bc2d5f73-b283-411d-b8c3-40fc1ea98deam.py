from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import random
import asyncio
import os

# Config
TOKEN = '8102352774:AAHgSq_CSRlXZFNwHvyoQbVFu4jMsNqUbSM'
ADMIN_ID = 6240986259

# Files
caption_file = 'caption.txt'
targets_file = 'targets.txt'
approved_users_file = 'approved_users.txt'

# Extreme Settings
MAX_CONCURRENT = 100  # Maximum concurrent messages
MAX_MESSAGES = 1000000  # Absolute maximum messages

# Word banks (optimized for speed)
VULGAR_COMBOS = [
    "maa ki chut {target}",
    "behenchod {target}",
    "teri {noun} {verb} dunga",
    "{target} madarchod",
    "lund lele {target}",
    "{target} randi ka bacha",
    "gaand mara {target}",
    "{target} chutmarike",
    "bhosdike {target}",
    "{target} teri maa randi"
]

# Global variables
is_sending = False
message_count = 0

def generate_insult(target):
    """Ultra-fast insult generation"""
    template = random.choice(VULGAR_COMBOS)
    return template.format(
        target=target,
        noun=random.choice(["maa", "behen", "gaand", "chut", "lund"]),
        verb=random.choice(["chod", "phod", "mara", "pel", "kaat"])
    )

def save_to_file(filename, text):
    """Optimized file saving"""
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"{text}\n")
        return True
    except:
        return False

def read_file(filename):
    """Optimized file reading"""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def clear_file(filename):
    """Clear file contents"""
    try:
        open(filename, 'w').close()
        return True
    except:
        return False

def remove_line(filename, text):
    """Remove specific line from file"""
    try:
        lines = read_file(filename)
        if text in lines:
            lines.remove(text)
            if clear_file(filename):
                for line in lines:
                    save_to_file(filename, line)
                return True
        return False
    except:
        return False

def is_user_approved(user_id):
    """Fast approval check"""
    approved = read_file(approved_users_file)
    return str(user_id) in approved

async def send_message(context, chat_id, text):
    """Fire-and-forget message sending"""
    global message_count
    try:
        await context.bot.send_message(chat_id=chat_id, text=text)
        message_count += 1
    except:
        pass

async def extreme_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ULTIMATE SPAM FUNCTION - MAXIMUM DESTRUCTION"""
    global is_sending, message_count
    
    if not is_user_approved(update.effective_user.id) and update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not approved to spam!")
        return
    
    targets = read_file(targets_file)
    if not targets:
        await update.message.reply_text("⚠️ No targets! Use /madarchod")
        return
    
    is_sending = True
    message_count = 0
    await update.message.reply_text("💣💥 **NUKE ACTIVATED! FULL POWER SPAMMING!** 💥💣")
    
    while is_sending and message_count < MAX_MESSAGES:
        tasks = []
        for _ in range(MAX_CONCURRENT):
            if not is_sending or message_count >= MAX_MESSAGES:
                break
                
            target = random.choice(targets)
            msg = generate_insult(target)
            task = asyncio.create_task(
                send_message(context, update.effective_chat.id, msg))
            tasks.append(task)
        
        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(0.01)  # Minimal delay
    
    is_sending = False
    await update.message.reply_text(f"☢️ **SPAM APOCALYPSE COMPLETE!** ☢️\nMessages sent: {message_count}")

async def stop_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Emergency stop"""
    global is_sending
    if not is_user_approved(update.effective_user.id) and update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not approved to use this command!")
        return
    
    is_sending = False
    await update.message.reply_text("🛑 **SPAM TERMINATED!**")

async def add_target(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add target"""
    if not is_user_approved(update.effective_user.id) and update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not approved to use this command!")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ Please provide target! Example: /madarchod username")
        return
    
    target = context.args[0]
    if not target.startswith('@'):
        target = f"@{target}"
    
    if save_to_file(targets_file, target):
        await update.message.reply_text(f"🎯 Target Added: {target}")
    else:
        await update.message.reply_text("⚠️ Failed to add target!")

async def remove_target(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove target"""
    if not is_user_approved(update.effective_user.id) and update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not approved to use this command!")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ Please provide target to remove! Example: /nikal username")
        return
    
    target = context.args[0]
    if not target.startswith('@'):
        target = f"@{target}"
    
    if remove_line(targets_file, target):
        await update.message.reply_text(f"❌ Target Removed: {target}")
    else:
        await update.message.reply_text("⚠️ Target not found or couldn't be removed!")

async def clear_targets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear all targets"""
    if not is_user_approved(update.effective_user.id) and update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not approved to use this command!")
        return
    
    if clear_file(targets_file):
        await update.message.reply_text("🧹 All targets cleared!")
    else:
        await update.message.reply_text("⚠️ Failed to clear targets!")

async def list_targets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all targets"""
    if not is_user_approved(update.effective_user.id) and update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not approved to use this command!")
        return
    
    targets = read_file(targets_file)
    if not targets:
        await update.message.reply_text("🎯 No targets saved!")
        return
    
    reply = "🎯 TARGETS:\n\n" + "\n".join(f"{i+1}. {t}" for i, t in enumerate(targets))
    await update.message.reply_text(reply)

async def approve_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Approve user"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 Only Admin can approve users!")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ Invalid User ID! Example: /approve 123456789")
        return
    
    user_id = context.args[0]
    if save_to_file(approved_users_file, user_id):
        await update.message.reply_text(f"✅ User Approved: {user_id}")
    else:
        await update.message.reply_text("⚠️ Failed to approve user!")

async def disapprove_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Disapprove user"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 Only Admin can disapprove users!")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ Invalid User ID! Example: /disapprove 123456789")
        return
    
    user_id = context.args[0]
    if remove_line(approved_users_file, user_id):
        await update.message.reply_text(f"❌ User Disapproved: {user_id}")
    else:
        await update.message.reply_text("⚠️ User not found or already disapproved!")

async def list_approved(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List approved users"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 Only Admin can view approved users!")
        return
    
    approved = read_file(approved_users_file)
    if not approved:
        await update.message.reply_text("📭 No approved users yet!")
        return
    
    reply = "✅ APPROVED USERS:\n\n" + "\n".join(f"{i+1}. {u}" for i, u in enumerate(approved))
    await update.message.reply_text(reply)

async def show_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot status"""
    if not is_user_approved(update.effective_user.id) and update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not approved to use this command!")
        return
    
    status = "🟢 RUNNING" if is_sending else "🔴 STOPPED"
    reply = (
        f"⚡ ULTRA SPAM BOT STATUS ⚡\n\n"
        f"Status: {status}\n"
        f"Messages sent: {message_count}\n"
        f"Targets loaded: {len(read_file(targets_file))}\n"
        f"Approved users: {len(read_file(approved_users_file))}\n"
        f"Max speed: {MAX_CONCURRENT} msg/batch"
    )
    await update.message.reply_text(reply)

def main():
    # Create files if they don't exist
    for file in [caption_file, targets_file, approved_users_file]:
        if not os.path.exists(file):
            open(file, 'w').close()
    
    print("💀 DEATH SPAM BOT ACTIVATED - READY FOR DESTRUCTION 💀")
    
    application = Application.builder().token(TOKEN).get_updates_without_proxy().build()
    
    # Command handlers
    application.add_handler(CommandHandler("chodo", extreme_spam))
    application.add_handler(CommandHandler("ruko", stop_spam))
    application.add_handler(CommandHandler("madarchod", add_target))
    application.add_handler(CommandHandler("nikal", remove_target))
    application.add_handler(CommandHandler("saaf", clear_targets))
    application.add_handler(CommandHandler("list", list_targets))
    application.add_handler(CommandHandler("approve", approve_user))
    application.add_handler(CommandHandler("disapprove", disapprove_user))
    application.add_handler(CommandHandler("approved_list", list_approved))
    application.add_handler(CommandHandler("status", show_status))
    
    application.run_polling()

if __name__ == '__main__':
    main()
