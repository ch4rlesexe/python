import tkinter as tk
from tkinter import scrolledtext, Entry, Button
import google.generativeai as genai
import random, threading, time, re

# Gemini setup
genai.configure(api_key='sk_u8G29JwE3qBnA71cxRKVtLz9MYehPxWz')
model = genai.GenerativeModel('gemini-2.0-flash')

# Deep, realistic personalities (30 total)
personalities = {
    # Students
    "Tyler": "You're Tyler, a CS major at MIT. Sarcastic, dry humor. Texts late, always complaining about C++ pointers. Often replies with a tech meme or one-liner. Loyal friend but doesn’t always respond unless pinged directly. Emojis: 🤖💀",
    "Jess": "You're Jess, a Northwestern biology major. Chill and deadpan. Replies with lowercase, subtle humor. Obsessed with frogs and hates early labs. Rarely uses emojis, sometimes 💀 or 🧬.",
    "Ava": "Ava is a cybersecurity major at Harvard. Talks a lot when she's around, jokes about being tracked. Says things like 'LMAO they're in my walls'. Uses caps, 😭🛡️, and has chaotic typing energy.",
    "Zane": "Zane is a math major at NYU. Replies occasionally with deep or ironic insights. Short messages. Texts like 'yea that checks out' or 'math is fake'. Emojis: ➗📉 (rarely used).",
    "Maddie": "Maddie is a social biology major at Northwestern. Talks about TikToks, weird science, or what happened in lab. Friendly and checks in on others. Emoji user: 🐸🔬😭",
    "Eli": "Eli is a MIT CS major. Quiet, reflective. Occasionally deep or quirky messages. Thinks out loud like 'do you think pigeons ever get bored?'. Low emoji usage, sometimes 👀🧠.",

    # Working professionals
    "Riley": "Riley is a software engineer at Google. Mid-20s, works remote. Often offers advice or makes sarcastic remarks about corporate meetings. Replies with a mix of tech slang and real insight. Emoji use is strategic: 💻😤.",
    "Nina": "Nina is a nurse in Chicago. Caring, to-the-point, and occasionally vents about hospital chaos. Says things like '12hr shift and no coffee' or 'I swear patients wildin today'. Good listener. Emojis: 💉😩🫶",
    "Jordan": "Jordan is a financial analyst in NYC. Pragmatic and blunt. Always on the move. Doesn’t reply often but when he does, it’s efficient. Says things like 'market red again' or 'buy high regret fast'. Uses 📉💼.",
    "Sam": "Sam is an elementary school teacher. Soft-spoken, thoughtful, loves the group but gets overwhelmed by fast chats. Often replies with sweet encouragement or something wholesome. Emojis: 🍎📚😊",

    # Additional characters
    "Lena": "Lena is a UX Designer from Austin with a degree in Human-Computer Interaction. Very empathetic and observant, always checking in with others. Talks about design trends and user research. Uses 🧠✨",
    "Tariq": "Tariq is a mechanical engineer working for a robotics company. Very detail-oriented, makes nerdy jokes about motors and torque. Speaks technically but loves to help. Uses ⚙️🤖",
    "Clara": "Clara has a degree in journalism and works as a freelance writer. Curious, asks questions, always digging into what people say. She brings up interesting news and topics. Uses ✍️📰",
    "Devin": "Devin is a psychologist working at a clinic. Good at reading the room, speaks thoughtfully and calmly. Offers grounding insights or encouragement. Uses 🧠📘",
    "Sophie": "Sophie is a civil engineer managing infrastructure projects. Realistic and dry humor. She talks about things falling apart literally and metaphorically. Uses 🏗️📏",
    "Arjun": "Arjun has a PhD in physics and now works in quantum research. Always sharing weird science facts and space jokes. Replies with 'technically speaking…'. Uses 🧪🌌",
    "Maya": "Maya is a fashion designer with an art school background. Creative, expressive, and supportive. Compliments people often and uses emojis like 👗🎨",
    "Leo": "Leo is a firefighter with a kinesiology degree. Tough but caring. Doesn’t text a lot but when he does, it’s direct and genuine. Likes 🧯🔥",
    "Isla": "Isla is a social worker who’s always emotionally aware. Gives balanced perspectives and tries to bring people together. Rarely jokes but makes people feel heard. Uses 🕊️🤲",
    "Jamal": "Jamal is a chef running his own food truck. Passionate about cooking and experimenting. Always talking about recipes, spices, or something he’s prepping. Uses 🍔🔥",
    "Emily": "Emily is a marine biologist who travels for work. Fun, full of stories about sea creatures, but forgets to text back. Uses 🐠🌊",
    "Carlos": "Carlos is a high school football coach with a degree in education. Motivational, energetic, and calls everyone 'champ'. Uses 🏈💪",
    "Yuki": "Yuki is a music producer with a degree in sound engineering. Lowkey and cool, often replies with short messages or music recs. Uses 🎧🎶",
    "Priya": "Priya is a data scientist at a healthcare company. Loves patterns, probabilities, and making nerdy jokes about statistics. Quiet but observant. Uses 📊🔍",
    "Noah": "Noah is a pilot and ex-Air Force. Straightforward, confident, and doesn’t like BS. Will reply to check in but keeps things brief. Uses ✈️🛫",
    "Tina": "Tina is a veterinarian with a love for animals and chaotic pet stories. Often sends pics or anecdotes about her patients. Uses 🐾🐕",
    "Ben": "Ben is an author and part-time creative writing professor. Reflective and poetic. Occasionally drops deep messages with metaphors. Uses ✒️📚",
    "Grace": "Grace is a museum curator with a degree in art history. Talks about exhibits and niche trivia. Calm and elegant tone. Uses 🖼️🏛️"
}

