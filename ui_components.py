class UIRenderer:
    def __init__(self):
        self.app_name = "Consistly"
        self.app_tagline = "Ensure Stylistic Consistency Across All Your Content"
        self.linkedin_url = "https://www.linkedin.com/in/ashutosh-gautam-3747b3179/"
    
    def render_main_page(self) -> str:
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Consistly - Content Style Consistency</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 20px; background: #0f0f0f; color: #fff; }
                .container { max-width: 1200px; margin: 0 auto; }
                .hero { text-align: center; padding: 60px 0; }
                .hero h1 { font-size: 3rem; margin-bottom: 20px; background: linear-gradient(135deg, #007aff 0%, #0056cc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
                .card { background: rgba(26, 26, 26, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 30px; margin: 20px 0; }
                .btn { background: linear-gradient(135deg, #007aff 0%, #0056cc 100%); color: white; border: none; padding: 15px 30px; border-radius: 12px; font-weight: 600; cursor: pointer; }
                .btn:hover { transform: translateY(-2px); }
                textarea { width: 100%; min-height: 120px; padding: 15px; border: 2px solid rgba(255, 255, 255, 0.1); border-radius: 12px; background: #2a2a2a; color: #fff; font-family: inherit; }
                textarea:focus { outline: none; border-color: #007aff; }
                .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
                @media (max-width: 768px) { .grid { grid-template-columns: 1fr; } }
                .warning { background: rgba(255, 193, 7, 0.1); border: 1px solid rgba(255, 193, 7, 0.3); border-radius: 12px; padding: 15px; margin: 20px 0; color: #ffc107; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="hero">
                    <h1>Consistly</h1>
                    <p style="font-size: 1.2rem; color: #b0b0b0;">Ensure Stylistic Consistency Across All Your Content</p>
                    <div class="warning">
                        <strong>⚠️ Privacy Notice:</strong> This cloud version processes content on our servers. 
                        For 100% privacy, use our <a href="https://github.com/ashutoshgautams/Consistly" style="color: #ffc107;">local setup</a>.
                    </div>
                </div>
                
                <div class="grid">
                    <div class="card">
                        <h3>📚 Reference Content</h3>
                        <p>Provide examples of your best content to establish style patterns.</p>
                        <textarea id="refText1" placeholder="Paste your reference content here..."></textarea>
                        <button class="btn" onclick="addReference()">+ Add Another Reference</button>
                    </div>
                    
                    <div class="card">
                        <h3>✏️ Draft Content</h3>
                        <p>Add the content that needs style consistency.</p>
                        <textarea id="draftText" placeholder="Paste your draft content here..." style="min-height: 200px;"></textarea>
                    </div>
                </div>
                
                <div class="card" style="text-align: center;">
                    <h3>✨ Transform Content</h3>
                    <p>Generate style-consistent content based on your patterns.</p>
                    <button class="btn" onclick="generateEdit()" id="generateBtn" style="font-size: 1.1rem; padding: 20px 40px;">
                        🎯 Transform Content
                    </button>
                    <div id="loading" style="display: none; margin: 20px 0; color: #007aff;">
                        <p>🧠 Analyzing patterns and transforming content...</p>
                    </div>
                </div>
                
                <div class="card">
                    <h3>📝 Transformed Content</h3>
                    <textarea id="result" placeholder="Your transformed content will appear here..." readonly style="min-height: 300px;"></textarea>
                    <button class="btn" onclick="copyResult()">📋 Copy Content</button>
                </div>
            </div>
            
            <script>
                let referenceCount = 1;
                
                function addReference() {
                    referenceCount++;
                    const container = document.querySelector('.card');
                    const newTextarea = document.createElement('textarea');
                    newTextarea.id = 'refText' + referenceCount;
                    newTextarea.placeholder = 'Paste another reference content here...';
                    newTextarea.style.marginTop = '15px';
                    container.insertBefore(newTextarea, container.querySelector('button'));
                }
                
                async function generateEdit() {
                    const references = [];
                    for (let i = 1; i <= referenceCount; i++) {
                        const text = document.getElementById('refText' + i)?.value.trim();
                        if (text) references.push(text);
                    }
                    
                    const draft = document.getElementById('draftText').value.trim();
                    
                    if (references.length === 0) {
                        alert('Please add at least one reference content');
                        return;
                    }
                    
                    if (!draft) {
                        alert('Please add your draft content');
                        return;
                    }
                    
                    const btn = document.getElementById('generateBtn');
                    const loading = document.getElementById('loading');
                    const result = document.getElementById('result');
                    
                    btn.disabled = true;
                    loading.style.display = 'block';
                    result.value = '';
                    
                    try {
                        const response = await fetch('/api/generate-edit', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                reference_articles: references,
                                draft_content: draft
                            })
                        });
                        
                        if (!response.ok) {
                            const error = await response.json();
                            throw new Error(error.detail || 'Generation failed');
                        }
                        
                        const data = await response.json();
                        result.value = data.data.edited_article;
                        result.scrollIntoView({ behavior: 'smooth' });
                        
                    } catch (error) {
                        alert('Error: ' + error.message);
                        result.value = 'Generation failed: ' + error.message;
                    } finally {
                        btn.disabled = false;
                        loading.style.display = 'none';
                    }
                }
                
                function copyResult() {
                    const result = document.getElementById('result');
                    if (!result.value) {
                        alert('Nothing to copy');
                        return;
                    }
                    result.select();
                    document.execCommand('copy');
                    alert('Content copied to clipboard!');
                }
                
                // Check health on load
                fetch('/api/health')
                    .then(r => r.json())
                    .then(data => {
                        if (data.ai_service.status === 'loading') {
                            document.getElementById('generateBtn').innerHTML = '⏳ AI Starting Up...';
                            document.getElementById('generateBtn').disabled = true;
                            
                            // Check again in 30 seconds
                            setTimeout(() => location.reload(), 30000);
                        }
                    })
                    .catch(() => {});
            </script>
        </body>
        </html>
        """
