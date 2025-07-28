# ✅ Internship Assignment 4 – Vivollo Unanswered Question Detection (AI/NLP)

## 🎯 Project Objective

This project analyzes customer conversations collected from the DüğünBuketi platform in JSON format. The goal is to detect which questions have not been answered and classify them by sentiment and intent.

## 🛠️ Tasks

- Parse and analyze conversation logs line by line from JSON format.
- For each message, generate the following labels:
  - **Answered?** → `Yes` / `No`
  - **Sentiment** → `Positive` / `Negative` / `Neutral`
  - **Category** → e.g., Wedding Venue, Bride, Photographer (a predefined list will be provided)
  - **Intent** → e.g., Looking for a venue, Product inquiry, Asking for information
- Export results in `.csv` or `.sqlite` format.

## ⚙️ Technical Requirements

- Python (recommended libraries: `pandas`, `nltk`, `scikit-learn`, or `transformers`)
- For sentiment and intent detection, you may use:
  - Pretrained models (e.g., Hugging Face Transformers)
  - Rule-based keyword matching (optional)

## 📂 Example Output Format

| message                          | answered | sentiment | category       | intent              |
|----------------------------------|----------|-----------|----------------|---------------------|
| "Do you have availability in May?" | No       | Neutral   | Wedding Venue  | Asking for info     |

## 📌 Notes

- All messages should be evaluated independently.
- You may create helper scripts for preprocessing, labeling, and exporting.
- Code should be modular and reusable for future tasks.

## ✅ Output

Final output should be saved as:

- `output.csv` or
- `output.sqlite`

---

