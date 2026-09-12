import streamlit as st
import time

# Cấu hình trang mở rộng
st.set_page_config(
    page_title="Hệ thống Trợ lý Lâm nghiệp & Đất đai AI",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tùy biến CSS tăng tính trực quan, giao diện phẳng chuyên nghiệp
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

# CỘT TRÁI: HỎI ĐÁP & CHAT TRỢ LÝ
with col_chat:
    st.subheader("💬 Trợ lý Nghiệp vụ Trực tuyến")
    
    # Gợi ý tác vụ nhanh (Quick Action Chips)
    c1, c2, c3 = st.columns(3)
    if c1.button("📋 Quy định diễn biến rừng", use_container_width=True):
        st.session_state.prefill = "Quy định mới nhất về theo dõi diễn biến rừng gồm những điểm gì?"
    if c2.button("⚖️ Định khung xử phạt phá rừng", use_container_width=True):
        st.session_state.prefill = "Hành vi phá rừng tự nhiên trái phép bị định khung xử phạt thế nào?"
    if c3.button("📝 Mẫu biên bản kiểm tra", use_container_width=True):
        st.session_state.prefill = "Soạn mẫu biên bản kiểm tra hiện trường khai thác lâm sản"

    # Hộp hiển thị lịch sử trao đổi
    chat_container = st.container(height=520)
    with chat_container:
        with st.chat_message("assistant"):
            st.markdown(
                "Xin chào đồng chí! Tôi có thể hỗ trợ tra cứu văn bản pháp luật, "
                "đối chiếu số liệu hiện trường hoặc soạn thảo văn bản tham mưu. Vui lòng nhập nội dung cần giải quyết."
            )

    # Khung nhập câu hỏi và file đính kèm trực tiếp
    user_prompt = st.chat_input("Nhập câu hỏi pháp lý hoặc yêu cầu nghiệp vụ...")

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