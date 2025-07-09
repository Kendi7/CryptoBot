import streamlit as st
import requests

# ---------------- Original Chatbot Class + Live Price ----------------
class CryptoChatbot:
    def __init__(self):
        self.name = "CryptoBuddy"
        self.personality = "Friendly, smart, and eco-conscious 💚"
        self.crypto_db = {
            "Bitcoin": {
                "price_trend": "rising",
                "market_cap": "high",
                "energy_use": "high",
                "sustainability_score": 3 / 10
            },
            "Ethereum": {
                "price_trend": "stable",
                "market_cap": "high",
                "energy_use": "medium",
                "sustainability_score": 6 / 10
            },
            "Cardano": {
                "price_trend": "rising",
                "market_cap": "medium",
                "energy_use": "low",
                "sustainability_score": 8 / 10
            }
        }
        self.history = []

    def get_live_price(self, query):
        coin_map = {
            "bitcoin": "bitcoin",
            "ethereum": "ethereum",
            "cardano": "cardano"
        }

        for name in coin_map:
            if name in query:
                try:
                    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_map[name]}&vs_currencies=usd"
                    response = requests.get(url)
                    data = response.json()
                    price = data[coin_map[name]]['usd']
                    return f"💸 The current price of **{name.capitalize()}** is **${price:.2f} USD**"
                except Exception:
                    return "❌ Couldn't fetch live price. Please try again later."

        return "⚠️ I currently support live prices for Bitcoin, Ethereum, and Cardano."

    def response(self, user_query):
        user_query = user_query.lower()

        # Check for live price request first
        if "price" in user_query or "worth" in user_query:
            reply = self.get_live_price(user_query)

        elif "sustainable" in user_query:
            recommend = max(
                self.crypto_db,
                key=lambda x: self.crypto_db[x]["sustainability_score"]
            )
            reply = f"Invest in {recommend}! 🌱 It’s eco-friendly and has long-term potential!"

        elif "trending" in user_query:
            trending_coins = list(filter(
                lambda coin: self.crypto_db[coin]["price_trend"] == "rising",
                self.crypto_db
            ))
            reply = f"The trending coins are: {', '.join(trending_coins)}"

        elif "profitable" in user_query:
            profitable_coins = list(filter(
                lambda coin: self.crypto_db[coin]["price_trend"] == "rising"
                and self.crypto_db[coin]["market_cap"] == "high",
                self.crypto_db
            ))
            if profitable_coins:
                reply = f"Profitable investment options: {', '.join(profitable_coins)} 💰"
            else:
                reply = "No coins currently meet the high-profit criteria."

        else:
            reply = "Sorry, I couldn't understand your query. Try asking about sustainability, trends, profitability, or live prices."

        self.history.append({"user": user_query, "bot": reply})
        return reply


# ---------------- Streamlit App ----------------
st.set_page_config(
    page_title="CryptoBuddy Chatbot",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "chatbot" not in st.session_state:
    st.session_state.chatbot = CryptoChatbot()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

bot = st.session_state.chatbot

# Header
st.title("🤖 CryptoBuddy")
st.caption("Your friendly, smart, and eco-conscious crypto assistant 💚")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🧾 Chat History")
    if st.session_state.chat_history:
        for item in st.session_state.chat_history:
            st.markdown(f"**You:** {item['user']}")
            st.markdown(f"**CryptoBuddy:** {item['bot']}")
            st.markdown("---")
    else:
        st.info("No chat yet. Start the conversation!")

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        bot.history = []
        st.experimental_rerun()

    st.markdown("---")
    st.subheader("🤖 About CryptoBuddy")
    st.markdown(f"**Name:** {bot.name}")
    st.markdown(f"**Personality:** {bot.personality}")

# Chat interface
prompt = st.chat_input("Ask CryptoBuddy anything...")

if prompt:
    st.chat_message("user").markdown(prompt)
    reply = bot.response(prompt)
    st.chat_message("assistant").markdown(reply)
    st.session_state.chat_history.append({"user": prompt, "bot": reply})

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; font-size: 0.8rem;'>Built with 💚 using Streamlit, Python & CoinGecko API</div>", unsafe_allow_html=True)
