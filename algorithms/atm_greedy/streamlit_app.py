import streamlit as st
from core import ATMGreedy


def format_currency(amount: int) -> str:
    """Format số tiền với dấu phẩy"""
    return f"{amount:,}"


def parse_currency_input(input_str: str) -> int:
    """Parse input string, loại bỏ dấu phẩy và chấm"""
    if not input_str:
        return 0
    return int(input_str.replace(",", "").replace(".", ""))


def main():
    # Cấu hình trang
    st.set_page_config(
        page_title="ATM Greedy Algorithm (Naive Approach)",
        page_icon="💰",
        layout="centered"
    )

    # Header
    st.title("ATM Greedy Algorithm Naive Approach")
    st.markdown("### Bài toán rút tiền sao cho số tờ tiền là ít nhất")
    st.markdown("---")

    # Sidebar - Thông tin thuật toán
    with st.sidebar:
        st.header("Về thuật toán")
        st.markdown("""
        **Greedy Algorithm** chọn mệnh giá lớn nhất có thể ở mỗi bước.

        **Mệnh giá VNĐ:**
        - 500,000 đ
        - 200,000 đ
        - 100,000 đ
        - 50,000 đ
        - 20,000 đ
        - 10,000 đ

        **Quy tắc:**
        - Số tiền phải > 0
        - Phải là bội số của 10,000 VNĐ
        - Chỉ được rút tối đa 100,000,000 VNĐ mỗi lần
        
        **Giả định:**
        - ATM có đủ tất cả các mệnh giá, không giới hạn số tờ tiền
        - Giả định này giúp minh họa thuật toán Greedy một cách đơn giản và dễ dàng nhất. 
        """)

        st.markdown("---")
        st.markdown("**Độ phức tạp:** O(n)")
        st.markdown("**n:** Số lượng mệnh giá")

        st.markdown("---")

    # Main content
    atm = ATMGreedy()

    # Session state để lưu giá trị
    if 'amount' not in st.session_state:
        st.session_state.amount = ""

    # Input với auto-format
    amount_input = st.text_input(
        "💵 Nhập số tiền cần rút (VNĐ):",
        value=st.session_state.amount,
        placeholder="Ví dụ: 1,250,000",
        help="Số tiền phải là bội số của 10,000 và nhỏ hơn hoặc bằng 100,000,000 VNĐ",
        key="amount_input"
    )

    # Format số khi người dùng nhập
    if amount_input:
        try:
            # Parse và format lại
            raw_amount = parse_currency_input(amount_input)
            if raw_amount > 0:
                formatted = format_currency(raw_amount)
                # Chỉ update nếu khác với giá trị hiện tại để tránh loop
                if amount_input != formatted:
                    st.session_state.amount = formatted
                    st.rerun()
        except ValueError:
            pass

    # Quick amount buttons
    st.markdown("**Hoặc chọn nhanh:**")
    quick_amounts = [500000, 1000000, 2000000, 5000000]
    cols = st.columns(4)

    for idx, qa in enumerate(quick_amounts):
        with cols[idx]:
            if st.button(f"💰 {qa // 1000}K", use_container_width=True):
                st.session_state.amount = format_currency(qa)
                st.rerun()

    st.markdown("---")

    # Process button
    calculate_btn = st.button("Rút tiền", type="primary", use_container_width=True)

    # Process
    if calculate_btn:
        if not amount_input:
            st.warning("Vui lòng nhập số tiền")
        else:
            try:
                amount = parse_currency_input(amount_input)

                # Validate
                is_valid, error_msg = atm.validate_amount(amount)
                if not is_valid:
                    st.error(f"{error_msg}")
                    return

                # Calculate
                result = atm.withdraw(amount)
                total_notes = atm.get_total_notes(result)

                # Display result
                st.success(f"✅ Rút thành công {format_currency(amount)} VNĐ")

                st.markdown("### 💵 Kết quả:")

                # Display in columns
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown("**Chi tiết:**")
                    for denomination, count in result.items():
                        st.markdown(
                            f"- **{count}** tờ × {format_currency(denomination)} đ "
                            f"= {format_currency(count * denomination)} đ"
                        )

                with col2:
                    st.metric(
                        label="Tổng số tờ",
                        value=total_notes,
                        delta="Tối ưu" if total_notes <= 10 else None
                    )

                # Visualization
                st.markdown("### 📊 Phân bố:")
                chart_data = {
                    f"{format_currency(d)}đ": count
                    for d, count in result.items()
                }
                st.bar_chart(chart_data)

            except ValueError as e:
                st.error(f"❌ Lỗi: {str(e)}")
            except Exception as e:
                st.error(f"❌ Có lỗi xảy ra: {str(e)}")

    # Footer
    st.markdown("---")

if __name__ == "__main__":
    main()