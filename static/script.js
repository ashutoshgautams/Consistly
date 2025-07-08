/**
 * AI Writing Style Copier - Frontend JavaScript
 * 
 * Handles all client-side interactions including file uploads,
 * form management, API communication, and UI updates.
 */

class WritingStyleCopier {
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
    }
    
    bindEventListeners() {
        // File upload handlers
        document.addEventListener('change', (e) => {
            if (e.target.type === 'file') {
                this.handleFileUpload(e.target);
            }
        });
        
        // Text area handlers
        document.addEventListener('input', (e) => {
            if (e.target.classList.contains('textarea-input')) {
                this.handleTextInput(e.target);
            }
        });
        
        // Global error handler
        window.addEventListener('unhandledrejection', (e) => {
            console.error('Unhandled promise rejection:', e.reason);
            this.showError('An unexpected error occurred. Please try again.');
        });
    }
    
    /**
     * Handle file upload and text extraction
     */
    async handleFileUpload(fileInput) {
        const file = fileInput.files[0];
        if (!file) return;
        
        // Show loading state
        this.showFileProcessing(fileInput.id, true);
        
        try {
            const text = await this.extractTextFromFile(file);
            
            // Update corresponding textarea
            if (fileInput.id === 'draftFile') {
                document.getElementById('draftText').value = text;
                this.draftContent = text;
                this.updateDraftStatus();
            } else if (fileInput.id.startsWith('refFile')) {
                const refNum = fileInput.id.replace('refFile', '');
                document.getElementById(`refText${refNum}`).value = text;
                this.updateReferenceStatus();
            }
            
            this.showFileSuccess(fileInput.id, file.name);
        } catch (error) {
            this.showFileError(fileInput.id, error.message);
        } finally {
            this.showFileProcessing(fileInput.id, false);
        }
    }
    
    /**
     * Handle text input in textareas
     */
    handleTextInput(textarea) {
        if (textarea.id === 'draftText') {
            this.draftContent = textarea.value;
            this.updateDraftStatus();
        } else if (textarea.id.startsWith('refText')) {
            this.updateReferenceStatus();
        }
    }
    
    /**
     * Extract text from uploaded file via API
     */
    async extractTextFromFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${this.apiBase}/extract-text`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to extract text from file');
        }
        
        const data = await response.json();
        return data.data.text;
    }
    
    /**
     * Add a new reference field
     */
    addReferenceField() {
        this.referenceCount++;
        const container = document.getElementById('referenceContainer');
        
        const newReference = document.createElement('div');
        newReference.className = 'reference-item';
        newReference.innerHTML = `
            <div class="reference-number">${this.referenceCount}</div>
            <div class="input-group">
                <label class="input-label">Reference Article ${this.referenceCount}</label>
                <div class="file-upload">
                    <input type="file" id="refFile${this.referenceCount}" accept=".txt,.docx,.pdf">
                    <div class="file-upload-label">
                        <i class="fas fa-upload"></i>
                        Upload File (.txt, .docx, .pdf)
                    </div>
                </div>
                <div class="divider"><span>or</span></div>
                <textarea class="textarea-input" id="refText${this.referenceCount}" 
                         placeholder="Paste your reference article here..."></textarea>
                <button class="btn btn-secondary" onclick="app.removeReference(this)" style="margin-top: var(--spacing-md);">
                    <i class="fas fa-trash"></i> Remove
                </button>
            </div>
        `;
        
        container.appendChild(newReference);
        
        // Animate the new reference
        newReference.style.opacity = '0';
        newReference.style.transform = 'translateY(20px)';
        setTimeout(() => {
            newReference.style.transition = 'all 0.3s ease';
            newReference.style.opacity = '1';
            newReference.style.transform = 'translateY(0)';
        }, 10);
    }
    
    /**
     * Remove a reference field
     */
    removeReference(button) {
        const referenceItem = button.closest('.reference-item');
        
        // Animate removal
        referenceItem.style.transition = 'all 0.3s ease';
        referenceItem.style.opacity = '0';
        referenceItem.style.transform = 'translateY(-20px)';
        
        setTimeout(() => {
            referenceItem.remove();
            this.updateReferenceStatus();
        }, 300);
    }
    
    /**
     * Update reference articles status
     */
    updateReferenceStatus() {
        this.referenceTexts = [];
        
        // Collect all reference texts
        for (let i = 1; i <= this.referenceCount; i++) {
            const textArea = document.getElementById(`refText${i}`);
            if (textArea && textArea.value.trim()) {
                this.referenceTexts.push(textArea.value.trim());
            }
        }
        
        const statusDiv = document.getElementById('referenceStatus');
        if (this.referenceTexts.length > 0) {
            statusDiv.innerHTML = `
                <div class="status success">
                    <i class="fas fa-check"></i> 
                    ${this.referenceTexts.length} reference article(s) ready
                </div>
            `;
        } else {
            statusDiv.innerHTML = '';
        }
    }
    
    /**
     * Update draft status
     */
    updateDraftStatus() {
        const statusDiv = document.getElementById('draftStatus');
        if (this.draftContent.trim()) {
            statusDiv.innerHTML = `
                <div class="status success">
                    <i class="fas fa-check"></i> 
                    Draft article ready (${this.draftContent.trim().split(' ').length} words)
                </div>
            `;
        } else {
            statusDiv.innerHTML = '';
        }
    }
    
    /**
     * Update overall status
     */
    updateStatus() {
        this.updateReferenceStatus();
        this.updateDraftStatus();
    }
    
    /**
     * Generate edited article
     */
    async generateEdit() {
        // Validate inputs
        this.updateStatus();
        
        if (this.referenceTexts.length === 0) {
            this.showError('Please add at least one reference article');
            document.getElementById('referenceStatus').innerHTML = `
                <div class="status error">
                    <i class="fas fa-exclamation-triangle"></i> 
                    Please add at least one reference article
                </div>
            `;
            return;
        }
        
        if (!this.draftContent.trim()) {
            this.showError('Please add your draft article');
            document.getElementById('draftStatus').innerHTML = `
                <div class="status error">
                    <i class="fas fa-exclamation-triangle"></i> 
                    Please add your draft article
                </div>
            `;
            return;
        }
        
        // UI state management
        const generateBtn = document.getElementById('generateBtn');
        const loading = document.getElementById('loading');
        const resultTextarea = document.getElementById('result');
        
        generateBtn.disabled = true;
        loading.classList.add('show');
        resultTextarea.value = '';
        
        try {
            const response = await fetch(`${this.apiBase}/generate-edit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
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
            resultTextarea.value = data.data.edited_article;
            
            // Scroll to results with smooth animation
            setTimeout(() => {
                resultTextarea.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            }, 100);
            
            // Show success message
            this.showSuccess('Article edited successfully!');
            
        } catch (error) {
            console.error('Generation error:', error);
            resultTextarea.value = `Error: ${error.message}`;
            this.showError(`Failed to generate edited article: ${error.message}`);
        } finally {
            generateBtn.disabled = false;
            loading.classList.remove('show');
        }
    }
    
    /**
     * Copy text to clipboard
     */
    async copyToClipboard() {
        const textarea = document.getElementById('result');
        const copySuccess = document.getElementById('copySuccess');
        
        if (!textarea.value.trim()) {
            this.showError('Nothing to copy. Generate an article first.');
            return;
        }
        
        try {
            await navigator.clipboard.writeText(textarea.value);
            this.showCopySuccess();
        } catch (err) {
            // Fallback for older browsers
            textarea.select();
            document.execCommand('copy');
            this.showCopySuccess();
        }
    }
    
    /**
     * Show copy success animation
     */
    showCopySuccess() {
        const copySuccess = document.getElementById('copySuccess');
        copySuccess.classList.add('show');
        setTimeout(() => {
            copySuccess.classList.remove('show');
        }, 2000);
    }
    
    /**
     * Show file processing state
     */
    showFileProcessing(fileInputId, isProcessing) {
        const fileInput = document.getElementById(fileInputId);
        const label = fileInput.nextElementSibling;
        
        if (isProcessing) {
            label.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing file...';
            label.style.opacity = '0.7';
        } else {
            label.innerHTML = '<i class="fas fa-upload"></i> Upload File (.txt, .docx, .pdf)';
            label.style.opacity = '1';
        }
    }
    
    /**
     * Show file upload success
     */
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
    
    /**
     * Show file upload error
     */
    showFileError(fileInputId, errorMessage) {
        const fileInput = document.getElementById(fileInputId);
        const label = fileInput.nextElementSibling;
        
        label.innerHTML = `<i class="fas fa-exclamation-triangle"></i> Error: ${errorMessage}`;
        label.style.background = 'var(--error-color)';
        
        setTimeout(() => {
            label.innerHTML = '<i class="fas fa-upload"></i> Upload File (.txt, .docx, .pdf)';
            label.style.background = '';
        }, 5000);
    }
    
    /**
     * Show success message
     */
    showSuccess(message) {
        this.showToast(message, 'success');
    }
    
    /**
     * Show error message
     */
    showError(message) {
        this.showToast(message, 'error');
    }
    
    /**
     * Show toast notification
     */
    showToast(message, type = 'info') {
        // Remove existing toasts
        const existingToasts = document.querySelectorAll('.toast');
        existingToasts.forEach(toast => toast.remove());
        
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check' : 'exclamation-triangle'}"></i>
            ${message}
        `;
        
        // Toast styles
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? 'var(--success-color)' : 'var(--error-color)'};
            color: white;
            padding: var(--spacing-md) var(--spacing-lg);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-lg);
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
            font-weight: 600;
            max-width: 400px;
            transform: translateX(100%);
            transition: transform var(--transition-normal);
        `;
        
        document.body.appendChild(toast);
        
        // Animate in
        setTimeout(() => {
            toast.style.transform = 'translateX(0)';
        }, 10);
        
        // Auto remove
        setTimeout(() => {
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.remove();
                }
            }, 300);
        }, 5000);
    }
    
    /**
     * Check system health
     */
    async checkHealth() {
        try {
            const response = await fetch(`${this.apiBase}/health`);
            const data = await response.json();
            
            console.log('System Health:', data);
            
            if (data.ai_service.status !== 'success') {
                this.showError(`AI service not available: ${data.ai_service.message}`);
            }
        } catch (error) {
            console.error('Health check failed:', error);
            this.showError('Unable to connect to the AI service. Please ensure Ollama is running.');
        }
    }
}

// Initialize the application
const app = new WritingStyleCopier();

// Global functions for HTML onclick handlers
window.addReferenceField = () => app.addReferenceField();
window.generateEdit = () => app.generateEdit();
window.copyToClipboard = () => app.copyToClipboard();

// Initialize health check on load
document.addEventListener('DOMContentLoaded', () => {
    app.checkHealth();
});

// Export for potential module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WritingStyleCopier;
}
