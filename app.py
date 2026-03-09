import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

st.set_page_config(page_title="YouTube 逐字稿工具", page_icon="📝")
st.title("🎥 YouTube 影片逐字稿抓取器")

url = st.text_input("輸入 YouTube 網址:")

def extract_id(url):
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
    return match.group(1) if match else None

if url:
    vid = extract_id(url)
    if vid:
        st.video(url)
        if st.button("生成逐字稿"):
            try:
                # 抓取字幕（優先繁中、簡中、英文）
                ts_list = YouTubeTranscriptApi.list_transcripts(vid)
                ts = ts_list.find_transcript(['zh-Hant', 'zh-TW', 'zh-Hans', 'en'])
                data = ts.fetch()
                text = " ".join([i['text'] for i in data])
                
                st.success("完成！")
                st.text_area("逐字稿內容：", text, height=300)
                st.download_button("下載文字檔", text, file_name="transcript.txt")
            except Exception as e:
                st.error("找不到字幕或該影片不支援。")
    else:
        st.error("網址格式錯誤")
