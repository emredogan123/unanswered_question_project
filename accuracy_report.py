import json
import pandas as pd

# Dosya adlarını buraya yaz
LLM_FILE = "llm_outputs.json"
MANUAL_FILE = "manual_labels.csv"

# 1) Manuel etiketleri oku
manual_df = pd.read_csv(MANUAL_FILE)

# 2) LLM çıktısını oku
with open(LLM_FILE, "r", encoding="utf-8") as f:
    llm_data = json.load(f)

# LLM çıktısındaki tahminleri ayrı sütunlara aç
llm_rows = []
for row in llm_data:
    pred = row.get("llm_prediction", {})
    llm_rows.append({
        "conversation_id": row.get("conversation_id"),
        "message_id": row.get("message_id"),
        "message_text": row.get("message_text"),
        "sentiment": pred.get("sentiment"),
        "topic": pred.get("topic"),
        "bot_answered": pred.get("bot_answered"),
    })

llm_df = pd.DataFrame(llm_rows)

# 3) İki tabloyu birleştir (message_id üzerinden eşleşme)
merged = pd.merge(
    manual_df,
    llm_df,
    on=["conversation_id", "message_id", "message_text"],
    suffixes=("_manual", "_llm")
)

# 4) Doğruluk hesapla
def hesapla(kolon):
    return (merged[f"{kolon}_manual"] == merged[f"{kolon}_llm"]).sum(), len(merged)

sonuclar = {}
for kolon in ["sentiment", "topic", "bot_answered"]:
    dogru_say, toplam = hesapla(kolon)
    sonuclar[kolon] = {
        "Doğru Sayısı": dogru_say,
        "Toplam": toplam,
        "Doğruluk (%)": round((dogru_say / toplam) * 100, 2)
    }

# 5) Sonuçları yazdır
print("\n--- Doğruluk Tablosu ---")
for kolon, deger in sonuclar.items():
    print(f"{kolon.capitalize():<15} {deger['Doğru Sayısı']:<10} {deger['Toplam']:<8} %{deger['Doğruluk (%)']}")

# 6) accuracy_report.md dosyasına kaydet
with open("accuracy_report.md", "w", encoding="utf-8") as f:
    f.write("| Başlık       | Doğru Sayısı | Toplam | Doğruluk (%) |\n")
    f.write("|--------------|--------------|--------|--------------|\n")
    for kolon, deger in sonuclar.items():
        f.write(f"| {kolon.capitalize()} | {deger['Doğru Sayısı']} | {deger['Toplam']} | %{deger['Doğruluk (%)']} |\n")

print("\n✅ 'accuracy_report.md' dosyası oluşturuldu.")
