# 🚀 NLWeb Railway Deployment - Complete Setup Guide

## Tổng quan

Dự án này đã được cấu hình để deploy lên Railway với đầy đủ tính năng:
- ✅ Web interface để load dữ liệu RSS
- ✅ Qdrant Cloud integration 
- ✅ WordPress widget hỗ trợ
- ✅ OpenAI API integration

## 📋 Bước 1: Chuẩn bị trước khi deploy

### 1.1 Tạo Qdrant Cloud Account
```bash
# Truy cập: https://cloud.qdrant.io
# Tạo account và cluster (free tier 1GB)
# Lấy: Cluster URL và API Key
```

### 1.2 Tạo OpenAI API Key mới
```bash
# Truy cập: https://platform.openai.com/api-keys
# Tạo key mới (vì key cũ đã bị public)
# Format: sk-proj-xxxxxxxxx
```

### 1.3 Validate cấu hình local
```bash
python validate_config.py
```

## 🚀 Bước 2: Deploy lên Railway

### 2.1 Push code lên GitHub
```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### 2.2 Tạo Railway project
1. Truy cập: https://railway.app
2. Đăng nhập bằng GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Chọn repository này

### 2.3 Cấu hình Environment Variables
Trong Railway dashboard → Variables, thêm:
```
OPENAI_API_KEY=sk-proj-your_new_key_here
OPENAI_ENDPOINT=https://api.openai.com/v1/chat/completions
QDRANT_URL=https://your-cluster.qdrant.cloud
QDRANT_API_KEY=your_qdrant_api_key
NLWEB_LOGGING_PROFILE=production
PORT=8000
```

## 📊 Bước 3: Kiểm tra deployment

### 3.1 Test API
```bash
# Thay your-app-url bằng URL thực tế từ Railway
curl "https://your-app-url.railway.app/ask?query=hello&site=all"
```

### 3.2 Kiểm tra database status
```bash
# Truy cập web interface
https://your-app-url.railway.app/admin/status
```

## 📈 Bước 4: Load dữ liệu RSS

### 4.1 Sử dụng web interface
1. Truy cập: `https://your-app-url.railway.app/admin/load-data`
2. Click "Check Database Status" để kiểm tra kết nối
3. Nhập RSS URL: `https://feeds.bbci.co.uk/news/rss.xml`
4. Nhập Site Name: `bbc-news`
5. Click "Load Data"

### 4.2 Test RSS URLs
```
BBC News: https://feeds.bbci.co.uk/news/rss.xml
CNN: https://rss.cnn.com/rss/edition.rss
TechCrunch: https://techcrunch.com/feed/
```

## 🔧 Bước 5: Cấu hình WordPress Widget

### 5.1 Thêm vào WordPress
```html
<!-- Trong header.php hoặc footer.php -->
<script>
window.NLWEB_CONFIG = {
    apiBaseUrl: 'https://your-app-url.railway.app', // ⚠️ Thay URL thực tế
    title: 'Trợ lý AI',
    welcomeMessage: '👋 Xin chào! Tôi có thể giúp gì cho bạn?'
};
</script>
<script src="https://your-app-url.railway.app/static/widget.js"></script>
```

### 5.2 Hoặc sử dụng WordPress Plugin
Xem file: `widget-integration-example.html` để hướng dẫn tạo plugin.

## 🐛 Troubleshooting

### Railway deployment fails
```bash
# Kiểm tra logs trong Railway dashboard
# Đảm bảo tất cả environment variables được set
# Kiểm tra file railway.json và nixpacks.toml
```

### Qdrant connection error
```bash
# Kiểm tra QDRANT_URL format: https://xxx.qdrant.cloud
# Kiểm tra QDRANT_API_KEY hợp lệ
# Đảm bảo cluster đang active
```

### OpenAI API error
```bash
# Kiểm tra OPENAI_API_KEY mới (không phải key cũ bị public)
# Đảm bảo account có credit
# Kiểm tra rate limits
```

### Widget không hiển thị
```bash
# Kiểm tra URL trong NLWEB_CONFIG
# Kiểm tra CORS headers (đã được cấu hình sẵn)
# Xem Console browser để debug
```

## 📁 Cấu trúc files quan trọng

```
├── railway.json              # Railway deployment config
├── nixpacks.toml             # Nixpacks build config
├── start.sh                  # Start script cho Railway
├── requirements.txt          # Python dependencies
├── validate_config.py        # Validation script
├── QDRANT_CLOUD_SETUP.md    # Hướng dẫn Qdrant Cloud
├── code/
│   ├── webserver/
│   │   └── data_loader.py    # Web interface cho data loading
│   └── config/
│       └── config_retrieval.yaml  # Cấu hình database
└── static/
    └── widget.js             # WordPress widget
```

## 🎯 Workflow hoàn chỉnh

1. **Local development**: Sử dụng Qdrant local + OpenAI
2. **Railway deployment**: Sử dụng Qdrant Cloud + OpenAI
3. **Data loading**: Web interface thay vì command line
4. **WordPress integration**: Widget tự động kết nối cloud

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Chạy `python validate_config.py` để kiểm tra cấu hình
2. Kiểm tra Railway logs
3. Test API endpoints manually
4. Xem file QDRANT_CLOUD_SETUP.md để setup chi tiết

---

**🎉 Chúc mừng! Bây giờ bạn có thể sử dụng NLWeb widget trên WordPress mà không cần chạy server local!** 🚀
