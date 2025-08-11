import json, os, requests, pandas as pd
from datetime import datetime

# ======= AYARLAR =======
INPUT_PATH  = "last-500-conversation-dugunbuketi.json"   # dosyanın adı/b yolu
OUT_JSON    = "llm_outputs.json"
OUT_MANUAL  = "manual_labels.csv"
OLLAMA_URL  = "http://localhost:11434/api/chat"
MODEL_NAME  = "llama3:8b"
MAX_CONTEXT_MSGS = 6  # her sohbetten LLM'e göndereceğimiz son mesaj sayısı (kısa tutalım)

# DugunBuketi konu listesi (menüde olanlar)
TOPICS = [
    # Düğün Mekanları
    "Düğün Salonları","Kır Düğünü Mekanları","Davet Alanları","Otelde Düğün","Tarihi Düğün Mekanları",
    "Havuz Başı Düğün Mekanları","Teknede Düğün ve Davet","Sosyal Tesisler","Luxury Wedding",
    "Nikah Salonu ve Evlendirme Dairesi","Sünnet Düğünü Mekanları","Tüm Düğün Mekanları",
    # Diğer Davet Mekanları
    "Kına Gecesi Mekanları","Gelin Hamamı Mekanları","Söz, İsteme, Nişan Mekanları, Davet Evleri",
    "Nikah Sonrası Yemek","Mezuniyet ve Balo Mekanları","After Party İçin Eğlence Mekanları",
    "Doğum Günü Parti Evleri ve Baby Shower Mekanları","Evlilik Teklifi Mekanları",
    "Konferans ve Toplantı Salonları","Tüm Diğer Davet Mekanları",
    # Düğün Firmaları
    "Dış Çekim ve Düğün Fotoğrafçıları","Gelin Saçı ve Makyajı","Gelinlik ve Moda Evleri","Gelin Arabası",
    "Düğün Orkestrası, DJ ve Müzik Grupları","Düğün Dans Kursu","Düğün Davetiyesi","Nikah Şekeri ve Hediyelik",
    "Düğün Yemeği için Catering Firmaları","Düğün Pastası Firmaları","Gelin Çiçeği","Damatlık Modelleri",
    "Gelin Ayakkabısı ve Aksesuarları","Nişanlık ve Abiye Modelleri","Alyans ve Tektaş Yüzük","Tüm Düğün Firmaları",
    # Organizasyon Firmaları
    "Kına Gecesi Organizasyonu","Nişan Organizasyonu Firmaları","Doğum Günü ve Baby Shower Organizasyonu Firmaları",
    "Mezuniyet ve Balo Organizasyonu Firmaları","Evlilik Teklifi Organizasyonu Firmaları","Sünnet Organizasyonu Firmaları",
    "Tüm Organizasyon Firmaları",
    # Balayı
    "Balayı Otelleri","Balayı Evleri","Balayı Gemi Turları","Tüm Balayı"
]

SYSTEM_PROMPT = f"""
Sen bir etiketleme asistanısın. Sana verilen kısa sohbet özetine bakarak
3 alan üret: sentiment, topic, bot_answered.

Kurallar:
- sentiment: "Pozitif" / "Negatif" / "Nötr"
- topic: AŞAĞIDAKİ LİSTEDEN birebir seç. Eğer uygun değilse "Diğer" yaz.
  Liste: {TOPICS}
- bot_answered: Kullanıcının ihtiyacına yönelik yanıt verildiyse "Evet", aksi halde "Hayır".

Sadece şu JSON şemasını döndür:
{{"sentiment":"...","topic":"...","bot_answered":"..."}}
Başka açıklama ekleme.
"""

def call_ollama(messages):
    """Ollama /api/chat ile konuşur ve tek satırlık JSON döner."""
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "options": {
            "temperature": 0.1
        },
        "stream": False
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=120)
    r.raise_for_status()
    content = r.json()["message"]["content"].strip()
    # İçerik JSON ise parse et, değilse güvenli şekilde deneriz
    try:
        return json.loads(content)
    except Exception:
        # içerikte kod bloğu vb. gelirse tırpanla
        content = content.replace("```json","").replace("```","").strip()
        return json.loads(content)

def build_context(conv):
    """
    Her sohbetten son MAX_CONTEXT_MSGS mesajı alırız.
    Kullanıcı + bot karışık kısa bağlam veriyoruz ki 'bot_answered' değerlendirilebilsin.
    """
    msgs = conv.get("messages", [])
    trimmed = [m for m in msgs if not m.get("is_internal")]  # sistem içi olanları çıkar
    tail = trimmed[-MAX_CONTEXT_MSGS:]

    def clean_text(m):
        c = m.get("content")
        if isinstance(c, dict):
            return c.get("text") or ""
        elif isinstance(c, list):
            # carousel/func vb. görmezden gel
            return ""
        return ""

    # Chat formatına çevir
    chat_msgs = [{"role":"system","content": SYSTEM_PROMPT}]
    for m in tail:
        role = "assistant" if (m.get("sender_id") and m.get("sender_id") != None and m.get("sender_id") != "") else "user"
        # heuristik: bot mesajlarında çoğu kez sender_id dolu ve metin 'Merhaba, ben Hera...' gibi
        if m.get("type") == "TEXT":
            text = clean_text(m)
            if not text:
                continue
            # Bazı satırlarda kullanıcı mesajı da 'sender_id' dolu olabilir; güvenli olsun:
            if m.get("sender_id") and m.get("sender_id").startswith("bf"):  # bot id'leri genelde bf... gibi
                role = "assistant"
            else:
                role = "user"
            chat_msgs.append({"role": role, "content": text})
    return chat_msgs

def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Bulunamadı: {INPUT_PATH}")

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        conversations = json.load(f)

    results = []
    manual_rows = []

    for conv in conversations[:100]:  # sadece ilk 100 sohbet

        conv_id = conv.get("conversation_id")
        msgs = conv.get("messages", [])
        # Etiketlenecek 'hedef metin' = son kullanıcı mesajı (text)
        user_text = ""
        user_msg_id = ""
        for m in reversed(msgs):
            if m.get("type") == "TEXT" and not m.get("is_internal"):
                c = m.get("content")
                is_user_like = (m.get("sender_id") is None) or not str(m.get("sender_id")).startswith("bf")
                if is_user_like and isinstance(c, dict) and c.get("text"):
                    user_text = c["text"]
                    user_msg_id = m.get("id")
                    break

        context = build_context(conv)
        try:
            pred = call_ollama(context)
        except Exception as e:
            pred = {"sentiment":"Nötr","topic":"Diğer","bot_answered":"Hayır","_error":str(e)}

        results.append({
            "conversation_id": conv_id,
            "message_id": user_msg_id,
            "message_text": user_text,
            "llm_prediction": pred
        })

        manual_rows.append({
            "conversation_id": conv_id,
            "message_id": user_msg_id,
            "message_text": user_text,
            "sentiment": "",
            "topic": "",
            "bot_answered": ""
        })

    # Çıktılar
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"[OK] {len(results)} sohbet işlendi.")
    print(f"[OK] LLM çıktıları: {OUT_JSON}")


if __name__ == "__main__":
    main()
