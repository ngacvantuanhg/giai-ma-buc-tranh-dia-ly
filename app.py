import streamlit as st
from PIL import Image
from groq import Groq
import base64
import markdown

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Giải Mã Bức Tranh Lịch Sử - Địa Lý", page_icon="🌍", layout="wide")

# Khởi tạo session_state để lưu trữ dữ liệu bền vững
if "ai_suggestions" not in st.session_state:
    st.session_state.ai_suggestions = ""
if "current_image_name" not in st.session_state:
    st.session_state.current_image_name = ""

# --- 2. BẢO MẬT: LẤY API KEY TỪ SECRETS ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("⚠️ Hệ thống chưa tìm thấy GROQ_API_KEY trong phần Settings > Secrets của Streamlit.")
    api_key = None

# --- 3. GIAO DIỆN CHÍNH ---
st.title("🌍 Ứng Dụng: Giải Mã Bức Tranh Lịch Sử - Địa Lý")
st.markdown("*Công cụ hỗ trợ giảng dạy tương tác cho giáo viên Địa lý - Trường THCS Lê Quý Đôn, phường Hà Giang 1, tỉnh Tuyên Quang*")
st.markdown("---")

# Tải ảnh lên
uploaded_file = st.file_uploader("📥 Giáo viên tải lên hình ảnh / bản đồ / biểu đồ tại đây (jpg, png)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Nếu đổi ảnh mới, tự động xóa gợi ý cũ
    if uploaded_file.name != st.session_state.current_image_name:
        st.session_state.ai_suggestions = ""
        st.session_state.current_image_name = uploaded_file.name

    # Chia bố cục 2 cột
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.image(image, caption="Bức tranh địa lý cần giải mã", use_container_width=True)
        
        # Nút gọi AI phân tích
        if api_key:
            if st.button("🤖 Nhờ Trợ lý AI phân tích và gợi ý câu hỏi", use_container_width=True):
                with st.spinner("AI đang giải mã bức tranh siêu tốc..."):
                    try:
                        # Chuyển ảnh sang Base64 cho Groq
                        uploaded_file.seek(0)
                        base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
                        
                        client = Groq(api_key=api_key)
                        
                        prompt = """
                        Bạn là một chuyên gia giảng dạy Địa lý cấp THCS. Hãy quan sát ảnh và soạn hệ thống câu hỏi gợi mở cho học sinh:
                        1. Quan sát: 2 câu hỏi mô tả sự vật, hiện tượng thấy rõ trong ảnh.
                        2. Phân tích: 2 câu hỏi giải thích tại sao có hiện tượng đó.
                        3. Suy luận: 2 câu hỏi về mối liên hệ với kinh tế, môi trường hoặc con người.
                        4. Tổng hợp: 1 câu hỏi chốt thông điệp chính.
                        Trình bày bằng tiếng Việt, ngôn ngữ sư phạm chuẩn mực.
                        """
                        
                        # Sử dụng mô hình Llama 4 Scout mới nhất
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
                        st.success("Đã phân tích xong!")
                    except Exception as e:
                        st.error(f"Có lỗi xảy ra: {e}")

    with col2:
        st.subheader("🔍 Quy trình Giải mã")
        
        # Hiển thị gợi ý AI và nút tải file Word
        if st.session_state.ai_suggestions:
            with st.expander("💡 BỘ CÂU HỎI GỢI Ý TỪ AI", expanded=True):
                st.markdown(st.session_state.ai_suggestions)
                
                # Chuyển Markdown sang HTML chuẩn Word
                html_content = markdown.markdown(st.session_state.ai_suggestions)
                word_template = f"""
                <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
                <head><meta charset="utf-8"></head>
                <body style="font-family:'Times New Roman', serif; font-size:14pt;">
                    <h2 style="text-align:center;">HỆ THỐNG CÂU HỎI GIẢI MÃ ĐỊA LÝ</h2>
                    <p style="text-align:center;"><i>Bức tranh: {st.session_state.current_image_name}</i></p>
                    <hr>
                    {html_content}
                </body>
                </html>
                """
                
                st.download_button(
                    label="📝 Tải bộ câu hỏi về máy (Bản Word chuẩn)",
                    data=word_template,
                    file_name=f"Giao_an_Dia_ly_{st.session_state.current_image_name}.doc",
                    mime="application/msword",
                    use_container_width=True
                )
        
        # Các Tab tương tác cho giáo viên ghi chú trên lớp
        tab1, tab2, tab3, tab4 = st.tabs(["1. Quan sát", "2. Phân tích", "3. Suy luận", "4. Tổng hợp"])
        
        with tab1:
            st.info("Học sinh nhìn thấy gì trong ảnh?")
            st.text_area("Ghi chú bước 1:", key="obs", height=100)
                
        with tab2:
            st.info("Giải thích đặc điểm, nguyên nhân địa lý.")
            st.text_area("Ghi chú bước 2:", key="ana", height=100)
                
        with tab3:
            st.info("Liên hệ thực tế, con người và kinh tế.")
            st.text_area("Ghi chú bước 3:", key="inf", height=100)
                
        with tab4:
            st.success("Thông điệp địa lý cốt lõi là gì?")
            st.text_area("Kết luận bài học:", key="sum", height=120)
            
            if st.button("🎉 Hoàn thành tiết học!", use_container_width=True):
                st.balloons()
