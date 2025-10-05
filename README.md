# Bank Statement Parser Agent

AI agent that autonomously generates custom PDF parsers for bank statements.

## Architecture

```
┌─────────────┐
│   agent.py  │
└──────┬──────┘
       │
       ↓
┌──────────────────────────────────┐
│  Self-Correction Loop (max 3x)   │
├──────────────────────────────────┤
│  1. Read PDF + CSV samples       │
│  2. Generate parser code (LLM)   │
│  3. Test parser output           │
│  4. If fail: analyze error       │
│  5. Retry with error context     │
└──────────────────────────────────┘
       │
       ↓
┌──────────────────┐
│ custom_parser/   │
│  ├─ icici_parser.py  │
│  └─ sbi_parser.py    │
└──────────────────┘
```

The agent uses LLM (Gemini/Claude) to write parsing code, tests it against expected output, and self-corrects up to 3 times by feeding error messages back to the LLM.

## Setup & Run (5 steps)

### 1. Clone repository
```bash
[git clone https://github.com/YOUR_USERNAME/ai-agent-challenge.git](https://github.com/AdityaKumar1009/ai-agent-challenge)
cd ai-agent-challenge
```

### 2. Install dependencies
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install pandas pdfplumber google-generativeai python-dotenv pytest
```

### 3. Get API key
- Go to https://aistudio.google.com/app/apikey
- Create API key
- Create `.env` file:
```bash
GEMINI_API_KEY=your_key_here
```

### 4. Run agent
```bash
python agent.py --target icici
```

### 5. Run tests
```bash
pytest test_parser.py -v
```

## Example Output

```
🚀 Starting agent for bank: ICICI
📄 PDF: data/icici/icici_sample.pdf
📊 CSV: data/icici/icici_sample.csv

============================================================
🔄 ATTEMPT 1/3
============================================================
🤖 Asking LLM to generate parser code...
✓ Generated 1247 characters of code
💾 Saved parser to: custom_parser/icici_parser.py
🧪 Testing generated parser...
❌ Attempt 1 failed: Column mismatch...

============================================================
🔄 ATTEMPT 2/3
============================================================
🤖 Asking LLM to generate parser code...
✓ Generated 1389 characters of code
💾 Saved parser to: custom_parser/icici_parser.py
🧪 Testing generated parser...
✅ Perfect match!

🎉 SUCCESS on attempt 2!
```

## Features

- ✅ Autonomous code generation
- ✅ Self-debugging (up to 3 attempts)
- ✅ Detailed error feedback to LLM
- ✅ Automated testing with pytest
- ✅ Works with any bank (if sample data provided)

## Technical Stack

- **LLM**: Google Gemini 1.5 Flash (free tier)
- **PDF Parsing**: pdfplumber
- **Data Processing**: pandas
- **Testing**: pytest
- **Agent Pattern**: Plan → Generate → Test → Self-Correct loop
