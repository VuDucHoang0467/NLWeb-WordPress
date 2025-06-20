"""
Data loading endpoint for Railway deployment
Allows loading RSS data via web interface instead of command line
"""

import asyncio
import json
from urllib.parse import unquote
from webserver.static_file_handler import send_static_file

async def handle_data_load_request(request_path, query_params):
    """Handle data loading requests"""
    
    if request_path == "/admin/load-data":
        # Serve the data loading interface
        return await serve_data_load_interface()
    
    elif request_path == "/admin/status":
        # Handle admin status check
        return await handle_admin_status(query_params)
    
    elif request_path == "/api/load-rss":
        # Handle RSS loading
        return await handle_rss_load(query_params)
    
    return None

async def serve_data_load_interface():
    """Serve the data loading web interface"""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>NLWeb Data Loader</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .form-group { margin: 15px 0; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 4px; }
            .error { background: #f8d7da; color: #721c24; }
            .success { background: #d4edda; color: #155724; }
        </style>
    </head>    <body>
        <h1>🔄 NLWeb Data Loader</h1>
        <p>Load RSS data into your Qdrant Cloud database</p>
        
        <!-- Status Section -->
        <div class="form-group">
            <button type="button" onclick="checkStatus()">🔍 Check Database Status</button>
        </div>
        <div id="statusResult"></div>
        
        <!-- Data Loading Form -->
        <form id="loadForm">
            <div class="form-group">
                <label for="rssUrl">RSS URL:</label>
                <input type="url" id="rssUrl" name="rssUrl" required 
                       placeholder="https://example.com/rss.xml">
            </div>
            
            <div class="form-group">
                <label for="siteName">Site Name:</label>
                <input type="text" id="siteName" name="siteName" required 
                       placeholder="example-site">
            </div>
            
            <button type="submit">🚀 Load Data</button>
        </form>
        
        <div id="result"></div>
          <script>
        // Check database status
        async function checkStatus() {
            const statusDiv = document.getElementById('statusResult');
            statusDiv.innerHTML = '<div class="result">⏳ Checking database status...</div>';
            
            try {
                const response = await fetch('/admin/status');
                const data = await response.json();
                
                if (data.success) {
                    const info = data.data;
                    statusDiv.innerHTML = `
                        <div class="result success">
                            ✅ Database Status: ${info.database}<br>
                            📊 Type: ${info.type}<br>
                            📁 Collections: ${info.collections.length || 0}<br>
                            📄 Total Documents: ${info.total_documents || 'N/A'}
                        </div>
                    `;
                } else {
                    statusDiv.innerHTML = `<div class="result error">❌ Error: ${data.error}</div>`;
                }
            } catch (error) {
                statusDiv.innerHTML = `<div class="result error">❌ Network error: ${error.message}</div>`;
            }
        }
        
        // Load RSS data
        document.getElementById('loadForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const rssUrl = document.getElementById('rssUrl').value;
            const siteName = document.getElementById('siteName').value;
            const resultDiv = document.getElementById('result');
            
            resultDiv.innerHTML = '<div class="result">⏳ Loading data...</div>';
            
            try {
                const response = await fetch(`/api/load-rss?rss_url=${encodeURIComponent(rssUrl)}&site_name=${encodeURIComponent(siteName)}`);
                const data = await response.json();
                
                if (data.success) {
                    resultDiv.innerHTML = `<div class="result success">✅ Success! Loaded ${data.count} items from ${siteName}</div>`;
                } else {
                    resultDiv.innerHTML = `<div class="result error">❌ Error: ${data.error}</div>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<div class="result error">❌ Network error: ${error.message}</div>`;
            }
        });
        </script>
    </body>
    </html>
    """
    
    return {
        'status': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': html_content
    }

async def handle_rss_load(query_params):
    """Handle RSS loading request"""
    
    try:
        rss_url = query_params.get('rss_url', [''])[0]
        site_name = query_params.get('site_name', [''])[0]
        
        if not rss_url or not site_name:
            return {
                'status': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'success': False, 'error': 'Missing rss_url or site_name'})
            }
        
        # Import and run the db_load functionality
        from tools.db_load import load_rss_data
        
        # Load the data
        result = await load_rss_data(rss_url, site_name)
        
        return {
            'status': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'success': True, 
                'count': result.get('count', 0),
                'message': f'Successfully loaded data from {site_name}'
            })
        }
        
    except Exception as e:
        return {
            'status': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'success': False, 'error': str(e)})
        }

async def handle_admin_status(query_params):
    """Handle admin status check"""
    try:
        # Check database connection
        from retrieval.retriever import get_vector_db_client
        client = get_vector_db_client()
        
        # Get database info
        status_info = {
            'database': 'connected',
            'type': 'qdrant',
            'collections': [],
            'total_documents': 0
        }
        
        try:
            # Try to get collections info
            collections_info = await client.get_collections_info()
            status_info['collections'] = collections_info
        except Exception as e:
            status_info['database'] = f'error: {str(e)}'
        
        return {
            'status': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'success': True, 'data': status_info})
        }
        
    except Exception as e:
        return {
            'status': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'success': False, 'error': str(e)})
        }
