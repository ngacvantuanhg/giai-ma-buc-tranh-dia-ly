import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Giải Mã Bức Tranh Địa Lý", page_icon="🌍", layout="wide")

# Khởi tạo session_state để lưu kết quả AI, tránh load lại khi gõ chữ
if "ai_suggestions" not in st.session_state:
    st.session_state.ai_suggestions = ""
if "current_image_name" not in st.session_state:
    st.session_state.current_image_name = ""

# --- SIDEBAR: CẤU HÌNH AI ---
with st.sidebar:
    st.header("⚙️ Cấu hình Trợ lý AI")
    st.markdown("Nhập API Key của Google Gemini để kích hoạt tính năng tự động gợi ý câu hỏi.")
    api_key = st.text_input("🔑 Google Gemini API Key:", type="password")
    st.markdown("*(Nhận API Key miễn phí tại [Google AI Studio](https://aistudio.google.com/app/apikey))*")
    st.divider()
    st.markdown("**Hướng dẫn sử dụng:**\n1. Nhập API Key\n2. Tải ảnh lên\n3. Bấm nút nhờ AI phân tích\n4. Dùng câu hỏi AI gợi ý để dẫn dắt học sinh.")

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
                with st.spinner("AI đang quét dữ liệu địa lý từ bức ảnh..."):
                    try:
                        genai.configure(api_key=api_key)
                        # Dùng model vision chuẩn của Gemini
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        
                        prompt = """
                        Bạn là một giáo viên Địa lý cấp THCS xuất sắc. Hãy quan sát kỹ bức ảnh này và soạn một hệ thống câu hỏi gợi mở để giáo viên hỏi học sinh trên lớp, theo đúng 4 bước sau:
                        1. Quan sát: 2 câu hỏi yêu cầu học sinh liệt kê chi tiết, màu sắc, đối tượng địa lý có trong ảnh.
                        2. Phân tích: 2 câu hỏi yêu cầu học sinh giải thích đặc điểm, nguyên nhân (Tại sao lại có hình dạng/màu sắc/hiện tượng đó?).
                        3. Suy luận: 2 câu hỏi yêu cầu học sinh liên kết hình ảnh với khí hậu, con người, kinh tế, môi trường.
                        4. Tổng hợp: 1 câu hỏi chốt lại bài học hoặc thông điệp địa lý.
                        Trình bày ngắn gọn, súc tích, ngôn từ phù hợp với học sinh lớp 6-9.
                        """
                        response = model.generate_content([prompt, image])
                        st.session_state.ai_suggestions = response.text
                        st.success("Đã phân tích xong! Hãy xem gợi ý bên phần Quy trình Giải mã.")
                    except Exception as e:
                        st.error(f"Có lỗi xảy ra khi gọi AI: {e}")
        else:
            st.warning("👈 Hãy nhập API Key ở menu bên trái để mở khóa tính năng AI!")

    with col2:
        st.subheader("🔍 Quy trình Giải mã")
        
        # Nếu AI đã có kết quả, hiển thị lên trên cùng để giáo viên dễ xem
        if st.session_state.ai_suggestions:
            with st.expander("💡 BỘ CÂU HỎI GỢI Ý TỪ AI (Dành cho giáo viên)", expanded=True):
                st.markdown(st.session_state.ai_suggestions)
        
        tab1, tab2, tab3, tab4 = st.tabs(["1. Quan sát", "2. Phân tích", "3. Suy luận", "4. Tổng hợp"])
        
        with tab1:
            st.markdown("### 👁️ Bước 1: Quan sát tổng thể")
            st.info("Yêu cầu học sinh nhìn kỹ và liệt kê những gì thấy trong tranh.")
            st.text_area("Ghi chép nhanh ý kiến học sinh:", key="obs", height=100)
                
        with tab2:
            st.markdown("### 🧠 Bước 2: Phân tích chi tiết")
            st.info("Kết nối các chi tiết hình ảnh với kiến thức nền.")
            st.text_area("Ghi chép nhanh ý kiến học sinh:", key="ana", height=100)
                
        with tab3:
            st.markdown("### 🕵️ Bước 3: Suy luận & Giải mã")
            st.info("Đưa ra kết luận về ý nghĩa địa lý, mối quan hệ nhân quả.")
            st.text_area("Ghi chép nhanh ý kiến học sinh:", key="inf", height=100)
                
        with tab4:
            st.markdown("### 📝 Bước 4: Tổng hợp")
            st.success("Rút ra thông điệp địa lý chính từ bức tranh.")
            st.text_area("Kết luận bài học:", key="sum", height=120)
            
            if st.button("🎉 Hoàn thành Giải mã!", use_container_width=True):
                st.balloons()
