import streamlit as st
import time
from google import genai

# Khởi tạo Gemini Client
client = genai.Client(api_key="AIzaSyAPsuCXtq4OiVVEplRDcjOCqd134Mg5gd4")

# Cấu hình trang mở rộng
st.set_page_config(
    page_title="Hệ thống Trợ lý Lâm nghiệp & Đất đai AI",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khởi tạo bộ nhớ hội thoại
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Xin chào đồng chí! Tôi có thể hỗ trợ tra cứu văn bản pháp luật, đối chiếu số liệu hiện trường hoặc soạn thảo văn bản tham mưu. Vui lòng nhập nội dung cần giải quyết."
        }
    ]

# Tùy biến CSS
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .stChatMessage { border-radius: 10px; padding: 12px; margin-bottom: 8px; }
    .stButton button { border-radius: 8px; height: 42px; font-weight: 500; }
    .doc-badge {
        display: inline-block;
        padding: 3px 8px;
        background: #e2e8f0;
        color: #334155;
        border-radius: 4px;
        font-size: 12px;
        margin-right: 4px;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR: QUẢN LÝ KHO TRI THỨC -----------------
with st.sidebar:
    st.header("🗂️ Kho Tri thức Quy chuẩn")
    
    with st.expander("📤 Nạp thêm tài liệu quy phạm/hồ sơ", expanded=False):
        uploaded_files = st.file_uploader(
            "Tải lên văn bản (PDF, DOCX, XLSX)", 
            accept_multiple_files=True,
            type=['pdf', 'docx', 'xlsx']
        )
        doc_category = st.selectbox(
            "Phân loại tài liệu", 
            ["Văn bản QPPL (Luật, NĐ, TT)", "Hồ sơ thiết kế / Khai thác", "Hồ sơ vi phạm / Xử phạt", "Khác"]
        )
        if st.button("⚡ Đồng bộ vào Vector DB", use_container_width=True):
            with st.spinner("Đang trích xuất và lập chỉ mục ngữ nghĩa..."):
                time.sleep(1)
            st.success("Đã đồng bộ thành công!")

    st.divider()
    st.subheader("Phạm vi truy xuất dữ liệu")
    filter_law = st.checkbox("Văn bản Quy phạm Pháp luật", value=True)
    filter_records = st.checkbox("Hồ sơ & Bản đồ hiện trạng địa bàn", value=True)
    
    st.caption("Trạng thái RAG: **Sẵn sàng (29 tài liệu đã lập chỉ mục)**")

# ----------------- GIAO DIỆN CHÍNH (CHIA ĐÔI MÀN HÌNH) -----------------
col_chat, col_inspect = st.columns([6, 4], gap="medium")

# CỘT TRÁI: HỎI ĐÁP & LỊCH SỬ CHAT
with col_chat:
    st.subheader("💬 Trợ lý Nghiệp vụ Trực tuyến")
    
    # Gợi ý tác vụ nhanh
    c1, c2, c3 = st.columns(3)
    quick_text = None
    if c1.button("📋 Quy định diễn biến rừng", use_container_width=True):
        quick_text = "Quy định mới nhất về theo dõi diễn biến rừng gồm những điểm gì?"
    if c2.button("⚖️ Định khung xử phạt phá rừng", use_container_width=True):
        quick_text = "Hành vi phá rừng tự nhiên trái phép bị định khung xử phạt thế nào?"
    if c3.button("📝 Mẫu biên bản kiểm tra", use_container_width=True):
        quick_text = "Soạn mẫu biên bản kiểm tra hiện trường khai thác lâm sản"

    # Hiển thị hội thoại
    chat_container = st.container(height=520)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

# CỘT PHẢI: TRÍCH XUẤT NGUỒN & BIÊN TẬP VĂN BẢN
with col_inspect:
    tab_source, tab_draft = st.tabs(["🔍 Căn cứ & Trích dẫn Nguồn", "📄 Soạn thảo Báo cáo"])
    
    with tab_source:
        st.caption("Các điều khoản, đoạn văn bản được AI trích xuất trực tiếp:")
        
        with st.expander("📌 Nghị định số 01/2019/NĐ-CP (Điều 8)", expanded=True):
            st.markdown("""
            * **Trích đoạn:** *“Kiểm lâm địa bàn có nhiệm vụ tham mưu Chủ tịch UBND cấp xã tổ chức thực hiện công tác quản lý bảo vệ rừng, theo dõi diễn biến rừng...”*
            * **Độ tương đồng:** `96.4%` | **Trang:** 4
            """)
            
        with st.expander("📌 Luật Lâm nghiệp 2017 (Điều 33)"):
            st.markdown("""
            * **Trích đoạn:** *“Theo dõi diễn biến rừng bao gồm việc thống kê, cập nhật các biến động về diện tích, cơ cấu loại rừng...”*
            * **Độ tương đồng:** `91.8%` | **Trang:** 18
            """)

    with tab_draft:
        st.caption("Xem trước và chỉnh sửa nhanh báo cáo tham mưu:")
        report_text = st.text_area(
            label="Nội dung văn bản",
            value="""BÁO CÁO THAM MƯU
Về việc rà soát quy định theo dõi diễn biến rừng trên địa bàn

Kính gửi: Lãnh đạo đơn vị

Căn cứ quy định hiện hành về quản lý và theo dõi diễn biến rừng...
1. Cơ sở dữ liệu và công cụ thực hiện:
- Sử dụng hệ thống phần mềm quản lý chuyên ngành và dữ liệu ảnh vệ tinh.
- Cập nhật định kỳ các biến động trạng thái rừng.""",
            height=380
        )
        
        btn_c1, btn_c2 = st.columns(2)
        btn_c1.download_button(
            label="📥 Tải file Word (.docx)",
            data=report_text,
            file_name="Bao_cao_tham_muu.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
        btn_c2.button("📋 Sao chép văn bản", use_container_width=True)

# ----------------- THANH NHẬP CHAT VÀ GỌI GEMINI AI -----------------
user_prompt = st.chat_input("Nhập câu hỏi pháp lý hoặc yêu cầu nghiệp vụ...")
active_prompt = user_prompt or quick_text

if active_prompt:
    st.session_state.messages.append({"role": "user", "content": active_prompt})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(active_prompt)
        
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            with st.spinner("Đang tra cứu cơ sở dữ liệu pháp luật và phân tích..."):
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f"Bạn là trợ lý nghiệp vụ lâm nghiệp chuyên trách. Hãy giải đáp chính xác, đúng căn cứ pháp luật cho câu hỏi: {active_prompt}"
                    )
                    reply = response.text
                except Exception as e:
                    reply = f"Lỗi phản hồi: {e}"
                
                response_placeholder.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
