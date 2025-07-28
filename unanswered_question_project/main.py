import json
import pandas as pd
from transformers import pipeline

# Load the sentiment model
sentiment_pipeline = pipeline("sentiment-analysis", model="savasy/bert-base-turkish-sentiment-cased")

# Load the JSON chat data
with open("unanswered_question_project/last-500-conversation-dugunbuketi.json", "r", encoding="utf-8") as file:
    conversations = json.load(file)

results = []

def detect_category(text):
    if any(word in text for word in ["mekan", "salon", "kır düğünü", "kapalı alan", "açık alan"]):
        return "Mekan"
    elif any(word in text for word in ["gelinlik", "abiye", "elbis", "kaftan"]):
        return "Gelinlik"
    elif any(word in text for word in ["fotoğraf", "çekim", "dış çekim", "poz"]):
        return "Fotoğrafçı"
    elif any(word in text for word in ["organizasyon", "süsleme", "dekorasyon"]):
        return "Organizasyon"
    elif any(word in text for word in ["müzik", "dj", "orkestra"]):
        return "Müzik"
    else:
        return "Diğer"

def detect_intent(text):
    if any(word in text for word in ["mekan", "salon", "kapalı alan", "kır düğünü", "açık alan"]):
        return "Mekan arıyor"
    elif any(word in text for word in ["fotoğraf", "çekim", "dış çekim", "stüdyo"]):
        return "Fotoğrafçı arıyor"
    elif any(word in text for word in ["fiyat", "ne kadar", "kaç kişi", "tarih", "ücret", "bütçe", "ne zaman"]):
        return "Bilgi soruyor"
    elif any(word in text for word in ["gelinlik", "abiye", "kaftan", "aksesuar"]):
        return "Ürün arıyor"
    elif any(word in text for word in ["yardımcı olur musunuz", "öneri", "bilgi alabilir miyim"]):
        return "Genel danışma"
    else:
        return "Belirsiz"

for conv in conversations:
    messages = conv.get("messages", [])
    
    for i, msg in enumerate(messages):
        sender_id = msg.get("sender_id")
        content = msg.get("content", {})

        if isinstance(content, dict):
            text = content.get("text", "")
        else:
            text = ""

        if not sender_id or not text or not isinstance(text, str) or not text.strip():
            continue

        answered = "No"
        for j in range(i+1, len(messages)):
            reply = messages[j]
            if reply.get("sender_id") and reply["sender_id"] != sender_id:
                answered = "Yes"
                break

        text_lower = text.lower()

        # Use transformer for sentiment
        try:
            result = sentiment_pipeline(text)
            sentiment = result[0]["label"]
        except:
            sentiment = "Neutral"

        category = detect_category(text_lower)
        intent = detect_intent(text_lower)

        results.append({
            "conversation_id": conv.get("conversation_id"),
            "message": text,
            "answered": answered,
            "sentiment": sentiment,
            "category": category,
            "intent": intent
        })


# Export to CSV
df = pd.DataFrame(results)
df.to_csv("C:\\Users\\Emre\\Desktop\\python\\unanswered_question_project\\output.csv", index=False, encoding="utf-8-sig")


from analysis import run_analysis


run_analysis("C:\\Users\\Emre\\Desktop\\python\\unanswered_question_project\\output.csv")
