# ai_marketing_copywriter.py
"""
Generative Marketing Copywriter  📢🖼️
────────────────────────────────────────────────────────────────────────────
Paste a short product / service description, pick a creativity level,
and this POC will:

1. **Generate** SEO-optimised ads (headline, body, keywords, hashtags)
   via a free OpenRouter LLM.  
2. **Create** 3 thumbnail-style images with Stable Diffusion (CPU) that
   match the product vibe.  
3. Let you download the copy and images.

Demo-grade only — for a production-ready generative-marketing pipeline
(brand tuning, safety filtering, caching) contact me → drtomharty.com/bio
"""
# ───────────────────────────────────────── imports ────────────────────────
import os, io, base64, requests
import streamlit as st
from diffusers import StableDiffusionPipeline
import torch

# ───────────────────── OpenRouter helper ──────────────────────────────────
API_KEY = st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY") or ""
MODEL   = "shisa-ai/shisa-v2-llama3.3-70b:free"  # free

def openrouter_generate(prompt, temperature=0.8):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://portfolio.example",
        "X-Title": "AI-Marketing-Copywriter",
    }
    body = {
        "model": MODEL,
        "messages": [
            {"role":"system","content":"You are a world-class marketing copywriter."},
            {"role":"user","content":prompt}
        ],
        "temperature": temperature,
    }
    r = requests.post(url, headers=headers, json=body, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

# ───────────────────── Stable Diffusion loader ───────────────────────────
@st.cache_resource(show_spinner=False)
def load_sd_pipeline():
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        safety_checker=None,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    )
    if torch.cuda.is_available():
        pipe = pipe.to("cuda")
    return pipe

def generate_images(prompt, n_imgs=3, guidance=7.5):
    pipe = load_sd_pipeline()
    images = pipe(prompt, num_inference_steps=30, guidance_scale=guidance, num_images_per_prompt=n_imgs).images
    return images

# ─────────────────────────── UI ──────────────────────────────────────────
st.set_page_config(page_title="Generative Marketing Copywriter", layout="wide")
st.title("🎨🤖 Generative Marketing Copywriter")

st.info(
    "🔔 **Demo Notice**  \n"
    "This app is a lightweight proof-of-concept. For brand-safe, enterprise-grade "
    "generative marketing systems, [contact me](https://drtomharty.com/bio).",
    icon="💡"
)

product_desc = st.text_area("📝 Describe your product or service", height=150,
                            placeholder="e.g., A plant-based protein bar with 20g protein, no sugar, and compostable wrapper")
creativity = st.slider("Creativity / Temperature", 0.2, 1.0, 0.8, 0.05)
tone = st.selectbox("Tone", ["Friendly", "Professional", "Playful", "Luxury", "Tech-Savvy"])

if st.button("🚀 Generate copy & images") and product_desc.strip():
    # ---------------- Copy Generation ----------------
    copy_prompt = (
        f"Write an ad in a **{tone.lower()}** tone for the following product description:\n\n"
        f"{product_desc}\n\n"
        "Return:\n"
        "1. Catchy Headline (≤10 words)\n"
        "2. Ad Body (30-40 words)\n"
        "3. 6 SEO Keywords\n"
        "4. 5 Hashtags\n\n"
        "Format clearly with markdown bullet points."
    )
    with st.spinner("Writing marketing copy…"):
        copy_text = openrouter_generate(copy_prompt, temperature=creativity)
    st.subheader("📄 Generated Marketing Copy")
    st.markdown(copy_text)

    # ---------------- Image Generation ---------------
    img_prompt = f"{product_desc}. minimalist studio product shot, bright lighting, high resolution"
    with st.spinner("Rendering images (may take ~40s on CPU)…"):
        imgs = generate_images(img_prompt, n_imgs=3)
    st.subheader("🖼️ AI-Generated Thumbnails")
    cols = st.columns(3)
    for i, im in enumerate(imgs):
        cols[i].image(im, use_column_width=True)
        # download link
        buf = io.BytesIO()
        im.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        cols[i].markdown(f"[Download](data:image/png;base64,{b64})", unsafe_allow_html=True)

    # ---------------- Download copy ------------------
    st.download_button("⬇️ Download copy (.txt)", copy_text.encode(), "marketing_copy.txt", "text/plain")

else:
    st.caption("Enter your product description above and click **Generate**.")