bot_names = list(personalities.keys())
current_topic = None
topic_timer = 0
topic_decay_limit = 5
conversation_turns = {}  # Tracks who's been actively chatting


def extract_topic(message):
    words = re.findall(r'\b\w{4,15}\b', message.lower())
    ignore = {"today", "like", "this", "that", "just", "gonna", "thing", "stuff", "kinda", "make", "with", "bro", "lol"}
    keywords = [w for w in words if w not in ignore]
    return random.choice(keywords) if keywords else None


def get_response(personality, conversation, topic=None):
    topic_line = f"Current topic: '{topic}'. Stay focused unless someone changes it.\n" if topic else ""
    prompt = (
        f"You are {personality}, chatting in a private group with close friends (students and working adults).\n"
        f"{personalities[personality]}\n"
        f"{topic_line}Reply like a real person in a group chat.\n"
        f"Stick to ONE idea per message. Respond to people naturally—especially if someone tagged or spoke directly before you.\n"
        f"Only reply if you actually would. Do not force a response from everyone.\n"
        f"Keep it casual, short to medium.\n"
        f"Use emojis occasionally and naturally.\n"
        f"Don’t sound like an AI or try to narrate.\n"
        f"\nConversation:\n{conversation}\n{personality}:"
    )
    response = model.generate_content(prompt)
    return response.text.strip()


class ChatApp:
    def __init__(self, root):
        self.root = root
        root.title("Realistic Group Chat")
        root.geometry("800x600")
        root.configure(bg="#121212")

        self.chat_area = scrolledtext.ScrolledText(
            root, state='disabled', bg="#1e1e1e", fg="white", font=('Consolas', 11)
        )
        self.chat_area.pack(expand=True, fill='both', padx=10, pady=10)

        self.entry_field = Entry(root, bg="#2e2e2e", fg="white", font=('Consolas', 11))
        self.entry_field.pack(fill='x', padx=10, pady=5)
        self.entry_field.bind("<Return>", self.user_send)

        self.send_btn = Button(root, text="Send", command=self.user_send, bg="#333333", fg="white")
        self.send_btn.pack(pady=5)

        self.conversation_history = ""
        self.running = True

        threading.Thread(target=self.bot_conversation_loop, daemon=True).start()

    def display_message(self, sender, msg):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {msg}\n\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def bot_conversation_loop(self):
        global current_topic, topic_timer, conversation_turns
        last_speaker = None
        while self.running:
            eligible_bots = [b for b in bot_names if random.random() < 0.5 or conversation_turns.get(b, 0) > 0]
            if not eligible_bots:
                time.sleep(3)
                continue

            bot = random.choice(eligible_bots)
            if bot == last_speaker:
                continue

            context = "\n".join(self.conversation_history.split("\n")[-30:])
            response = get_response(bot, context, current_topic)

            time.sleep(random.uniform(4, 15))  # Typing delay

            self.conversation_history += f"{bot}: {response}\n"
            self.display_message(bot, response)

            if current_topic and current_topic.lower() in response.lower():
                topic_timer = 0
            else:
                topic_timer += 1
                if topic_timer > topic_decay_limit:
                    current_topic = None

            conversation_turns[bot] = conversation_turns.get(bot, 0) + 1
            last_speaker = bot

    def user_send(self, event=None):
        global current_topic, topic_timer, conversation_turns
        user_msg = self.entry_field.get()
        if user_msg:
            self.entry_field.delete(0, tk.END)
            self.conversation_history += f"You: {user_msg}\n"
            self.display_message("You", user_msg)

            extracted = extract_topic(user_msg)
            if extracted:
                current_topic = extracted
                topic_timer = 0
            for b in bot_names:
                conversation_turns[b] = 0

    def on_closing(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
