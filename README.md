# Slackers Financial Analysis AI Backend

Hệ thống backend AI phân tích tài chính tự động dành cho thị trường chứng khoán Việt Nam. Dự án ứng dụng kiến trúc **Multi-Agent** kết hợp Mô hình Ngôn ngữ Lớn (LLMs) thông qua Ollama để trích xuất dữ liệu, phân tích chỉ số và đưa ra khuyến nghị đầu tư tự động.

---

## Tính năng nổi bật (Multi-Agent System)

Hệ thống được vận hành bởi 4 Agent chuyên biệt, hoạt động độc lập và phối hợp chặt chẽ:

* **Router Agent:** Đóng vai trò như một lễ tân thông minh. Sử dụng LLM để nhận diện ý định của người dùng, trích xuất mã cổ phiếu (Ticker) từ tin nhắn văn bản. Nếu người dùng chỉ muốn trò chuyện (Small talk), Agent sẽ phản hồi thân thiện; nếu có mã cổ phiếu, yêu cầu sẽ được chuyển tuyến đến các Agent phân tích.
* **Technical Analysis (TA) Agent:** Chuyên gia phân tích kỹ thuật. Tự động lấy dữ liệu lịch sử giá qua `vnstock`, tính toán các chỉ báo (MACD, RSI, Bollinger Bands bằng `pandas_ta`) và đánh giá xung lượng, xu hướng, cũng như xác định các mốc hỗ trợ/kháng cự.
* **Fundamental Analysis (FA) Agent:** Chuyên gia phân tích cơ bản. Truy xuất dữ liệu tài chính qua `yfinance` để đánh giá định giá (P/E, P/B), hiệu quả sinh lời (ROE, ROA, Biên lợi nhuận), tốc độ tăng trưởng và tỷ suất cổ tức.
* **Investment Analysis (Manager) Agent:** Đóng vai trò Giám đốc Đầu tư (CIO). Tổng hợp báo cáo từ cả TA Agent và FA Agent để đưa ra quyết định cuối cùng (MUA / BÁN / NẮM GIỮ / QUAN SÁT) kèm theo kế hoạch giao dịch (Target, Stop-loss) bám sát thực tiễn.

---

## Công nghệ sử dụng

* **Framework:** FastAPI
* **LLM:** gpt-oss:120b-cloud từ Ollama Cloud (Tích hợp cơ chế tự động Retry với `tenacity`)
* **Dữ liệu chứng khoán:** `vnstock` (Dữ liệu VN), `yfinance` (Dữ liệu tài chính)
* **Xử lý dữ liệu:** `pandas`, `pandas-ta` (Phân tích kỹ thuật)

---

## Cấu trúc thư mục

```text
.
├── notebooks/                              # Jupyter notebooks dùng để R&D, test prompt & logic
│   ├── fundamental_analysis_agent.ipynb
│   ├── investment_analysis_agent.ipynb
│   ├── router_agent.ipynb
│   └── technical_analysis_agent.ipynb
├── src/                                    # Mã nguồn chính của API
│   ├── fundamental_analysis_agent/         # Module Phân tích cơ bản
│   ├── investment_analysis_agent/          # Module Khuyến nghị đầu tư
│   ├── ollama/                             # Cấu hình và Client kết nối với Ollama
│   ├── router_agent/                       # Module Phân loại ý định & Chat
│   ├── technical_analysis_agent/           # Module Phân tích kỹ thuật
│   └── main.py                             # Điểm khởi chạy FastAPI (Entry point)
├── test/                                   # Script kiểm thử nhanh các API Endpoints
├── requirements.txt                        # Danh sách thư viện phụ thuộc
├── .env                                    # Biến môi trường (Không push lên GitHub)
└── LICENSE                                 # Apache License 2.0
```

---

## Hướng dẫn Cài đặt & Chạy dự án

### 1. Cài đặt môi trường

Yêu cầu hệ thống đã cài đặt Python (khuyên dùng Python 3.13).

```bash
# Clone repository
git clone https://github.com/24520152-ben/WDA2026-Slackers-Financial-Analysis-Backend
cd WDA2026-Slackers-Financial-Analysis-Backend

# Cài đặt thư viện
pip install -r requirements.txt
```

### 2. Cấu hình biến môi trường

Tạo một file `.env` ở thư mục gốc của dự án và điền thông tin cấu hình Ollama Cloud:

```env
OLLAMA_API_KEY=your_api_key_here
OLLAMA_HOST=https://ollama.com
OLLAMA_MODEL=gpt-oss:120b-cloud
```

### 3. Khởi chạy Server

Chạy server FastAPI với uvicorn:

```bash
uvicorn src.main:app --reload
```

Server sẽ chạy mặc định tại: `http://127.0.0.1:8000`.
Có thể truy cập **Swagger UI** tại `http://127.0.0.1:8000/docs` để xem tài liệu API và test trực tiếp.

---

## API Endpoints chính

| Endpoint | Method | Mô tả |
| :--- | :---: | :--- |
| `/chat/` | `POST` | Giao tiếp tự nhiên với hệ thống, tự động phân luồng logic (Small talk hoặc Phân tích mã). |
| `/fundamental_analysis/` | `POST` | Yêu cầu báo cáo phân tích cơ bản chuyên sâu cho 1 mã cổ phiếu cụ thể. |
| `/technical_analysis/` | `POST` | Yêu cầu báo cáo phân tích kỹ thuật và hành vi giá cho 1 mã cổ phiếu. |
| `/investment_analysis/` | `POST` | Kích hoạt cả TA và FA chạy song song, trả về quyết định đầu tư tổng hợp. |

Có thể tham khảo các file Python trong thư mục `/test` để xem ví dụ gửi payload cụ thể.

---

## Giấy phép (License)

Dự án này được phát hành dưới giấy phép **Apache License 2.0**.
Bản quyền © 2026 thuộc về Ho Pham Quoc Bao. Xem chi tiết tại file `LICENSE`.