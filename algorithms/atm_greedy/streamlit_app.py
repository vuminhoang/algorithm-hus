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
    st.set_page_config(
        page_title="ATM Greedy Algorithm",
        page_icon="💰",
        layout="centered"
    )

    # Header
    st.title("ATM Greedy Algorithm")
    st.markdown("### Minh họa thuật toán tham lam trong bài toán rút tiền")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("Về Greedy Algorithm")

        st.markdown("""
        **Nguyên tắc:**
        > Ở mỗi bước, chọn mệnh giá **lớn nhất có thể**, nhằm giảm thiểu số tờ tiền cần sử dụng.
        """)

        st.markdown("---")

        # Toggle giới hạn
        enable_limits = st.toggle(
            "🔒 Giới hạn số tờ tiền",
            value=False,
            help="Bật để mô phỏng ATM thực tế với số tờ tiền có giới hạn"
        )

        if enable_limits:
            st.info("**Chế độ:** Có giới hạn (ATM thực tế)")
        else:
            st.success("**Chế độ:** Không giới hạn (Minh họa thuật toán)")

        st.markdown("---")
        st.markdown("""
        **Mệnh giá VNĐ:**
        - 500,000 đ
        - 200,000 đ  
        - 100,000 đ
        - 50,000 đ
        - 20,000 đ
        - 10,000 đ

        **Độ phức tạp:** O(n)  
        **n:** Số lượng mệnh giá (6)
        """)

    # Main content
    atm = ATMGreedy()

    # Session state
    if 'amount' not in st.session_state:
        st.session_state.amount = ""
    if 'limits' not in st.session_state:
        st.session_state.limits = {d: 100 for d in atm.DENOMINATIONS}

    # Cấu hình giới hạn (nếu bật)
    limits = None
    if enable_limits:
        st.markdown("### 🏦 Cấu hình ATM")
        st.markdown("**Số tờ tiền có sẵn cho mỗi mệnh giá:**")

        col1, col2, col3 = st.columns(3)
        limits = {}

        for idx, denom in enumerate(atm.DENOMINATIONS):
            col = [col1, col2, col3][idx % 3]
            with col:
                limits[denom] = st.number_input(
                    f"{format_currency(denom)}đ",
                    min_value=0,
                    max_value=1000,
                    value=st.session_state.limits[denom],
                    step=10,
                    key=f"limit_{denom}"
                )

        # Hiển thị tổng tiền
        total_in_atm = sum(d * c for d, c in limits.items())
        st.metric(
            label="💰 Tổng tiền trong ATM",
            value=f"{format_currency(total_in_atm)} VNĐ"
        )

        # Nút reset
        col_reset1, col_reset2 = st.columns([1, 1])
        with col_reset1:
            if st.button("🔄 Reset về 100 tờ", use_container_width=True):
                for denom in atm.DENOMINATIONS:
                    st.session_state.limits[denom] = 100
                st.rerun()
        with col_reset2:
            if st.button("🎲 Số ngẫu nhiên", use_container_width=True):
                import random
                for denom in atm.DENOMINATIONS:
                    st.session_state.limits[denom] = random.randint(5, 50)
                st.rerun()

        st.markdown("---")

    # Input số tiền
    st.markdown("### 💵 Nhập số tiền cần rút")

    amount_input = st.text_input(
        "Số tiền (VNĐ):",
        value=st.session_state.amount,
        placeholder="Ví dụ: 1,250,000",
        help="Phải là bội số của 10,000 VNĐ và ≤ 100,000,000 VNĐ",
        label_visibility="collapsed"
    )

    # Auto format
    if amount_input:
        try:
            raw_amount = parse_currency_input(amount_input)
            if raw_amount > 0:
                formatted = format_currency(raw_amount)
                if amount_input != formatted:
                    st.session_state.amount = formatted
                    st.rerun()
        except ValueError:
            pass

    # Quick buttons
    st.markdown("**Hoặc chọn nhanh:**")
    quick_amounts = [500000, 1000000, 2000000, 5000000]
    cols = st.columns(4)

    for idx, qa in enumerate(quick_amounts):
        with cols[idx]:
            if st.button(f"{qa // 1000}K", use_container_width=True, key=f"quick_{qa}"):
                st.session_state.amount = format_currency(qa)
                st.rerun()

    st.markdown("---")

    # Process button
    if st.button("💸 Rút tiền", type="primary", use_container_width=True):
        if not amount_input:
            st.warning("⚠️ Vui lòng nhập số tiền")
        else:
            try:
                amount = parse_currency_input(amount_input)

                # Validate
                is_valid, error_msg = atm.validate_amount(amount)
                if not is_valid:
                    st.error(f"❌ {error_msg}")
                else:
                    # Check balance nếu có giới hạn
                    if enable_limits:
                        sufficient, total = atm.check_sufficient_balance(amount, limits)
                        if not sufficient:
                            st.error(
                                f"❌ **ATM không đủ tiền!**\n\n"
                                f"- Cần rút: **{format_currency(amount)} VNĐ**\n"
                                f"- Có sẵn: **{format_currency(total)} VNĐ**"
                            )
                            st.stop()

                    # Calculate
                    with st.spinner("⏳ Đang áp dụng thuật toán Greedy..."):
                        try:
                            result = atm.withdraw(amount, limits)
                            rounded_amount = amount
                        except ValueError as e:
                            error_msg = str(e)
                            # Kiểm tra xem có phải case làm tròn không
                            if error_msg.startswith("ROUND_DOWN|"):
                                parts = error_msg.split("|")
                                rounded_amount = int(parts[1])
                                message = parts[2]

                                # Hiển thị thông báo làm tròn
                                st.warning(f"⚠️ {message}")

                                # Hỏi người dùng có muốn rút số tiền làm tròn không
                                st.markdown("---")
                                col_yes, col_no = st.columns(2)
                                with col_yes:
                                    if st.button("✅ Đồng ý rút số tiền làm tròn",
                                                 use_container_width=True,
                                                 type="primary",
                                                 key="accept_round"):
                                        result = atm.withdraw(rounded_amount, limits)
                                        amount = rounded_amount  # Update amount
                                    else:
                                        st.stop()
                                with col_no:
                                    if st.button("❌ Hủy giao dịch",
                                                 use_container_width=True,
                                                 key="cancel_round"):
                                        st.info("Giao dịch đã bị hủy")
                                        st.stop()
                                st.stop()
                            else:
                                # Lỗi khác
                                raise e

                    total_notes = atm.get_total_notes(result)

                    # Success
                    st.success(f"✅ **Rút thành công {format_currency(amount)} VNĐ**")

                    # Display result
                    st.markdown("### 💵 Kết quả chi tiết:")

                    col1, col2 = st.columns([3, 1])

                    with col1:
                        for denomination, count in sorted(result.items(), reverse=True):
                            st.markdown(
                                f"**{count}** tờ × {format_currency(denomination)} đ "
                                f"= **{format_currency(count * denomination)} đ**"
                            )

                    with col2:
                        st.metric(
                            label="📊 Tổng số tờ",
                            value=total_notes,
                            delta="Tối ưu ✨"
                        )

                    # Visualization
                    st.markdown("### 📊 Biểu đồ phân bố:")
                    chart_data = {
                        f"{format_currency(d)}đ": count
                        for d, count in sorted(result.items(), reverse=True)
                    }
                    st.bar_chart(chart_data, height=300)

                    # Số tờ còn lại (nếu có giới hạn)
                    if enable_limits:
                        st.markdown("---")
                        st.markdown("### 🏦 Số tờ còn lại trong ATM:")

                        remaining = {
                            d: limits[d] - result.get(d, 0)
                            for d in atm.DENOMINATIONS
                        }

                        cols = st.columns(3)
                        for idx, (denom, count) in enumerate(remaining.items()):
                            with cols[idx % 3]:
                                delta_val = -result.get(denom, 0) if denom in result else None
                                st.metric(
                                    label=f"{format_currency(denom)}đ",
                                    value=f"{count} tờ",
                                    delta=delta_val
                                )

            except ValueError as e:
                st.error(f"❌ {str(e)}")
            except Exception as e:
                st.error(f"❌ Lỗi không xác định: {str(e)}")

    # Footer
    st.markdown("---")

if __name__ == "__main__":
    main()