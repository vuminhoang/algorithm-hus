# ATM Greedy Demo

### Cách áp dụng thuật toán tham lam để rút tiền ATM

**Lặp lại cho đến hết:**

1. **Duyệt** danh sách mệnh giá từ **lớn → nhỏ**
2. Tìm mệnh giá **lớn nhất** mà ≤ số tiền còn lại
3. **Chia lấy phần nguyên:** `số_tờ = số_tiền // mệnh_giá`
4. **Cập nhật số tiền còn lại:** `còn_lại = còn_lại - (số_tờ × mệnh_giá)`
5. Quay lại bước 1 với số tiền còn lại

**Ví dụ: Rút 1,250,000 đ**
```
Bước 1: 1,250,000 ÷ 500,000 = 2 tờ → Còn: 250,000
Bước 2: 250,000 ÷ 200,000 = 1 tờ → Còn: 50,000
Bước 3: 50,000 ÷ 50,000 = 1 tờ → Còn: 0 ✓
```

**Kết quả:** 4 tờ (2×500k + 1×200k + 1×50k)

### 📁 Tệp tin trong thư mục
Files
- core.py: greedy_change(amount, denominations) implementation
- streamlit_app.py: Streamlit demo
- requirements.txt: minimal dependencies
- Dockerfile: containerizes the demo

### 🚀 Hướng dẫn chạy demo
Run locally
- pip install -r requirements.txt
- streamlit run streamlit_app.py

Run with Docker:
- Open Docker Desktop and ensure it's running.
- cd algorithm-hus
- docker compose build atm_greedy
- docker compose up -d atm_greedy
- Access the demo at http://localhost:8501
- Code change: update code and run `docker compose restart atm_greedy`
- Logs: `docker compose logs -f atm_greedy --tail 100`

