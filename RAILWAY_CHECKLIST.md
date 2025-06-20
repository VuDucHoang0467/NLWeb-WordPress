# 🚀 Railway Deployment Checklist

## ✅ Completed Steps:
- [x] Code pushed to GitHub
- [x] Railway project created

## 📋 Next Steps:

### 1. Configure Environment Variables in Railway
```
OPENAI_API_KEY=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
OPENAI_ENDPOINT=https://api.openai.com/v1/chat/completions
NLWEB_LOGGING_PROFILE=production
PORT=8000
```

### 2. Test Deployment
- [ ] Check build logs in Railway dashboard
- [ ] Get public URL from Railway
- [ ] Test API endpoint: `https://your-url.railway.app/ask?query=hello&site=all`
- [ ] Verify CORS headers work

### 3. Update WordPress Widget
After getting Railway URL, update your WordPress with:

```html
<script>
window.NLWEB_CONFIG = {
    apiBaseUrl: 'https://your-railway-url.railway.app', // Replace with actual URL
    title: 'Trợ lý AI',
    welcomeMessage: '👋 Xin chào! Tôi có thể giúp gì cho bạn?'
};
</script>
<script src="https://your-railway-url.railway.app/static/widget.js"></script>
```

### 4. Final Testing
- [ ] Widget appears on WordPress site
- [ ] Chat functionality works
- [ ] Responses are generated correctly

## 🔧 Common Issues:

### Build Fails:
- Check Railway build logs
- Ensure requirements.txt is in code/ directory
- Verify Python version compatibility

### Environment Variables:
- Make sure OPENAI_API_KEY is set correctly
- Check all required variables are present

### CORS Issues:
- Already configured in the code
- Should work automatically

### Performance:
- Railway free tier has limitations
- Consider upgrading if needed

## 📞 Support:
If you encounter issues, check:
1. Railway dashboard logs
2. GitHub repository structure
3. Environment variables configuration
