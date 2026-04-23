import streamlit as st
from PIL import Image

# Cấu hình trang
st.set_page_config(page_title="Giải Mã Bức Tranh Địa Lý", page_icon="🌍", layout="wide")

# Tiêu đề ứng dụng
st.title("🌍 Ứng Dụng: Giải Mã Bức Tranh Địa Lý")
st.markdown("*Công cụ hỗ trợ giảng dạy tương tác - Giúp học sinh khám phá tri thức qua góc nhìn không gian*")
st.markdown("---")

# Khu vực tải ảnh (Giáo viên chuẩn bị trước hoặc tải trực tiếp trên lớp)
uploaded_file = st.file_uploader("📥 Giáo viên tải lên hình ảnh / bản đồ / biểu đồ tại đây (jpg, png)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Chia bố cục làm 2 cột: Ảnh bên trái, Quy trình giải mã bên phải
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.image(image, caption="Bức tranh bí ẩn cần giải mã hôm nay", use_container_width=True)
        
    with col2:
        st.subheader("🔍 Quy trình Giải mã")
        # Sử dụng Tabs để đi từng bước, tránh làm học sinh bị ngợp thông tin
        tab1, tab2, tab3, tab4 = st.tabs(["1. Quan sát", "2. Phân tích", "3. Suy luận", "4. Tổng hợp"])
        
        with tab1:
            st.markdown("### 👁️ Bước 1: Quan sát tổng thể")
            st.info("Yêu cầu học sinh nhìn kỹ và liệt kê những gì thấy trong tranh.")
            st.text_area("Ghi chép nhanh ý kiến học sinh:", placeholder="VD: Em thấy có núi cao, ruộng bậc thang màu vàng, mây mù...", key="obs", height=100)
            with st.expander("💡 Gợi ý câu hỏi cho giáo viên"):
                st.write("- Các em thấy những đối tượng địa lý nào xuất hiện?")
                st.write("- Màu sắc chủ đạo của bức tranh là gì?")
                st.write("- Vị trí của các đối tượng sắp xếp ra sao?")
                
        with tab2:
            st.markdown("### 🧠 Bước 2: Phân tích chi tiết")
            st.info("Kết nối các chi tiết hình ảnh với kiến thức nền.")
            st.text_area("Ghi chép nhanh ý kiến học sinh:", placeholder="VD: Ruộng bậc thang được làm ở sườn đồi dốc để chống xói mòn...", key="ana", height=100)
            with st.expander("💡 Gợi ý câu hỏi cho giáo viên"):
                st.write("- Tại sao đối tượng này lại có hình dạng/màu sắc như vậy?")
                st.write("- Điểm đặc biệt nhất trong bức ảnh này là gì?")
                
        with tab3:
            st.markdown("### 🕵️ Bước 3: Suy luận & Giải mã")
            st.info("Đưa ra kết luận về ý nghĩa địa lý, mối quan hệ nhân quả.")
            st.text_area("Ghi chép nhanh ý kiến học sinh:", placeholder="VD: Khí hậu ở đây chắc chắn rất mát mẻ, phù hợp trồng lúa nước vùng cao...", key="inf", height=100)
            with st.expander("💡 Gợi ý câu hỏi cho giáo viên"):
                st.write("- Yếu tố tự nhiên (khí hậu, địa hình) ảnh hưởng thế nào đến hoạt động của con người trong ảnh?")
                st.write("- Bức tranh phản ánh vấn đề gì? (môi trường, dân số, kinh tế...)")
                
        with tab4:
            st.markdown("### 📝 Bước 4: Tổng hợp")
            st.success("Rút ra thông điệp địa lý chính từ bức tranh.")
            st.text_area("Kết luận bài học:", placeholder="Thông điệp chính của bức tranh là...", key="sum", height=150)
            
            if st.button("🎉 Hoàn thành Giải mã!", use_container_width=True):
                st.balloons()
                st.success("Tuyệt vời! Các em đã giải mã thành công thông điệp địa lý của tiết học hôm nay.")

# --- TÍNH NĂNG NÂNG CAO DÀNH CHO BẠN ---
st.markdown("---")
with st.expander("⚙️ Góc Kỹ Thuật: Tích hợp Trợ lý AI tạo câu hỏi (Dành cho quản trị viên)"):
    st.write("Vì bạn quen thuộc với Python, sau này bạn có thể tích hợp thư viện `google-generativeai` vào đây.")
    st.write("Ý tưởng: Tải ảnh lên -> AI tự động phân tích -> Sinh ra 4 câu hỏi mồi cho 4 bước tương ứng với nội dung bức ảnh, giúp giáo viên tiết kiệm thời gian chuẩn bị giáo án.")
    st.code("""
# Gợi ý code tích hợp AI sau này:
# import google.generativeai as genai
# model = genai.GenerativeModel('gemini-1.5-flash')
# response = model.generate_content(["Đóng vai giáo viên địa lý, hãy đặt 4 câu hỏi theo 4 mức độ: quan sát, phân tích, suy luận, tổng hợp cho bức ảnh này", image])
# st.write(response.text)
    """, language="python")
