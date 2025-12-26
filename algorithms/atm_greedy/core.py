from typing import Dict, List, Tuple, Optional


class ATMGreedy:
    """
    ATM Greedy Algorithm - Minh họa thuật toán tham lam

    Với mệnh giá VNĐ, Greedy LUÔN cho kết quả tối ưu vì đây là
    canonical coin system (hệ mệnh giá chuẩn tắc).
    """

    DENOMINATIONS = [500000, 200000, 100000, 50000, 20000, 10000]

    def __init__(self, denominations: List[int] = None):
        if denominations:
            self.denominations = sorted(denominations, reverse=True)
        else:
            self.denominations = self.DENOMINATIONS

    def validate_amount(self, amount: int) -> Tuple[bool, str]:
        """Kiểm tra tính hợp lệ của số tiền"""
        if amount <= 0:
            return False, "Số tiền phải lớn hơn 0"
        if amount % 10000 != 0:
            return False, "Số tiền phải là bội số của 10,000 VNĐ"
        if amount > 100000000:
            return False, "Số tiền rút tối đa là 100,000,000 VNĐ"
        return True, ""

    def withdraw(self, amount: int, limits: Optional[Dict[int, int]] = None) -> Dict[int, int]:
        """
        Rút tiền bằng thuật toán Greedy

        Args:
            amount: Số tiền cần rút
            limits: Giới hạn số tờ mỗi mệnh giá (None = vô hạn)

        Returns:
            Dict {mệnh_giá: số_tờ_sử_dụng}

        Raises:
            ValueError: Nếu không thể rút được số tiền này
        """
        is_valid, error_msg = self.validate_amount(amount)
        if not is_valid:
            raise ValueError(error_msg)

        if limits is None:
            return self._greedy_unlimited(amount)
        else:
            return self._greedy_limited(amount, limits)

    def _greedy_unlimited(self, amount: int) -> Dict[int, int]:
        """
        Greedy không giới hạn - Luôn tối ưu với mệnh giá VNĐ
        Độ phức tạp: O(n) với n là số mệnh giá
        """
        result = {}
        remaining = amount

        for denom in self.denominations:
            if remaining >= denom:
                count = remaining // denom
                result[denom] = count
                remaining -= count * denom

        if remaining > 0:
            raise ValueError(f"Không thể rút {amount:,} VNĐ với các mệnh giá hiện có")

        return result

    def _greedy_limited(self, amount: int, limits: Dict[int, int]) -> Dict[int, int]:
        """
        Greedy có giới hạn - Vẫn tối ưu với mệnh giá VNĐ

        Nguyên tắc: Chọn mệnh giá lớn nhất có thể, lấy min(số cần, số có)
        Độ phức tạp: O(n) với n là số mệnh giá
        """
        result = {}
        remaining = amount

        for denom in self.denominations:
            available = limits.get(denom, 0)

            if remaining >= denom and available > 0:
                needed = remaining // denom
                count = min(needed, available)

                result[denom] = count
                remaining -= count * denom

        if remaining > 0:
            total_available = sum(d * limits.get(d, 0) for d in self.denominations)

            if total_available < amount:
                raise ValueError(
                    f"ATM không đủ tiền!\n"
                    f"Cần rút: {amount:,} VNĐ\n"
                    f"Có sẵn: {total_available:,} VNĐ"
                )
            else:
                # Làm tròn xuống
                rounded_amount = amount - remaining
                raise ValueError(
                    f"ROUND_DOWN|{rounded_amount}|"
                    f"Không thể rút chính xác {amount:,} VNĐ.\n"
                    f"Có thể rút: {rounded_amount:,} VNĐ (làm tròn xuống {remaining:,} VNĐ)"
                )

        return result

    def get_total_notes(self, result: Dict[int, int]) -> int:
        """Tính tổng số tờ tiền"""
        return sum(result.values())

    def check_sufficient_balance(self, amount: int, limits: Dict[int, int]) -> Tuple[bool, int]:
        """
        Kiểm tra ATM có đủ tiền không

        Returns:
            (đủ_tiền, tổng_tiền_trong_ATM)
        """
        total = sum(denom * count for denom, count in limits.items())
        return total >= amount, total

    def format_result(self, result: Dict[int, int]) -> str:
        """Format kết quả thành chuỗi dễ đọc"""
        if not result:
            return "Không có tờ tiền nào"

        lines = []
        for denomination, count in sorted(result.items(), reverse=True):
            lines.append(f"{count} tờ {denomination:,} VNĐ")

        total_notes = self.get_total_notes(result)
        lines.append(f"\nTổng số tờ: {total_notes}")

        return "\n".join(lines)


def withdraw_money(amount: int, limits: Optional[Dict[int, int]] = None) -> Dict[int, int]:
    """
    Helper function để rút tiền nhanh

    Args:
        amount: Số tiền cần rút
        limits: Giới hạn số tờ (optional)

    Returns:
        Dictionary {mệnh_giá: số_tờ}

    Examples:
        >>> withdraw_money(1500000)
        {500000: 3}

        >>> withdraw_money(1500000, {500000: 2, 200000: 5, 100000: 10})
        {500000: 2, 200000: 2, 100000: 5}
    """
    atm = ATMGreedy()
    return atm.withdraw(amount, limits)