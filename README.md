# SIP/SMPP NOC Assistant

AI-powered PCAP analyzer for SIP + SMPP traffic with rules, alerts, and Grok explanations.

### Features
- Drag & drop PCAP upload
- Folder watcher (`watched/` folder) – auto processes new files
- Simple rule engine (SIP failure rate, SMPP errors)
- SQLite DB (zero-config, works on Streamlit Cloud)
- Natural language chat with Grok
- Dashboard with charts & alerts

### Quick Local Run
```bash
git clone https://github.com/yourusername/sip-smpp-noc-assistant.git
cd sip-smpp-noc-assistant
cp .env.example .env
# Add your XAI_API_KEY
pip install -r requirements.txt
# Install tshark (Wireshark CLI)
# Ubuntu: sudo apt install tshark
# macOS: brew install wireshark
streamlit run app.py
