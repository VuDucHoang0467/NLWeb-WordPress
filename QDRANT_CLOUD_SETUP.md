# Qdrant Cloud Configuration for Railway Deployment

## Bước 1: Tạo Qdrant Cloud Account

1. Truy cập: https://cloud.qdrant.io
2. Đăng ký account (có free tier 1GB)
3. Tạo cluster mới

## Bước 2: Lấy thông tin kết nối

Sau khi tạo cluster, bạn sẽ có:
- **Cluster URL**: `https://xyz-abc123.qdrant.cloud`
- **API Key**: `qdrant_xxxxxxxxxxxxxxxxxxxx`

## Bước 3: Cấu hình Railway Environment Variables

Trong Railway dashboard, thêm các biến môi trường:

```
QDRANT_URL=https://your-cluster-id.qdrant.cloud
QDRANT_API_KEY=qdrant_your_api_key_here
OPENAI_API_KEY=sk-proj-your_openai_key_here
OPENAI_ENDPOINT=https://api.openai.com/v1/chat/completions
NLWEB_LOGGING_PROFILE=production
```

## Bước 4: Cập nhật config_retrieval.yaml

File `code/config/config_retrieval.yaml` cần thay đổi:

```yaml
preferred_endpoint: qdrant_url
```

## Bước 5: Kiểm tra kết nối

Sau khi deploy trên Railway:

1. Truy cập: `https://your-app.railway.app/admin/status`
2. Click "Check Database Status"
3. Xác nhận kết nối thành công

## Bước 6: Load dữ liệu RSS

1. Truy cập: `https://your-app.railway.app/admin/load-data`
2. Nhập RSS URL (ví dụ: `https://feeds.bbci.co.uk/news/rss.xml`)
3. Nhập Site Name (ví dụ: `bbc-news`)
4. Click "Load Data"

## Troubleshooting

### Lỗi kết nối Qdrant:
- Kiểm tra QDRANT_URL và QDRANT_API_KEY
- Đảm bảo cluster đang active
- Kiểm tra firewall/network settings

### Lỗi OpenAI:
- Kiểm tra OPENAI_API_KEY hợp lệ
- Đảm bảo account có credit
- Kiểm tra rate limits

### Lỗi RSS:
- URL RSS có accessible không
- Kiểm tra định dạng RSS hợp lệ
- Thử với RSS URL khác để test

## Test URLs

Một số RSS URLs để test:
- BBC News: `https://feeds.bbci.co.uk/news/rss.xml`
- CNN: `https://rss.cnn.com/rss/edition.rss`
- TechCrunch: `https://techcrunch.com/feed/`

## Monitoring

- Check logs trong Railway dashboard
- Monitor Qdrant Cloud dashboard
- Monitor OpenAI usage dashboard
