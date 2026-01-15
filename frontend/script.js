// DOM Elements
const jobDescription = document.getElementById('jobDescription');
const charCount = document.getElementById('charCount');
const clearBtn = document.getElementById('clearBtn');
const generateBtn = document.getElementById('generateBtn');
const emptyState = document.getElementById('emptyState');
const loadingState = document.getElementById('loadingState');
const resultState = document.getElementById('resultState');
const loadingStatus = document.getElementById('loadingStatus');
const progressFill = document.getElementById('progressFill');
const proposalText = document.getElementById('proposalText');
const editBtn = document.getElementById('editBtn');
const copyBtn = document.getElementById('copyBtn');
const regenerateBtn = document.getElementById('regenerateBtn');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toastMessage');

// Loading messages for animation
const loadingMessages = [
    "Analyzing job requirements...",
    "Identifying key skills needed...",
    "Searching relevant experience...",
    "Crafting personalized introduction...",
    "Highlighting your strengths...",
    "Polishing the final draft...",
    "Almost there..."
];

// Sample proposal for demo
const sampleProposal = `Dear Hiring Manager,

I am excited to apply for this position, as it aligns perfectly with my expertise and professional background.

After carefully reviewing your requirements, I am confident that my skills and experience make me an ideal candidate for this role. Here's why:

✨ Relevant Experience
I have extensive experience working on similar projects, delivering high-quality solutions that exceed client expectations. My portfolio includes successful implementations of comparable systems with measurable results.

🛠️ Technical Expertise
My technical skill set includes proficiency in the exact technologies you've mentioned. I stay current with industry best practices and continuously improve my craft through ongoing learning and real-world application.

💡 Problem-Solving Approach
I take a methodical approach to understanding project requirements before diving into implementation. This ensures that the final deliverable not only meets but exceeds your expectations.

📋 Project Approach
1. Initial consultation to clarify requirements and goals
2. Detailed project plan with milestones and timelines
3. Regular progress updates and open communication
4. Thorough testing and quality assurance
5. Post-delivery support and documentation

I am available to start immediately and am flexible with communication across time zones. I would love the opportunity to discuss how I can contribute to your project's success.

Looking forward to hearing from you!

Best regards`;

// State
let isEditing = false;

// Initialize
function init() {
    updateCharCount();
    setupEventListeners();
}

// Event Listeners
function setupEventListeners() {
    jobDescription.addEventListener('input', updateCharCount);
    clearBtn.addEventListener('click', clearInput);
    generateBtn.addEventListener('click', handleGenerate);
    editBtn.addEventListener('click', toggleEdit);
    copyBtn.addEventListener('click', copyToClipboard);
    regenerateBtn.addEventListener('click', handleGenerate);
}

// Update character count
function updateCharCount() {
    charCount.textContent = jobDescription.value.length;
}

// Clear input
function clearInput() {
    jobDescription.value = '';
    updateCharCount();
    jobDescription.focus();
}

// Handle generate proposal
async function handleGenerate() {
    const description = jobDescription.value.trim();
    
    if (!description) {
        shakeElement(jobDescription);
        jobDescription.focus();
        return;
    }
    
    // Show loading state
    showState('loading');
    generateBtn.disabled = true;
    
    // Simulate API call with loading animation
    await simulateLoading();
    
    // Show result
    proposalText.textContent = sampleProposal;
    showState('result');
    generateBtn.disabled = false;
    
    // Reset edit state
    isEditing = false;
    proposalText.contentEditable = 'false';
    editBtn.classList.remove('active');
}

// Simulate loading with progress
async function simulateLoading() {
    let progress = 0;
    let messageIndex = 0;
    
    return new Promise((resolve) => {
        const interval = setInterval(() => {
            // Update progress
            progress += Math.random() * 15 + 5;
            if (progress > 100) progress = 100;
            progressFill.style.width = `${progress}%`;
            
            // Update message
            if (progress > (messageIndex + 1) * (100 / loadingMessages.length)) {
                messageIndex = Math.min(messageIndex + 1, loadingMessages.length - 1);
                loadingStatus.textContent = loadingMessages[messageIndex];
            }
            
            // Complete
            if (progress >= 100) {
                clearInterval(interval);
                setTimeout(resolve, 300);
            }
        }, 200);
    });
}

// Show specific state
function showState(state) {
    emptyState.classList.add('hidden');
    loadingState.classList.add('hidden');
    resultState.classList.add('hidden');
    
    // Reset loading state
    if (state === 'loading') {
        progressFill.style.width = '0%';
        loadingStatus.textContent = loadingMessages[0];
    }
    
    switch (state) {
        case 'empty':
            emptyState.classList.remove('hidden');
            break;
        case 'loading':
            loadingState.classList.remove('hidden');
            break;
        case 'result':
            resultState.classList.remove('hidden');
            break;
    }
}

// Toggle edit mode
function toggleEdit() {
    isEditing = !isEditing;
    proposalText.contentEditable = isEditing ? 'true' : 'false';
    editBtn.classList.toggle('active', isEditing);
    
    if (isEditing) {
        proposalText.focus();
        // Place cursor at end
        const range = document.createRange();
        const selection = window.getSelection();
        range.selectNodeContents(proposalText);
        range.collapse(false);
        selection.removeAllRanges();
        selection.addRange(range);
    }
}

// Copy to clipboard
async function copyToClipboard() {
    const text = proposalText.textContent;
    
    try {
        await navigator.clipboard.writeText(text);
        showToast('Copied to clipboard!');
    } catch (err) {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast('Copied to clipboard!');
    }
}

// Show toast notification
function showToast(message) {
    toastMessage.textContent = message;
    toast.classList.remove('hidden');
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.classList.add('hidden');
        }, 300);
    }, 2500);
}

// Shake animation for validation
function shakeElement(element) {
    element.style.animation = 'none';
    element.offsetHeight; // Trigger reflow
    element.style.animation = 'shake 0.5s ease-in-out';
    
    setTimeout(() => {
        element.style.animation = '';
    }, 500);
}

// Add shake animation to CSS dynamically
const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
`;
document.head.appendChild(shakeStyle);

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', init);
