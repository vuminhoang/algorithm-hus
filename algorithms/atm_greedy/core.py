from typing import Dict, List, Tuple

class ATMGreedy:

    # Mệnh giá tiền Việt Nam
    DENOMINATIONS = [500000, 200000, 100000, 50000, 20000, 10000]

    def __init__(self, denominations: List[int] = None):
        if denominations:
            self.denominations = sorted(denominations, reverse=True)
        else:
            self.denominations = self.DENOMINATIONS

    def validate_amount(self, amount: int) -> Tuple[bool, str]:
        """
        Kiểm tra tính hợp lệ của số tiền
        """
        if amount <= 0:
            return False, "Số tiền phải lớn hơn 0"

        if amount % 10000 != 0:
            return False, "Số tiền phải là bội số của 10,000 VNĐ"

        if amount > 100000000:
            return False, "Số tiền rút tối đa là 100,000,000 VNĐ"

        return True, ""

    # HÀM RÚT TIỀN
    def withdraw(self, amount: int) -> Dict[int, int]:
        is_valid, error_msg = self.validate_amount(amount)
        if not is_valid:
            raise ValueError(error_msg)

        result = {}
        remaining = amount

        for denomination in self.denominations:
            if remaining >= denomination:
                count = remaining // denomination
                result[denomination] = count
                remaining -= count * denomination

        if remaining > 0:
            raise ValueError(f"Không thể rút số tiền {amount:,} VNĐ với các mệnh giá hiện có")

        return result

    def get_total_notes(self, result: Dict[int, int]) -> int:
        """Tính tổng số tờ tiền"""
        return sum(result.values())

    def format_result(self, result: Dict[int, int]) -> str:
        if not result:
            return "Không có tờ tiền nào"

        lines = []
        for denomination, count in result.items():
            lines.append(f"{count} tờ {denomination:,} VNĐ")

        total_notes = self.get_total_notes(result)
        lines.append(f"\nTổng số tờ: {total_notes}")

        return "\n".join(lines)

# helper function
def withdraw_money(amount: int) -> Dict[int, int]:
    """
    Hàm helper để rút tiền nhanh

    Args:
        amount: Số tiền cần rút

    Returns:
        Dictionary với key là mệnh giá, value là số tờ
    """
    atm = ATMGreedy()
    return atm.withdraw(amount)