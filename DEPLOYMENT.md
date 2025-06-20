# NLWeb Deployment Guide

Hướng dẫn deploy dự án NLWeb lên cloud để sử dụng widget từ WordPress mà không cần chạy local.

## Chuẩn bị trước khi deploy

### 1. Cập nhật cấu hình
Đảm bảo file `.env` trong thư mục `code/` có đầy đủ thông tin:
```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_ENDPOINT=https://api.openai.com/v1/chat/completions
```

### 2. Backup dữ liệu Qdrant
Nếu bạn có dữ liệu quan trọng trong Qdrant local (`data/db/`), hãy backup trước khi deploy.

## Phương án 1: Deploy lên Railway (Khuyến nghị)

### Bước 1: Chuẩn bị repository
```bash
git init
git add .
git commit -m "Initial commit for deployment"
```

### Bước 2: Deploy lên Railway
1. Truy cập https://railway.app
2. Đăng nhập bằng GitHub
3. Chọn "New Project" > "Deploy from GitHub repo"
4. Chọn repository chứa code NLWeb
5. Railway sẽ tự động detect và build project

### Bước 3: Cấu hình environment variables
Trong Railway dashboard:
- Vào Settings > Environment
- Thêm các biến môi trường:
  ```
  OPENAI_API_KEY=your_key_here
  OPENAI_ENDPOINT=https://api.openai.com/v1/chat/completions
  PORT=8000
  NLWEB_LOGGING_PROFILE=production
  ```

### Bước 4: Cấu hình CORS
Railway sẽ cung cấp một URL như `https://your-app.railway.app`

## Phương án 2: Deploy lên Render

### Bước 1: Tạo tài khoản Render
1. Truy cập https://render.com
2. Đăng nhập bằng GitHub

### Bước 2: Tạo Web Service
1. Chọn "New" > "Web Service"
2. Connect GitHub repository
3. Cấu hình:
   - Build Command: `pip install -r code/requirements.txt`
   - Start Command: `cd code && python app-file.py`

### Bước 3: Environment Variables
```
OPENAI_API_KEY=your_key_here
OPENAI_ENDPOINT=https://api.openai.com/v1/chat/completions
PORT=10000
PYTHON_VERSION=3.12
```

## Phương án 3: Docker + VPS

### Bước 1: Build Docker image
```bash
docker build -t nlweb-app .
```

### Bước 2: Run container
```bash
docker run -d -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -e OPENAI_ENDPOINT=https://api.openai.com/v1/chat/completions \
  -v $(pwd)/data:/app/data \
  nlweb-app
```

### Bước 3: Deploy lên VPS
- Upload image lên Docker Hub hoặc registry
- Deploy trên VPS với docker-compose

## Cấu hình CORS cho production

Sau khi deploy, bạn cần cấu hình CORS để widget có thể gọi API từ WordPress.

### Cập nhật cấu hình webserver
Tìm file cấu hình webserver và thêm CORS headers cho domain WordPress của bạn.

## Cập nhật Widget WordPress

### Cách 1: Sử dụng configuration global
Trong WordPress, trước khi load widget.js:
```html
<script>
window.NLWEB_CONFIG = {
    apiBaseUrl: 'https://your-deployed-app.railway.app', // Thay bằng URL thực tế
    title: 'My Assistant',
    welcomeMessage: '👋 Xin chào! Tôi có thể giúp gì cho bạn?'
};
</script>
<script src="https://your-deployed-app.railway.app/static/widget.js"></script>
```

### Cách 2: Sửa trực tiếp trong widget.js
Thay đổi dòng này trong widget.js:
```javascript
apiBaseUrl: 'https://your-deployed-app.railway.app'
```

## Kiểm tra deployment

1. Truy cập URL của app đã deploy
2. Test API endpoint: `https://your-app-url.com/ask?query=hello&site=all`
3. Test widget trên WordPress

## Troubleshooting

### Lỗi CORS
- Đảm bảo server có cấu hình CORS headers
- Kiểm tra domain WordPress có được whitelist

### Lỗi Qdrant
- Dữ liệu local không được sync lên cloud
- Cần re-index dữ liệu sau khi deploy

### Performance
- Railway/Render free tier có giới hạn
- Xem xét upgrade plan nếu cần

## Bảo mật

1. Không commit API keys vào git
2. Sử dụng environment variables
3. Cấu hình HTTPS
4. Giới hạn CORS origins

## Monitoring

- Kiểm tra logs trên platform deploy
- Set up health checks
- Monitor API usage và costs
