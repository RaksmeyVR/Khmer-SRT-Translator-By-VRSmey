import streamlit as st
import google.generativeai as genai
import re

# កំណត់ API Key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

def translate_srt(content, target_language="Khmer"):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # បង្កើត Prompt ដើម្បីប្រាប់ AI ឱ្យរក្សាទម្រង់ដើម
    prompt = f"""
    You are a professional subtitle translator. Translate the following SRT content into {target_language}.
    IMPORTANT RULES:
    1. Keep all timestamps (00:00:00,000 --> 00:00:00,000) exactly as they are.
    2. Keep the subtitle index numbers.
    3. Only translate the text sentences.
    4. Return the result in SRT format.
    
    Content:
    {content}
    """
    
    response = model.generate_content(prompt)
    return response.text

st.title("🎬 កម្មវិធីបកប្រែ Subtitle ទៅជាភាសាខ្មែរ")

uploaded_file = st.file_uploader("សូមជ្រើសរើសឯកសារ .srt", type=["srt"])

if uploaded_file is not None:
    # អានអត្ថបទក្នុង File
    file_content = uploaded_file.getvalue().decode("utf-8")
    
    if st.button("ចាប់ផ្ដើមបកប្រែ"):
        with st.spinner('កំពុងបកប្រែ... សូមរង់ចាំមួយភ្លែត'):
            try:
                translated_text = translate_srt(file_content)
                
                st.success("ការបកប្រែជោគជ័យ!")
                st.text_area("លទ្ធផលសម្រាំង:", translated_text, height=300)
                
                # បង្កើតប៊ូតុងសម្រាប់ទាញយក
                st.download_button(
                    label="ទាញយកឯកសារដែលបកប្រែរួច (.srt)",
                    data=translated_text,
                    file_name=f"khmer_{uploaded_file.name}",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"មានបញ្ហាខ្លះ៖ {e}")
