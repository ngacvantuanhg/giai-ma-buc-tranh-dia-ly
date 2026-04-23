import streamlit as st
from PIL import Image
from groq import Groq
import base64
import markdown

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Giải Mã Bức Tranh Địa Lý", page_icon="🌍", layout="wide")

# Khởi tạo session_state để lưu kết quả AI
if "ai_suggestions" not in st.session_state:
    st.session_state.ai_suggestions = ""
if "current_image_name" not in st.session_state:
    st.session_state.current_image_name = ""

# --- BẢO MẬT: LẤY API KEY CỦA GROQ ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("⚠️ Hệ thống chưa tìm thấy GROQ_API_KEY trong phần Settings > Secrets.")
    api_key = None

# --- GIAO DIỆN CHÍNH ---
st.title("🌍 Ứng Dụng: Giải Mã Bức Tranh Địa Lý")
st.markdown("*Công cụ hỗ trợ giảng dạy tương tác - Giới thiệu tri thức qua không gian trực quan*")
st.markdown("---")

uploaded_file = st.file_uploader("📥 Giáo viên tải lên hình ảnh / bản đồ / biểu đồ tại đây (jpg, png)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Nếu đổi ảnh mới, xóa gợi ý AI cũ đi
    if uploaded_file.name != st.session_state.current_image_name:
        st.session_state.ai_suggestions = ""
        st.session_state.current_image_name = uploaded_file.name

    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.image(image, caption="Bức tranh bí ẩn cần giải mã hôm nay", use_container_width=True)
        
        # Nút gọi AI phân tích
        if api_key:
            if st.button("🤖 Nhờ Trợ lý AI phân tích và gợi ý câu hỏi", use_container_width=True):
                with st.spinner("AI đang quét dữ liệu siêu tốc..."):
                    try:
                        # Chuyển đổi ảnh sang định dạng Base64 để gửi cho Groq
                        uploaded_file.seek(0)
                        base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
                        
                        client = Groq(api_key=api_key)
                        
                        prompt = """
                        Bạn là một giáo viên Địa lý cấp THCS. Hãy quan sát kỹ bức ảnh này và soạn hệ thống câu hỏi gợi mở để hỏi học sinh trên lớp theo 4 bước:
                        1. Quan sát: 2 câu hỏi liệt kê chi tiết trong ảnh.
                        2. Phân tích: 2 câu hỏi giải thích đặc điểm, nguyên nhân.
                        3. Suy luận: 2 câu hỏi liên kết hình ảnh với khí hậu, con người, kinh tế.
                        4. Tổng hợp: 1 câu hỏi chốt lại thông điệp địa lý.
                        Trình bày bằng tiếng Việt, ngắn gọn, súc tích.
                        """
                        
                        # Gọi mô hình Llama 3.2 Vision siêu tốc của Groq
                        response = client.chat.completions.create(
                            model="meta-llama/llama-4-scout-17b-16e-instruct",
                            messages=[
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": prompt},
                                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                    ]
                                }
                            ],
                            temperature=0.4,
                            max_tokens=1024
                        )
                        
                        st.session_state.ai_suggestions = response.choices[0].message.content
                        st.success("Đã phân tích xong! Hãy xem gợi ý bên phần Quy trình Giải mã.")
                    except Exception as e:
                        st.error(f"Có lỗi xảy ra: {e}")

    with col2:
        st.subheader("🔍 Quy trình Giải mã")
        
        if st.session_state.ai_suggestions:
            with st.expander("💡 BỘ CÂU HỎI GỢI Ý TỪ AI (Dành cho giáo viên)", expanded=True):
                st.markdown(st.session_state.ai_suggestions)
                
                # --- TÍNH NĂNG MỚI: TẢI VỀ MÁY LÀM GIÁO ÁN (ĐÃ CĂN CHỈNH ĐẸP) ---
                # Dịch Markdown sang HTML
                html_text = markdown.markdown(st.session_state.ai_suggestions)
                
                # Bọc văn bản vào khung chuẩn của Word (Font Times New Roman, size 14)
                word_content = f"""
                <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
                <head>
                    <meta charset="utf-8">
                    <title>Giáo Án</title>
                </head>
                <body style="font-family: 'Times New Roman', serif; font-size: 14pt; line-height: 1.5;">
                    <h2 style="text-align: center; color: #2c3e50;">HỆ THỐNG CÂU HỎI GIẢI MÃ</h2>
                    <hr>
                    {html_text}
                </body>
                </html>
                """

                st.download_button(
                    label="📝 Tải giáo án về máy (Bản Word chuẩn)",
                    data=word_content,
                    file_name=f"Giao_an_Dia_ly_{st.session_state.current_image_name}.doc",
                    mime="application/msword",
                    use_container_width=True
                )
        
        tab1, tab2, tab3, tab4 = st.tabs(["1. Quan sát", "2. Phân tích", "3. Suy luận", "4. Tổng hợp"])
        
        tab1, tab2, tab3, tab4 = st.tabs(["1. Quan sát", "2. Phân tích", "3. Suy luận", "4. Tổng hợp"])
        
        with tab1:
            st.markdown("### 👁️ Bước 1: Quan sát tổng thể")
            st.text_area("Ghi chép nhanh ý kiến học sinh:", key="obs", height=100)
                
        with tab2:
            st.markdown("### 🧠 Bước 2: Phân tích chi tiết")
            st.text_area("Ghi chép nhanh ý kiến học sinh:", key="ana", height=100)
                
        with tab3:
            st.markdown("### 🕵️ Bước 3: Suy luận & Giải mã")
            st.text_area("Ghi chép nhanh ý kiến học sinh:", key="inf", height=100)
                
        with tab4:
            st.markdown("### 📝 Bước 4: Tổng hợp")
            st.text_area("Kết luận bài học:", key="sum", height=120)
            
            if st.button("🎉 Hoàn thành Giải mã!", use_container_width=True):
                st.balloons()
