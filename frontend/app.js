// API Base URL - adjust if backend is on different host/port
const API_BASE_URL = window.location.origin;

// Get candidate ID from URL parameters or localStorage
function getCandidateId() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('candidateId') || localStorage.getItem('candidateId');
}

// Store candidate ID
function storeCandidateId(candidateId) {
    localStorage.setItem('candidateId', candidateId);
}

// Navigate to jobs view
function navigateToJobsView(candidateId) {
    storeCandidateId(candidateId);
    window.location.href = `jobs-view.html?candidateId=${candidateId}`;
}

// Navigate back to login
function navigateToLogin() {
    window.location.href = 'index.html';
}

// Show error message
function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

// Hide error message
function hideError(elementId) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.style.display = 'none';
    }
}

// Show loading indicator
function showLoading() {
    const loadingElement = document.getElementById('loadingIndicator');
    if (loadingElement) {
        loadingElement.style.display = 'block';
    }
}

// Hide loading indicator
function hideLoading() {
    const loadingElement = document.getElementById('loadingIndicator');
    if (loadingElement) {
        loadingElement.style.display = 'none';
    }
}

// Format skills array for display
function formatSkills(skills) {
    if (!skills || !Array.isArray(skills) || skills.length === 0) {
        return '<span class="skill-tag">None</span>';
    }
    return skills.map(skill => `<span class="skill-tag">${escapeHtml(skill)}</span>`).join('');
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Get match score class for styling
function getMatchScoreClass(score) {
    if (score >= 70) return 'high';
    if (score >= 40) return 'medium';
    return 'low';
}

// Fetch job matches from API
async function fetchJobMatches(candidateId) {
    try {
        showLoading();
        hideError('errorMessage');
        
        const response = await fetch(`${API_BASE_URL}/candidates/${candidateId}/matches`);
        
        if (!response.ok) {
            if (response.status === 404) {
                throw new Error('Candidate not found. Please check your candidate ID.');
            }
            throw new Error(`Failed to fetch matches: ${response.statusText}`);
        }
        
        const matches = await response.json();
        return matches;
    } catch (error) {
        throw error;
    } finally {
        hideLoading();
    }
}

// Render jobs table
function renderJobsTable(matches) {
    const tableBody = document.getElementById('jobsTableBody');
    const tableContainer = document.getElementById('jobsTableContainer');
    const noJobsMessage = document.getElementById('noJobsMessage');
    
    if (!tableBody || !tableContainer) return;
    
    // Clear existing rows
    tableBody.innerHTML = '';
    
    if (!matches || matches.length === 0) {
        tableContainer.style.display = 'none';
        if (noJobsMessage) {
            noJobsMessage.style.display = 'block';
        }
        return;
    }
    
    // Hide no jobs message
    if (noJobsMessage) {
        noJobsMessage.style.display = 'none';
    }
    
    // Show table
    tableContainer.style.display = 'block';
    
    // Add rows for each job match
    matches.forEach(match => {
        const row = document.createElement('tr');
        
        const scoreClass = getMatchScoreClass(match.matchScore);
        const skillsHtml = formatSkills(match.requiredSkills);
        
        row.innerHTML = `
            <td><strong>${escapeHtml(match.title)}</strong></td>
            <td><div class="skills-list">${skillsHtml}</div></td>
            <td>${match.minYearsExperience} years</td>
            <td><span class="match-score ${scoreClass}">${match.matchScore}%</span></td>
        `;
        
        tableBody.appendChild(row);
    });
}

// Initialize login page
function initLoginPage() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const candidateIdInput = document.getElementById('candidateId');
            const candidateId = candidateIdInput.value.trim();
            
            if (!candidateId) {
                showError('errorMessage', 'Please enter a candidate ID');
                return;
            }
            
            // Validate candidate ID is a positive number
            const id = parseInt(candidateId, 10);
            if (isNaN(id) || id <= 0) {
                showError('errorMessage', 'Please enter a valid candidate ID (positive number)');
                return;
            }
            
            hideError('errorMessage');
            
            // Navigate to jobs view
            navigateToJobsView(candidateId);
        });
    }
}

// Initialize jobs view page
async function initJobsViewPage() {
    const backButton = document.getElementById('backButton');
    
    // Set up back button
    if (backButton) {
        backButton.addEventListener('click', navigateToLogin);
    }
    
    // Get candidate ID from URL or localStorage
    const candidateId = getCandidateId();
    
    if (!candidateId) {
        showError('errorMessage', 'No candidate ID provided. Please go back to login.');
        return;
    }
    
    try {
        // Fetch and display job matches
        const matches = await fetchJobMatches(candidateId);
        renderJobsTable(matches);
    } catch (error) {
        showError('errorMessage', error.message || 'An error occurred while fetching job matches.');
    }
}

// Initialize appropriate page based on current URL
document.addEventListener('DOMContentLoaded', () => {
    const currentPage = window.location.pathname;
    
    if (currentPage.includes('jobs-view.html')) {
        initJobsViewPage();
    } else {
        initLoginPage();
    }
});

