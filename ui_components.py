"""
UI Components Module

Handles rendering of HTML templates and UI components
for the Consistly application.
"""

from typing import Dict, Any


class UIRenderer:
    """
    Handles rendering of UI components and templates.
    """
    
    def __init__(self):
        """Initialize the UI renderer."""
        self.app_name = "Consistly"
        self.app_tagline = "Open Source for Stylistic Consistency"
        self.app_description = "Transform any draft to match your established writing style and brand voice"
        self.linkedin_url = "https://www.linkedin.com/in/ashutosh-gautam-3747b3179/"
    
    def render_main_page(self) -> str:
        """
        Render the main application page.
        """
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.app_name} - Stylistic Consistency for Marketing & Documentation</title>
            <meta name="description" content="Ensure stylistic consistency across all your marketing content and documentation. Transform any draft to match your established writing style.">
            
            <!-- Fonts -->
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            
            <!-- Icons -->
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
            
            <!-- Styles -->
            {self._get_styles()}
        </head>
        <body>
            {self._get_hero_section()}
            
            <div class="container">
                {self._get_value_props()}
                {self._get_main_interface()}
                {self._get_generate_section()}
                {self._get_output_section()}
                {self._get_contact_section()}
            </div>
            
            {self._get_scripts()}
        </body>
        </html>
        """
        return html_content
    
    def _get_styles(self) -> str:
        """Get CSS styles."""
        return """
        <style>
        :root {
          /* Dark Modern Theme with Electric Blue Accents */
          --primary-gradient: linear-gradient(135deg, #007aff 0%, #0056cc 100%);
          --primary-color: #007aff;
          --primary-light: #40a0ff;
          --primary-dark: #0056cc;
          --accent-gradient: linear-gradient(135deg, #5ac8fa 0%, #007aff 100%);
          --accent-color: #5ac8fa;
          
          --bg-primary: #0f0f0f;
          --bg-secondary: #1a1a1a;
          --bg-tertiary: #2a2a2a;
          --bg-card: rgba(26, 26, 26, 0.8);
          --bg-card-hover: rgba(42, 42, 42, 0.9);
          
          --text-primary: #ffffff;
          --text-secondary: #b0b0b0;
          --text-muted: #707070;
          --text-accent: #007aff;
          
          --border-primary: rgba(0, 122, 255, 0.25);
          --border-secondary: rgba(255, 255, 255, 0.1);
          
          --success-color: #4caf50;
          --error-color: #f44336;
          --warning-color: #ff9800;
          
          --spacing-xs: 0.25rem;
          --spacing-sm: 0.5rem;
          --spacing-md: 1rem;
          --spacing-lg: 1.5rem;
          --spacing-xl: 2rem;
          --spacing-2xl: 3rem;
          
          --radius-sm: 0.5rem;
          --radius-md: 0.75rem;
          --radius-lg: 1rem;
          --radius-xl: 1.5rem;
          
          --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
          --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
          --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
          --shadow-glow: 0 0 20px rgba(0, 122, 255, 0.4);
          
          --transition-fast: 0.2s ease;
          --transition-normal: 0.3s ease;
          --transition-slow: 0.5s ease;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
          background: var(--bg-primary);
          color: var(--text-primary);
          line-height: 1.6;
          min-height: 100vh;
          overflow-x: hidden;
          font-feature-settings: 'kern' 1;
          -webkit-font-smoothing: antialiased;
          -moz-osx-font-smoothing: grayscale;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-secondary); }
        ::-webkit-scrollbar-thumb { background: var(--primary-color); border-radius: 4px; }
        
        .container { 
          max-width: 1200px; 
          margin: 0 auto; 
          padding: var(--spacing-lg); 
        }
        
        .grid-2 { 
          display: grid; 
          grid-template-columns: 1fr 1fr; 
          gap: var(--spacing-xl); 
        }
        
        .grid-full { grid-column: 1 / -1; }
        
        /* Hero Section */
        .hero {
          background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
          padding: var(--spacing-2xl) 0;
          position: relative;
          overflow: hidden;
        }
        
        .hero::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: radial-gradient(circle at 30% 30%, rgba(0, 122, 255, 0.08) 0%, transparent 50%);
          pointer-events: none;
        }
        
        .hero-content {
          position: relative;
          z-index: 1;
          text-align: center;
        }
        
        .brand-badge {
          display: inline-flex;
          align-items: center;
          gap: var(--spacing-sm);
          background: var(--primary-gradient);
          color: var(--text-primary);
          padding: var(--spacing-sm) var(--spacing-lg);
          border-radius: 50px;
          font-weight: 600;
          font-size: 0.9rem;
          margin-bottom: var(--spacing-lg);
          box-shadow: var(--shadow-glow);
        }
        
        .hero-title {
          font-size: 4rem;
          font-weight: 900;
          margin-bottom: var(--spacing-md);
          letter-spacing: -0.02em;
          background: var(--primary-gradient);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }
        
        .hero-subtitle {
          font-size: 1.5rem;
          font-weight: 600;
          color: var(--text-secondary);
          margin-bottom: var(--spacing-md);
          max-width: 600px;
          margin-left: auto;
          margin-right: auto;
        }
        
        .hero-description {
          font-size: 1.1rem;
          color: var(--text-muted);
          max-width: 700px;
          margin: 0 auto var(--spacing-xl);
          line-height: 1.7;
        }
        
        /* Value Propositions */
        .value-props {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: var(--spacing-lg);
          margin: var(--spacing-2xl) 0;
        }
        
        .value-prop {
          background: var(--bg-card);
          backdrop-filter: blur(20px);
          border: 1px solid var(--border-secondary);
          border-radius: var(--radius-lg);
          padding: var(--spacing-xl);
          text-align: center;
          transition: all var(--transition-normal);
          position: relative;
          overflow: hidden;
        }
        
        .value-prop::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 3px;
          background: var(--primary-gradient);
        }
        
        .value-prop:hover {
          transform: translateY(-8px);
          box-shadow: var(--shadow-lg);
          border-color: var(--border-primary);
        }
        
        .value-prop-icon {
          width: 60px;
          height: 60px;
          background: var(--primary-gradient);
          border-radius: var(--radius-lg);
          display: flex;
          align-items: center;
          justify-content: center;
          margin: 0 auto var(--spacing-md);
          font-size: 1.8rem;
          color: var(--text-primary);
          box-shadow: var(--shadow-glow);
        }
        
        .value-prop-title {
          font-size: 1.2rem;
          font-weight: 700;
          color: var(--text-primary);
          margin-bottom: var(--spacing-sm);
        }
        
        .value-prop-desc {
          color: var(--text-secondary);
          font-size: 0.95rem;
          line-height: 1.6;
        }
        
        /* Cards */
        .card {
          background: var(--bg-card);
          backdrop-filter: blur(20px);
          border: 1px solid var(--border-secondary);
          border-radius: var(--radius-xl);
          padding: var(--spacing-xl);
          transition: all var(--transition-normal);
          position: relative;
          overflow: hidden;
        }
        
        .card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 4px;
          background: var(--primary-gradient);
        }
        
        .card:hover {
          transform: translateY(-5px);
          box-shadow: var(--shadow-lg);
          background: var(--bg-card-hover);
          border-color: var(--border-primary);
        }
        
        .card-header {
          display: flex;
          align-items: flex-start;
          gap: var(--spacing-lg);
          margin-bottom: var(--spacing-xl);
        }
        
        .card-icon {
          width: 56px;
          height: 56px;
          background: var(--primary-gradient);
          border-radius: var(--radius-lg);
          display: flex;
          align-items: center;
          justify-content: center;
          color: var(--text-primary);
          font-size: 1.6rem;
          flex-shrink: 0;
          box-shadow: var(--shadow-glow);
        }
        
        .step-badge {
          background: var(--accent-color);
          color: var(--text-primary);
          padding: 0.25rem 0.75rem;
          border-radius: 50px;
          font-size: 0.8rem;
          font-weight: 700;
          margin-bottom: var(--spacing-sm);
          display: inline-block;
        }
        
        .card-title {
          font-size: 1.4rem;
          font-weight: 700;
          color: var(--text-primary);
          margin: 0 0 var(--spacing-sm) 0;
        }
        
        .card-description {
          color: var(--text-secondary);
          font-size: 1rem;
          line-height: 1.6;
          margin: 0;
        }
        
        /* Form Elements */
        .input-group {
          margin-bottom: var(--spacing-lg);
        }
        
        .input-label {
          display: block;
          margin-bottom: var(--spacing-sm);
          color: var(--text-primary);
          font-weight: 600;
          font-size: 0.95rem;
        }
        
        .file-upload {
          position: relative;
          width: 100%;
        }
        
        .file-upload input[type="file"] {
          position: absolute;
          opacity: 0;
          width: 100%;
          height: 100%;
          cursor: pointer;
          z-index: 2;
        }
        
        .file-upload-label {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: var(--spacing-sm);
          padding: var(--spacing-lg);
          background: var(--primary-gradient);
          color: var(--text-primary);
          border-radius: var(--radius-lg);
          cursor: pointer;
          transition: all var(--transition-normal);
          font-weight: 600;
          min-height: 60px;
          border: 2px solid transparent;
        }
        
        .file-upload-label:hover {
          transform: translateY(-2px);
          box-shadow: var(--shadow-glow);
          border-color: var(--primary-light);
        }
        
        .textarea-input {
          width: 100%;
          min-height: 120px;
          padding: var(--spacing-lg);
          border: 2px solid var(--border-secondary);
          border-radius: var(--radius-lg);
          font-family: inherit;
          font-size: 0.95rem;
          background: var(--bg-tertiary);
          color: var(--text-primary);
          resize: vertical;
          transition: all var(--transition-normal);
          line-height: 1.6;
        }
        
        .textarea-input:focus {
          outline: none;
          border-color: var(--primary-color);
          box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.2);
          background: var(--bg-secondary);
        }
        
        .textarea-input::placeholder {
          color: var(--text-muted);
        }
        
        /* Buttons */
        .btn {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          gap: var(--spacing-sm);
          padding: var(--spacing-md) var(--spacing-lg);
          border: none;
          border-radius: var(--radius-lg);
          font-weight: 600;
          font-size: 0.95rem;
          cursor: pointer;
          transition: all var(--transition-normal);
          text-decoration: none;
          min-height: 48px;
          position: relative;
          overflow: hidden;
        }
        
        .btn-primary {
          background: var(--primary-gradient);
          color: var(--text-primary);
          box-shadow: var(--shadow-md);
        }
        
        .btn-primary:hover {
          transform: translateY(-2px);
          box-shadow: var(--shadow-glow);
        }
        
        .btn-secondary {
          background: rgba(0, 122, 255, 0.1);
          color: var(--primary-color);
          border: 2px solid var(--border-primary);
        }
        
        .btn-secondary:hover {
          background: rgba(0, 122, 255, 0.2);
          border-color: var(--primary-color);
        }
        
        .btn-large {
          padding: var(--spacing-lg) var(--spacing-2xl);
          font-size: 1.2rem;
          font-weight: 700;
          border-radius: var(--radius-xl);
          min-height: 64px;
        }
        
        .btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
          transform: none !important;
        }
        
        /* Reference Items */
        .reference-item {
          margin-bottom: var(--spacing-lg);
          padding: var(--spacing-lg);
          background: rgba(0, 122, 255, 0.04);
          border: 1px solid var(--border-primary);
          border-radius: var(--radius-lg);
          position: relative;
        }
        
        .reference-number {
          position: absolute;
          top: -12px;
          left: var(--spacing-lg);
          background: var(--primary-gradient);
          color: var(--text-primary);
          width: 28px;
          height: 28px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.85rem;
          font-weight: 700;
          box-shadow: var(--shadow-glow);
        }
        
        .divider {
          text-align: center;
          margin: var(--spacing-lg) 0;
          color: var(--text-muted);
          font-size: 0.9rem;
          position: relative;
        }
        
        .divider::before {
          content: '';
          position: absolute;
          top: 50%;
          left: 0;
          right: 0;
          height: 1px;
          background: var(--border-secondary);
          z-index: 1;
        }
        
        .divider span {
          background: var(--bg-card);
          padding: 0 var(--spacing-lg);
          position: relative;
          z-index: 2;
        }
        
        /* Status Messages */
        .status {
          padding: var(--spacing-md);
          border-radius: var(--radius-lg);
          margin-top: var(--spacing-md);
          font-size: 0.9rem;
          font-weight: 500;
          display: flex;
          align-items: center;
          gap: var(--spacing-sm);
          border: 1px solid;
        }
        
        .status.success {
          background: rgba(76, 175, 80, 0.1);
          color: var(--success-color);
          border-color: rgba(76, 175, 80, 0.3);
        }
        
        .status.error {
          background: rgba(244, 67, 54, 0.1);
          color: var(--error-color);
          border-color: rgba(244, 67, 54, 0.3);
        }
        
        /* Generate Section */
        .generate-section {
          text-align: center;
          margin: var(--spacing-2xl) 0;
          padding: var(--spacing-2xl);
          background: var(--bg-card);
          border: 1px solid var(--border-secondary);
          border-radius: var(--radius-xl);
          position: relative;
        }
        
        .generate-section::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 4px;
          background: var(--accent-gradient);
        }
        
        .generate-title {
          font-size: 2rem;
          font-weight: 800;
          color: var(--text-primary);
          margin-bottom: var(--spacing-md);
          display: flex;
          align-items: center;
          justify-content: center;
          gap: var(--spacing-md);
        }
        
        .generate-subtitle {
          font-size: 1.1rem;
          color: var(--text-secondary);
          margin-bottom: var(--spacing-xl);
          max-width: 600px;
          margin-left: auto;
          margin-right: auto;
        }
        
        .loading {
          display: none;
          text-align: center;
          padding: var(--spacing-xl);
          margin: var(--spacing-lg) 0;
        }
        
        .loading.show { display: block; }
        
        .loading-content {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: var(--spacing-lg);
          background: rgba(233, 30, 99, 0.1);
          padding: var(--spacing-xl);
          border-radius: var(--radius-lg);
          border: 1px solid var(--border-primary);
        }
        
        .loading-icon {
          font-size: 2rem;
          color: var(--primary-color);
          animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.7; transform: scale(1.1); }
        }
        
        .loading-text {
          color: var(--text-primary);
          font-weight: 600;
        }
        
        /* Output Section */
        .output-section {
          background: var(--bg-card);
          border: 1px solid var(--border-secondary);
          border-radius: var(--radius-xl);
          padding: var(--spacing-xl);
          position: relative;
          margin: var(--spacing-2xl) 0;
        }
        
        .output-section::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 4px;
          background: var(--primary-gradient);
        }
        
        .output-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: var(--spacing-lg);
          flex-wrap: wrap;
          gap: var(--spacing-md);
        }
        
        .output-textarea {
          width: 100%;
          min-height: 300px;
          padding: var(--spacing-lg);
          border: 2px solid var(--border-secondary);
          border-radius: var(--radius-lg);
          font-family: inherit;
          font-size: 1rem;
          line-height: 1.7;
          background: var(--bg-tertiary);
          color: var(--text-primary);
          resize: vertical;
          transition: all var(--transition-normal);
        }
        
        .output-textarea:focus {
          outline: none;
          border-color: var(--primary-color);
          box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.2);
        }
        
        .copy-btn {
          position: relative;
        }
        
        .copy-success {
          position: absolute;
          top: -45px;
          right: 0;
          background: var(--success-color);
          color: var(--text-primary);
          padding: var(--spacing-sm) var(--spacing-md);
          border-radius: var(--radius-lg);
          font-size: 0.85rem;
          font-weight: 600;
          opacity: 0;
          transform: translateY(10px);
          transition: all var(--transition-normal);
          z-index: 10;
          white-space: nowrap;
          box-shadow: var(--shadow-md);
        }
        
        .copy-success.show {
          opacity: 1;
          transform: translateY(0);
        }
        
        /* Contact Section */
        .contact-section {
          background: var(--bg-card);
          border: 1px solid var(--border-secondary);
          border-radius: var(--radius-xl);
          padding: var(--spacing-2xl);
          text-align: center;
          margin-top: var(--spacing-2xl);
          position: relative;
        }
        
        .contact-section::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 4px;
          background: var(--accent-gradient);
        }
        
        .contact-title {
          color: var(--text-primary);
          font-size: 1.8rem;
          font-weight: 700;
          margin-bottom: var(--spacing-md);
          display: flex;
          align-items: center;
          justify-content: center;
          gap: var(--spacing-md);
        }
        
        .contact-description {
          color: var(--text-secondary);
          font-size: 1.1rem;
          margin-bottom: var(--spacing-xl);
          line-height: 1.6;
          max-width: 600px;
          margin-left: auto;
          margin-right: auto;
        }
        
        .linkedin-link, .github-link {
          display: inline-flex;
          align-items: center;
          gap: var(--spacing-md);
          color: var(--text-primary);
          background: var(--primary-gradient);
          text-decoration: none;
          font-weight: 600;
          font-size: 1rem;
          padding: var(--spacing-md) var(--spacing-xl);
          border-radius: var(--radius-lg);
          transition: all var(--transition-normal);
          box-shadow: var(--shadow-md);
          min-width: 180px;
          justify-content: center;
        }
        
        .github-link {
          background: linear-gradient(135deg, #333 0%, #24292e 100%);
        }
        
        .linkedin-link:hover, .github-link:hover {
          transform: translateY(-2px);
          box-shadow: var(--shadow-glow);
        }
        
        .footer-info {
          padding-top: var(--spacing-xl);
          border-top: 1px solid var(--border-secondary);
        }
        
        .footer-text {
          color: var(--text-secondary);
          font-size: 0.95rem;
          margin: 0 0 var(--spacing-sm) 0;
        }
        
        .footer-subtext {
          color: var(--text-muted);
          font-size: 0.85rem;
          margin: 0;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
          .grid-2 { grid-template-columns: 1fr; gap: var(--spacing-lg); }
          .hero-title { font-size: 2.5rem; }
          .generate-title { font-size: 1.5rem; }
          .value-props { grid-template-columns: 1fr; }
          .card-header { flex-direction: column; text-align: center; }
          .output-header { flex-direction: column; align-items: stretch; }
          .container { padding: var(--spacing-md); }
          .btn-large { padding: var(--spacing-md) var(--spacing-lg); font-size: 1rem; }
        }
        </style>
        """
    
    def _get_hero_section(self) -> str:
        """Get hero section HTML."""
        return f"""
        <div class="hero">
            <div class="container">
                <div class="hero-content">
                    <div class="brand-badge">
                        <i class="fas fa-check-circle"></i>
                        Content Consistency Made Simple
                    </div>
                    
                    <h1 class="hero-title">{self.app_name}</h1>
                    <p class="hero-subtitle">{self.app_tagline}</p>
                    
                    <div style="background: rgba(255, 193, 7, 0.1); border: 1px solid rgba(255, 193, 7, 0.3); border-radius: var(--radius-lg); padding: var(--spacing-md); margin: var(--spacing-lg) auto; max-width: 700px;">
                        <p style="color: #ffc107; font-weight: 600; margin: 0; font-size: 0.95rem; display: flex; align-items: center; gap: var(--spacing-sm);">
                            <i class="fas fa-shield-alt"></i>
                            <strong>Privacy Notice:</strong> <p>This cloud version processes content on our servers. </p>
                            <p>For 100% privacy, use our <a href="https://github.com/ashutoshgautam/consistly#setup" target="_blank" style="color: #ffc107; text-decoration: underline; font-weight: 700;">local setup guide</a></p>.
                        </p>
                    </div>
                    
                    <p class="hero-description">
                        Transform any draft to match your established writing patterns. Perfect for marketing teams, 
                        content creators, and organizations who need consistent voice across all communications. 
                        Upload your best-performing content as examples, and we'll help maintain that quality standard.
                    </p>
                </div>
            </div>
        </div>
        """
    
    def _get_value_props(self) -> str:
        """Get value propositions HTML."""
        return """
        <div class="value-props">
            <div class="value-prop">
                <div class="value-prop-icon">
                    <i class="fas fa-bullseye"></i>
                </div>
                <h3 class="value-prop-title">Style Pattern Learning</h3>
                <p class="value-prop-desc">
                    Analyzes your reference content to understand tone, structure, vocabulary, and approach patterns unique to your brand.
                </p>
            </div>
            
            <div class="value-prop">
                <div class="value-prop-icon">
                    <i class="fas fa-shield-alt"></i>
                </div>
                <h3 class="value-prop-title">100% Private & Local</h3>
                <p class="value-prop-desc">
                    Your content never leaves your device. Everything runs locally using open-source AI models for complete privacy.
                </p>
            </div>
            
            <div class="value-prop">
                <div class="value-prop-icon">
                    <i class="fas fa-rocket"></i>
                </div>
                <h3 class="value-prop-title">Marketing & Docs Focus</h3>
                <p class="value-prop-desc">
                    Specifically designed for marketing content, documentation, and business communications where consistency matters most.
                </p>
            </div>
            
            <div class="value-prop">
                <div class="value-prop-icon">
                    <i class="fas fa-cogs"></i>
                </div>
                <h3 class="value-prop-title">No Training Required</h3>
                <p class="value-prop-desc">
                    Works with any writing style out of the box. No complex setup, model training, or technical configuration needed.
                </p>
            </div>
        </div>
        """
    
    def _get_main_interface(self) -> str:
        """Get main interface HTML."""
        return f"""
        <div style="margin: var(--spacing-2xl) 0;">
            <div style="text-align: center; margin-bottom: var(--spacing-2xl);">
                <h2 style="font-size: 2.5rem; font-weight: 800; color: var(--text-primary); margin-bottom: var(--spacing-md);">
                    <i class="fas fa-play-circle" style="color: var(--primary-color);"></i>
                    How It Works
                </h2>
                <p style="font-size: 1.2rem; color: var(--text-secondary); max-width: 600px; margin: 0 auto;">
                    Three simple steps to transform any draft into content that matches your established style.
                </p>
            </div>
            
            <div class="grid-2">
                {self._get_reference_section()}
                {self._get_draft_section()}
            </div>
        </div>
        """

    def _get_reference_section(self) -> str:
        """Get reference section HTML."""
        return """
        <div class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-graduation-cap"></i>
                </div>
                <div>
                    <div class="step-badge">Step 1</div>
                    <h3 class="card-title">Upload Reference Content</h3>
                    <p class="card-description">
                        Provide 3-5 examples of your best content. These establish the style patterns, 
                        tone, and structure that Consistly will learn from and replicate.
                    </p>
                </div>
            </div>
            
            <div id="referenceContainer">
                <div class="reference-item">
                    <div class="reference-number">1</div>
                    <div class="input-group">
                        <label class="input-label">Reference Content 1</label>
                        <div class="file-upload">
                            <input type="file" id="refFile1" accept=".txt,.docx,.pdf">
                            <div class="file-upload-label">
                                <i class="fas fa-upload"></i>
                                Upload File (.txt, .docx, .pdf)
                            </div>
                        </div>
                        <div class="divider"><span>or</span></div>
                        <textarea class="textarea-input" id="refText1" 
                                 placeholder="Paste your reference content here..."></textarea>
                    </div>
                </div>
            </div>
            
            <button class="btn btn-secondary" onclick="addReferenceField()">
                <i class="fas fa-plus"></i> Add Another Reference
            </button>
            
            <div id="referenceStatus"></div>
        </div>
        """

    def _get_draft_section(self) -> str:
        """Get draft section HTML."""
        return """
        <div class="card">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-edit"></i>
                </div>
                <div>
                    <div class="step-badge">Step 2</div>
                    <h3 class="card-title">Add Your Draft</h3>
                    <p class="card-description">
                        Upload or paste the content that needs consistency improvements. 
                        This could be a blog post, documentation, or any marketing material.
                    </p>
                </div>
            </div>
            
            <div class="input-group">
                <label class="input-label">Draft Content</label>
                <div class="file-upload">
                    <input type="file" id="draftFile" accept=".txt,.docx,.pdf">
                    <div class="file-upload-label">
                        <i class="fas fa-upload"></i>
                        Upload Draft (.txt, .docx, .pdf)
                    </div>
                </div>
                <div class="divider"><span>or</span></div>
                <textarea class="textarea-input" id="draftText" 
                         placeholder="Paste your draft content here..." 
                         style="min-height: 200px;"></textarea>
            </div>
            
            <div id="draftStatus"></div>
        </div>
        """

    def _get_generate_section(self) -> str:
        """Get generate section HTML."""
        return """
        <div class="generate-section">
            <div style="background: var(--accent-color); color: var(--text-primary); padding: 0.5rem 1.5rem; border-radius: 50px; font-size: 1rem; font-weight: 700; margin-bottom: var(--spacing-lg); display: inline-block;">
                Step 3
            </div>
            
            <h2 class="generate-title">
                <i class="fas fa-wand-magic-sparkles"></i>
                Generate Consistent Content
            </h2>
            
            <p class="generate-subtitle">
                Our AI analyzes your reference patterns and transforms your draft to match your established style, 
                tone, and structure while preserving the original message and intent.
            </p>
            
            <button class="btn btn-primary btn-large" onclick="generateEdit()" id="generateBtn">
                <i class="fas fa-magic"></i>
                Transform Content
            </button>
            
            <div class="loading" id="loading">
                <div class="loading-content">
                    <i class="fas fa-brain loading-icon"></i>
                    <div class="loading-text">
                        <strong>Analyzing patterns and transforming content...</strong>
                        <div style="color: var(--text-secondary); font-weight: normal; margin-top: 0.5rem;">
                            This typically takes 30-90 seconds
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """

    def _get_output_section(self) -> str:
        """Get output section HTML."""
        return """
        <div class="output-section grid-full">
            <div class="output-header">
                <div>
                    <h2 style="color: var(--text-primary); display: flex; align-items: center; gap: var(--spacing-md); margin: 0;">
                        <i class="fas fa-check-circle" style="color: var(--success-color);"></i> 
                        Transformed Content
                    </h2>
                    <p style="color: var(--text-secondary); margin: 0.5rem 0 0 0; font-size: 0.95rem;">
                        Content transformed to match your established style patterns
                    </p>
                </div>
                <button class="btn btn-primary copy-btn" onclick="copyToClipboard()" id="copyBtn">
                    <i class="fas fa-copy"></i>
                    Copy Content
                    <div class="copy-success" id="copySuccess">Copied to clipboard!</div>
                </button>
            </div>
            <textarea class="output-textarea" id="result" 
                     placeholder="Your stylistically consistent content will appear here...

✨ What to expect:
- Improved tone consistency
- Better structure alignment  
- Enhanced vocabulary matching
- Preserved original message
- Professional quality output" 
                     readonly></textarea>
        </div>
        """

    def _get_contact_section(self) -> str:
        """Get contact section HTML."""
        return f"""
        <div class="contact-section">
            <h3 class="contact-title">
                <i class="fas fa-handshake"></i> 
                Let's Work Together
            </h3>
            <p class="contact-description">
                Need bulk processing, API access, team collaboration features, or custom integrations? 
                Let's discuss how Consistly can scale with your organization's content needs.
            </p>
            
            <div style="display: flex; gap: var(--spacing-lg); justify-content: center; flex-wrap: wrap; margin-bottom: var(--spacing-xl);">
                <a href="{self.linkedin_url}" target="_blank" rel="noopener noreferrer" class="linkedin-link">
                    <i class="fab fa-linkedin"></i>
                    Connect on LinkedIn
                </a>
                
                <a href="https://github.com/your-username/consistly" target="_blank" rel="noopener noreferrer" class="github-link">
                    <i class="fab fa-github"></i>
                    View on GitHub
                </a>
            </div>
            
            <div class="footer-info">
                <p class="footer-text">
                    Built with ❤️ by <strong>Ashutosh Gautam</strong> • Open Source for the Win! 🎉
                </p>
                <p class="footer-subtext">
                    Your content stays on your device. Powered by local AI for complete privacy.
                </p>
            </div>
        </div>
        """

    def _get_scripts(self) -> str:
        """Get JavaScript code."""
        return """
        <script>
        class Consistly {
            constructor() {
                this.referenceCount = 1;
                this.referenceTexts = [];
                this.draftContent = '';
                this.apiBase = '/api';
                this.init();
            }
            
            init() {
                this.bindEventListeners();
                this.updateStatus();
                this.showWelcomeMessage();
            }
            
            showWelcomeMessage() {
                setTimeout(() => {
                    this.showToast('Welcome to Consistly! Upload your reference content to get started. 🎯', 'info');
                }, 1500);
            }
            
            bindEventListeners() {
                document.addEventListener('change', (e) => {
                    if (e.target.type === 'file') {
                        this.handleFileUpload(e.target);
                    }
                });
                
                document.addEventListener('input', (e) => {
                    if (e.target.classList.contains('textarea-input')) {
                        this.handleTextInput(e.target);
                    }
                });
            }
            
            async handleFileUpload(fileInput) {
                const file = fileInput.files[0];
                if (!file) return;
                
                this.showFileProcessing(fileInput.id, true);
                
                try {
                    const text = await this.extractTextFromFile(file);
                    
                    if (fileInput.id === 'draftFile') {
                        document.getElementById('draftText').value = text;
                        this.draftContent = text;
                        this.updateDraftStatus();
                        this.showToast(`Draft uploaded successfully! (${text.split(' ').length} words)`, 'success');
                    } else if (fileInput.id.startsWith('refFile')) {
                        const refNum = fileInput.id.replace('refFile', '');
                        document.getElementById(`refText${refNum}`).value = text;
                        this.updateReferenceStatus();
                        this.showToast(`Reference ${refNum} uploaded successfully!`, 'success');
                    }
                    
                    this.showFileSuccess(fileInput.id, file.name);
                } catch (error) {
                    this.showFileError(fileInput.id, error.message);
                } finally {
                    this.showFileProcessing(fileInput.id, false);
                }
            }
            
            handleTextInput(textarea) {
                if (textarea.id === 'draftText') {
                    this.draftContent = textarea.value;
                    this.updateDraftStatus();
                } else if (textarea.id.startsWith('refText')) {
                    this.updateReferenceStatus();
                }
            }
            
            async extractTextFromFile(file) {
                const formData = new FormData();
                formData.append('file', file);
                
                const response = await fetch(`${this.apiBase}/extract-text`, {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Failed to extract text');
                }
                
                const data = await response.json();
                return data.data.text;
            }
            
            addReferenceField() {
                this.referenceCount++;
                const container = document.getElementById('referenceContainer');
                
                const newReference = document.createElement('div');
                newReference.className = 'reference-item';
                newReference.innerHTML = `
                    <div class="reference-number">${this.referenceCount}</div>
                    <div class="input-group">
                        <label class="input-label">Reference Content ${this.referenceCount}</label>
                        <div class="file-upload">
                            <input type="file" id="refFile${this.referenceCount}" accept=".txt,.docx,.pdf">
                            <div class="file-upload-label">
                                <i class="fas fa-upload"></i>
                                Upload File (.txt, .docx, .pdf)
                            </div>
                        </div>
                        <div class="divider"><span>or</span></div>
                        <textarea class="textarea-input" id="refText${this.referenceCount}" 
                                 placeholder="Paste your reference content here..."></textarea>
                        <button class="btn btn-secondary" onclick="app.removeReference(this)" style="margin-top: var(--spacing-md);">
                            <i class="fas fa-trash"></i> Remove
                        </button>
                    </div>
                `;
                
                container.appendChild(newReference);
                
                // Animate in
                newReference.style.opacity = '0';
                newReference.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    newReference.style.transition = 'all 0.3s ease';
                    newReference.style.opacity = '1';
                    newReference.style.transform = 'translateY(0)';
                }, 10);
                
                this.showToast(`Reference field ${this.referenceCount} added!`, 'success');
            }
            
            removeReference(button) {
                const referenceItem = button.closest('.reference-item');
                referenceItem.style.transition = 'all 0.3s ease';
                referenceItem.style.opacity = '0';
                referenceItem.style.transform = 'translateY(-20px)';
                
                setTimeout(() => {
                    referenceItem.remove();
                    this.updateReferenceStatus();
                    this.showToast('Reference field removed!', 'info');
                }, 300);
            }
            
            updateReferenceStatus() {
                this.referenceTexts = [];
                
                for (let i = 1; i <= this.referenceCount; i++) {
                    const textArea = document.getElementById(`refText${i}`);
                    if (textArea && textArea.value.trim()) {
                        this.referenceTexts.push(textArea.value.trim());
                    }
                }
                
                const statusDiv = document.getElementById('referenceStatus');
                if (this.referenceTexts.length > 0) {
                    const totalWords = this.referenceTexts.reduce((sum, text) => sum + text.split(' ').length, 0);
                    statusDiv.innerHTML = `
                        <div class="status success">
                            <i class="fas fa-check-circle"></i> 
                            ${this.referenceTexts.length} reference content ready (${totalWords.toLocaleString()} words total)
                        </div>
                    `;
                } else {
                    statusDiv.innerHTML = '';
                }
            }
            
            updateDraftStatus() {
                const statusDiv = document.getElementById('draftStatus');
                if (this.draftContent.trim()) {
                    const wordCount = this.draftContent.trim().split(' ').length;
                    const readTime = Math.ceil(wordCount / 200);
                    statusDiv.innerHTML = `
                        <div class="status success">
                            <i class="fas fa-check-circle"></i> 
                            Draft ready (${wordCount.toLocaleString()} words • ~${readTime} min read)
                        </div>
                    `;
                } else {
                    statusDiv.innerHTML = '';
                }
            }
            
            updateStatus() {
                this.updateReferenceStatus();
                this.updateDraftStatus();
            }
            
            async generateEdit() {
                this.updateStatus();
                
                if (this.referenceTexts.length === 0) {
                    this.showError('Please add at least one reference content to establish style patterns');
                    document.getElementById('referenceContainer').scrollIntoView({ behavior: 'smooth' });
                    return;
                }
                
                if (!this.draftContent.trim()) {
                    this.showError('Please add your draft content to transform');
                    document.getElementById('draftText').focus();
                    return;
                }
                
                const generateBtn = document.getElementById('generateBtn');
                const loading = document.getElementById('loading');
                const resultTextarea = document.getElementById('result');
                
                generateBtn.disabled = true;
                loading.classList.add('show');
                resultTextarea.value = '';
                
                this.showToast('🧠 Analyzing your style patterns...', 'info');
                
                try {
                    const startTime = Date.now();
                    
                    const response = await fetch(`${this.apiBase}/generate-edit`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            reference_articles: this.referenceTexts,
                            draft_content: this.draftContent
                        })
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || `HTTP ${response.status}`);
                    }
                    
                    const data = await response.json();
                    const endTime = Date.now();
                    const processingTime = Math.round((endTime - startTime) / 1000);
                    
                    resultTextarea.value = data.data.edited_article;
                    
                    // Scroll to results
                    setTimeout(() => {
                        resultTextarea.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 500);
                    
                    // Show success
                    this.showToast(
                        `✅ Content transformed in ${processingTime}s! Your consistent content is ready.`, 
                        'success'
                    );
                    
                } catch (error) {
                    console.error('Generation error:', error);
                    resultTextarea.value = `❌ Transformation failed: ${error.message}

This usually happens when:
- Ollama isn't running (run 'ollama serve' in terminal)
- The AI model needs to be downloaded
- Network connectivity issues

Please check that Ollama is running and try again.`;
                    this.showError(`Transformation failed: ${error.message}`);
                } finally {
                    generateBtn.disabled = false;
                    loading.classList.remove('show');
                }
            }
            
            async copyToClipboard() {
                const textarea = document.getElementById('result');
                const copySuccess = document.getElementById('copySuccess');
                
                if (!textarea.value.trim()) {
                    this.showError('Nothing to copy. Generate content first!');
                    return;
                }
                
                try {
                    await navigator.clipboard.writeText(textarea.value);
                    copySuccess.classList.add('show');
                    setTimeout(() => copySuccess.classList.remove('show'), 2500);
                    
                    this.showToast('📋 Content copied to clipboard! Ready to use.', 'success');
                } catch (err) {
                    textarea.select();
                    document.execCommand('copy');
                    copySuccess.classList.add('show');
                    setTimeout(() => copySuccess.classList.remove('show'), 2500);
                    this.showToast('📋 Content copied! Ready to use.', 'success');
                }
            }
            
            showFileProcessing(fileInputId, isProcessing) {
                const fileInput = document.getElementById(fileInputId);
                const label = fileInput.nextElementSibling;
                
                if (isProcessing) {
                    label.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing file...';
                    label.style.opacity = '0.8';
                } else {
                    label.innerHTML = '<i class="fas fa-upload"></i> Upload File (.txt, .docx, .pdf)';
                    label.style.opacity = '1';
                }
            }
            
            showFileSuccess(fileInputId, filename) {
                const fileInput = document.getElementById(fileInputId);
                const label = fileInput.nextElementSibling;
                
                label.innerHTML = `<i class="fas fa-check"></i> ${filename}`;
                label.style.background = 'var(--success-color)';
                
                setTimeout(() => {
                    label.innerHTML = '<i class="fas fa-upload"></i> Upload File (.txt, .docx, .pdf)';
                    label.style.background = '';
                }, 3000);
            }
            
            showFileError(fileInputId, errorMessage) {
                const fileInput = document.getElementById(fileInputId);
                const label = fileInput.nextElementSibling;
                
                label.innerHTML = `<i class="fas fa-exclamation-triangle"></i> Error`;
                label.style.background = 'var(--error-color)';
                
                setTimeout(() => {
                    label.innerHTML = '<i class="fas fa-upload"></i> Upload File (.txt, .docx, .pdf)';
                    label.style.background = '';
                }, 3000);
                
                this.showError(errorMessage);
            }
            
            showSuccess(message) {
                this.showToast(message, 'success');
            }
            
            showError(message) {
                this.showToast(message, 'error');
            }
            
            showToast(message, type = 'info') {
                const existingToasts = document.querySelectorAll('.toast');
                existingToasts.forEach(toast => toast.remove());
                
                const toast = document.createElement('div');
                toast.className = `toast toast-${type}`;
                
                const icons = {
                    success: 'fas fa-check-circle',
                    error: 'fas fa-exclamation-triangle',
                    info: 'fas fa-info-circle'
                };
                
                const colors = {
                    success: 'var(--success-color)',
                    error: 'var(--error-color)',
                    info: 'var(--primary-color)'
                };
                
                toast.innerHTML = `
                    <i class="${icons[type]}"></i>
                    <span>${message}</span>
                `;
                
                toast.style.cssText = `
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: ${colors[type]};
                    color: var(--text-primary);
                    padding: var(--spacing-md) var(--spacing-lg);
                    border-radius: var(--radius-lg);
                    box-shadow: var(--shadow-lg);
                    z-index: 1000;
                    display: flex;
                    align-items: center;
                    gap: var(--spacing-md);
                    font-weight: 600;
                    max-width: 400px;
                    transform: translateX(100%);
                    transition: transform var(--transition-normal);
                    font-size: 0.9rem;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                `;
                
                document.body.appendChild(toast);
                
                setTimeout(() => {
                    toast.style.transform = 'translateX(0)';
                }, 10);
                
                setTimeout(() => {
                    toast.style.transform = 'translateX(100%)';
                    setTimeout(() => {
                        if (toast.parentNode) toast.remove();
                    }, 300);
                }, type === 'error' ? 6000 : 4000);
            }
            
            async checkHealth() {
                try {
                    const response = await fetch(`${this.apiBase}/health`);
                    const data = await response.json();
                    
                    if (data.ai_service.status !== 'success') {
                        this.showError(`⚠️ AI service not available: ${data.ai_service.message}. Please ensure Ollama is running.`);
                    } else {
                        console.log('✅ Consistly AI is ready!');
                    }
                } catch (error) {
                    console.error('Health check failed:', error);
                    this.showError('⚠️ Unable to connect to AI service. Please ensure Ollama is running with "ollama serve".');
                }
            }
        }
        
        // Initialize the application
        const app = new Consistly();
        
        // Global functions for HTML onclick handlers
        window.addReferenceField = () => app.addReferenceField();
        window.generateEdit = () => app.generateEdit();
        window.copyToClipboard = () => app.copyToClipboard();
        
        // Initialize health check
        document.addEventListener('DOMContentLoaded', () => {
            app.checkHealth();
        });
        </script>
        """