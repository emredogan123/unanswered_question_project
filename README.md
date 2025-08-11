# ✅ Internship Assignment 4 – Vivollo Semantic Labeling & Accuracy Analysis (AI/NLP)

## 🎯 Project Objective

This project analyzes customer conversations collected from the **DüğünBuketi** platform (JSON format).
The goal is to **semantically label** each message and measure the accuracy of a Large Language Model (LLM) by comparing its predictions with manually labeled ground truth.

For each message:

* Detect if the bot answered (`bot_answered`: Yes / No)
* Detect sentiment (`sentiment`: Positive / Negative / Neutral)
* Detect topic/category (`topic`: predefined DüğünBuketi category list)

Additionally, calculate **accuracy metrics** by comparing LLM predictions vs manual labels.

---

## 🛠️ Tasks

1. **Parse JSON conversation logs** – Read `.json` file line by line, extract message text and metadata.
2. **Generate labels with an LLM** – Use a prompt to get `sentiment`, `topic`, and `bot_answered` for each message, save to `llm_outputs.json`.
3. **Manual labeling** – Fill in `manual_labels.csv` with correct labels.
4. **Accuracy analysis** – Compare LLM vs manual labels, compute accuracy per label type, save to `accuracy_report.md`.

---

## ⚙️ Technical Requirements

* **Python 3.9+**
* Libraries: `pandas`, `requests`
* LLM options: Local ([Ollama](https://ollama.ai) with `mistral`, `llama3`, etc.) or Cloud (OpenAI, Gemini)
* **Free model usage first**: Begin with free/open-source LLMs (e.g., Ollama local models) to develop and test the pipeline.
* **Optional premium models**: Upgrade to GPT-4 or similar for final evaluation if available.

---

## 📂 File Structure

```
unanswered_question_project/
├── accuracy_report.md          # Accuracy results + best prompt notes
├── accuracy_report.py          # Accuracy calculation script
├── analysis.py                  # Extra analysis
├── last-500-conversation-dugunbuketi.json   # Raw data
├── llm_outputs.json             # LLM predictions
├── main.py                      # Labeling script
├── manual_labels.csv            # Ground truth labels
├── output.csv                   # Optional export
├── prompt_versions.txt          # Prompt history
├── README.md                    # Documentation
└── test_openai.py                # API test script
```

---

## 📋 Example Output

**manual\_labels.csv**

```csv
message_text,sentiment,topic,bot_answered
"Merhaba, gelinlik denemek için randevu alabilir miyim?",Pozitif,Gelinlik ve Moda Evleri,Evet
"Fiyatlarınız çok pahalı, bu nasıl hizmet!",Negatif,Düğün Mekanları,Hayır
```

**accuracy\_report.md**

| Başlık        | Doğru Sayısı | Toplam | Doğruluk (%) |
| ------------- | ------------ | ------ | ------------ |
| Sentiment     | 92           | 100    | %92          |
| Topic         | 89           | 100    | %89          |
| Bot\_answered | 96           | 100    | %96          |

**Example JSON Input**

```json
{
  "conversation_id": "12345",
  "message_id": "abc123",
  "message_text": "Do you have availability in May?"
}
```

**Example JSON Output (LLM Prediction)**

```json
{
  "conversation_id": "12345",
  "message_id": "abc123",
  "message_text": "Do you have availability in May?",
  "llm_prediction": {
    "sentiment": "Nötr",
    "topic": "Düğün Mekanları",
    "bot_answered": "Hayır"
  }
}
```

---

## 📌 Notes

* Evaluate each message independently.
* Topics must match **DüğünBuketi** list.
* Keep prompt history in `prompt_versions.txt`.
* Code should be reusable.

---

## ✅ Final Deliverables

1. `llm_outputs.json`
2. `manual_labels.csv`
3. `accuracy_report.md`
4. `prompt_versions.txt`

---

## 🏆 Best Prompt (v3 – En iyi sonuç)

```
Sen bir etiketleme asistanısın. Sana verilen kısa sohbet özetine bakarak
3 alan üret: sentiment, topic, bot_answered.

Kurallar:
- sentiment: "Pozitif" / "Negatif" / "Nötr"
- topic: AŞAĞIDAKİ LİSTEDEN birebir seç.
  Düğün Mekanları: Düğün Salonları, Kır Düğünü Mekanları, Davet Alanları, Otelde Düğün, Tarihi Düğün Mekanları, Havuz Başı Düğün Mekanları, Teknede Düğün ve Davet, Sosyal Tesisler, Luxury Wedding, Nikah Salonu ve Evlendirme Dairesi, Sünnet Düğünü Mekanları, Tüm Düğün Mekanları
  Diğer Davet Mekanları: Kına Gecesi Mekanları, Gelin Hamamı Mekanları, Söz, İsteme, Nişan Mekanları, Davet Evleri, Nikah Sonrası Yemek, Mezuniyet ve Balo Mekanları, After Party İçin Eğlence Mekanları, Doğum Günü Parti Evleri ve Baby Shower Mekanları, Evlilik Teklifi Mekanları, Konferans ve Toplantı Salonları, Tüm Diğer Davet Mekanları
  Düğün Firmaları: Dış Çekim ve Düğün Fotoğrafçıları, Gelin Saçı ve Makyajı, Gelinlik ve Moda Evleri, Gelin Arabası, Düğün Orkestrası, DJ ve Müzik Grupları, Düğün Dans Kursu, Düğün Davetiyesi, Nikah Şekeri ve Hediyelik, Düğün Yemeği için Catering Firmaları, Düğün Pastası Firmaları, Gelin Çiçeği, Damatlık Modelleri, Gelin Ayakkabısı ve Aksesuarları, Nişanlık ve Abiye Modelleri, Alyans ve Tektaş Yüzük, Tüm Düğün Firmaları
  Organizasyon Firmaları: Kına Gecesi Organizasyonu, Nişan Organizasyonu Firmaları, Doğum Günü ve Baby Shower Organizasyonu Firmaları, Mezuniyet ve Balo Organizasyonu Firmaları, Evlilik Teklifi Organizasyonu Firmaları, Sünnet Organizasyonu Firmaları, Tüm Organizasyon Firmaları
  Balayı: Balayı Otelleri, Balayı Evleri, Balayı Gemi Turları, Tüm Balayı
- bot_answered: Kullanıcının ihtiyacına yönelik yanıt verildiyse "Evet", aksi halde "Hayır".
- Konu seçiminde anahtar kelimeleri dikkate al.
- Yanıtı geçerli JSON formatında döndür.
- Ek açıklama yazma.
```

**Notes:** Full category list, low temperature, strict JSON output → highest accuracy.
