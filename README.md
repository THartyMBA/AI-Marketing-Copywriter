# AI-Marketing-Copywriter

🎨🤖 Generative Marketing Copywriter
A Streamlit proof-of-concept that turns a simple product description into:

SEO-optimized ad copy (headline, body text, keywords, hashtags) via a free OpenRouter LLM

AI-generated thumbnail images (Stable Diffusion) to match your brand vibe

One-click downloads of both the copy and the images

Demo only—no brand filtering, safety audits, or enterprise workflows.
For a production-grade generative marketing pipeline, contact me.

✨ Features
Text generation: Catchy headline, concise ad body, 6 SEO keywords, 5 hashtags

Image generation: 3 thumbnails rendered with Stable Diffusion v1-5 (CPU-fallback)

Adjustable creativity: Temperature slider + tone selector

Download buttons: Grab your copy as .txt and images as .png

Zero frontend code: Single Python file, no JavaScript needed

🔑 Add your OpenRouter API Key
Streamlit Cloud
Deploy your repo → ⋯ ➜ Edit secrets

Add:

toml
Copy
Edit
OPENROUTER_API_KEY = "sk-or-xxxxxxxxxxxxxxxx"
Local development
Create ~/.streamlit/secrets.toml:

toml
Copy
Edit
OPENROUTER_API_KEY = "sk-or-xxxxxxxxxxxxxxxx"
OR export an env-var:

bash
Copy
Edit
export OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxx
🚀 Quick Start (Local)
bash
Copy
Edit
git clone https://github.com/THartyMBA/ai-marketing-copywriter.git
cd ai-marketing-copywriter
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run ai_marketing_copywriter.py
Open http://localhost:8501 in your browser, paste your product description, and click Generate copy & images.

☁️ Deploy on Streamlit Cloud (Free)
Push this repo (public or private) to GitHub under your THartyMBA account.

Go to streamlit.io/cloud ➜ New app → select your repo/branch.

Add OPENROUTER_API_KEY in Secrets.

Click Deploy—done!

🛠️ Requirements
shell
Copy
Edit
streamlit>=1.32
requests
diffusers
transformers
torch
(Stable Diffusion runs on CPU in ~40 s per batch on Streamlit’s free tier.)

🗂️ Repo Structure
vbnet
Copy
Edit
ai_marketing_copywriter.py   ← single-file Streamlit app
requirements.txt
README.md                    ← you’re reading it now
📜 License
CC0 1.0 – public domain dedication. Attribution appreciated but not required.

🙏 Acknowledgements
OpenRouter – unified free LLM gateway

Stable Diffusion – image generation

Streamlit – rapid Python UIs

Diffusers – inference pipeline

Create stunning ad copy and visuals in seconds—enjoy!
