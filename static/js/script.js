


let processingInterval;
let currentSession = null;


$(document).ready(function () {
    initializeApp();
});

function initializeApp() {
    
    initCharacterCounter();

    
    initExampleButtons();

    
    initFormValidation();

    
    initVideoPlayer();

    
    initTooltips();

    
    initSmoothScrolling();
}


function initCharacterCounter() {
    const promptTextarea = $('#prompt');
    const charCount = $('#charCount');

    if (promptTextarea.length && charCount.length) {
        promptTextarea.on('input', function () {
            const length = $(this).val().length;
            charCount.text(length);

            
            charCount.removeClass('text-warning text-danger');
            if (length > 900) {
                charCount.addClass('text-danger');
            } else if (length > 800) {
                charCount.addClass('text-warning');
            }
        });

        
        promptTextarea.trigger('input');
    }
}


function initExampleButtons() {
    $('.example-btn').on('click', function () {
        const prompt = $(this).data('prompt');
        const promptTextarea = $('#prompt');

        
        promptTextarea.val('');
        typeText(promptTextarea[0], prompt, 50);

        
        $(this).addClass('btn-success').removeClass('btn-outline-primary');
        setTimeout(() => {
            $(this).removeClass('btn-success').addClass('btn-outline-primary');
        }, 1000);
    });
}


function typeText(element, text, speed = 50) {
    let i = 0;
    element.value = '';

    function typeChar() {
        if (i < text.length) {
            element.value += text.charAt(i);
            i++;
            setTimeout(typeChar, speed);

            
            $(element).trigger('input');
        }
    }

    typeChar();
}

function initFormValidation() {
    const form = $('#videoForm');

    if (form.length) {
        form.on('submit', function (e) {
            const prompt = $('#prompt').val().trim();

            
            if (prompt.length < 10) {
                e.preventDefault();
                showAlert('Please provide a more detailed description (at least 10 characters).', 'warning');
                $('#prompt').focus();
                return false;
            }

            if (prompt.length > 1000) {
                e.preventDefault();
                showAlert('Please keep your description under 1000 characters.', 'warning');
                $('#prompt').focus();
                return false;
            }

            
            
        });

        
        $('#generateBtn').on('click', function () {
            
            setTimeout(() => {
                const prompt = $('#prompt').val().trim();
                if (prompt.length >= 10 && prompt.length <= 1000) {
                    showProcessingStatus();
                    disableForm();
                    startStatusSimulation();
                }
            }, 10);
        });
    }
}


function showProcessingStatus() {
    const statusDiv = $('#processingStatus');

    if (statusDiv.length) {
        statusDiv.removeClass('d-none');

        
        $('html, body').animate({
            scrollTop: statusDiv.offset().top - 100
        }, 500);
    }
}


function disableForm() {
    const generateBtn = $('#generateBtn');
    const promptTextarea = $('#prompt');

    generateBtn.prop('disabled', true);
    generateBtn.html('<span class="spinner-border spinner-border-sm me-2"></span>Processing...');

    promptTextarea.prop('disabled', true);
    $('.example-btn').prop('disabled', true);
}


function startStatusSimulation() {
    const steps = [
        { id: 'step1Icon', message: 'Analyzing your prompt with AI...', delay: 1000 },
        { id: 'step2Icon', message: 'Searching for relevant stock videos...', delay: 3000 },
        { id: 'step3Icon', message: 'Generating natural AI voiceover...', delay: 5000 },
        { id: 'step4Icon', message: 'Merging video, audio, and subtitles...', delay: 7000 }
    ];

    let currentStep = 0;

    const updateStep = () => {
        if (currentStep < steps.length) {
            const step = steps[currentStep];

            
            $(`#${step.id}`).removeClass('text-muted').addClass('text-primary pulse');

            
            $('#statusMessage').text(step.message);

            
            const progress = ((currentStep + 1) / steps.length) * 100;
            $('#progressBar').css('width', progress + '%');

            currentStep++;

            
            setTimeout(updateStep, step.delay);
        }
    };

    
    setTimeout(updateStep, 500);
}


function initVideoPlayer() {
    const video = $('#generatedVideo');

    if (video.length) {
        
        video.on('loadedmetadata', function () {
            addVideoControls(this);
        });

        
        video.on('loadstart', function () {
            $(this).addClass('loading');
        });

        video.on('canplay', function () {
            $(this).removeClass('loading');
        });

        
        video.on('timeupdate', function () {
            updateVideoProgress(this);
        });
    }
}


function addVideoControls(videoElement) {
    const $video = $(videoElement);
    const duration = videoElement.duration;

    
    const durationText = formatTime(duration);
    const infoText = `Duration: ${durationText}`;

    $video.closest('.card-body').find('.position-relative').append(
        `<div class="position-absolute top-0 start-0 bg-dark bg-opacity-75 text-white px-2 py-1 m-2 rounded">
            <small>${infoText}</small>
        </div>`
    );
}


function updateVideoProgress(videoElement) {
    const progress = (videoElement.currentTime / videoElement.duration) * 100;
    const currentTime = formatTime(videoElement.currentTime);
    const duration = formatTime(videoElement.duration);

    
    console.log(`Video progress: ${progress.toFixed(1)}% (${currentTime}/${duration})`);
}


function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}


function initTooltips() {
    
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}


function initSmoothScrolling() {
    $('a[href^="#"]').on('click', function (e) {
        e.preventDefault();

        const target = $(this.getAttribute('href'));
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 100
            }, 800);
        }
    });
}


function showAlert(message, type = 'info', duration = 5000) {
    const alertClass = type === 'error' ? 'danger' : type;
    const alertHTML = `
        <div class="alert alert-${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    
    let container = $('.container').first();
    if (!container.length) {
        container = $('body');
    }

    const alertElement = $(alertHTML);
    container.prepend(alertElement);

    
    if (duration > 0) {
        setTimeout(() => {
            alertElement.alert('close');
        }, duration);
    }
}


function toggleFullscreen() {
    const video = document.getElementById('generatedVideo');
    if (!video) return;

    if (video.requestFullscreen) {
        video.requestFullscreen();
    } else if (video.webkitRequestFullscreen) {
        video.webkitRequestFullscreen();
    } else if (video.msRequestFullscreen) {
        video.msRequestFullscreen();
    }
}

function downloadVideo() {
    const video = document.getElementById('generatedVideo');
    if (!video) return;

    const videoSrc = video.querySelector('source').src;
    const link = document.createElement('a');
    link.href = videoSrc;
    link.download = 'ai-generated-video.mp4';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    
    showAlert('Video download started!', 'success', 3000);
}

function copyScript() {
    const scriptText = $('.script-container p').text();

    if (navigator.clipboard) {
        navigator.clipboard.writeText(scriptText).then(function () {
            
            const btn = event.target.closest('button');
            const originalHTML = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
            btn.classList.remove('btn-outline-primary');
            btn.classList.add('btn-success');

            setTimeout(() => {
                btn.innerHTML = originalHTML;
                btn.classList.remove('btn-success');
                btn.classList.add('btn-outline-primary');
            }, 2000);

            showAlert('Script copied to clipboard!', 'success', 3000);
        }).catch(function () {
            showAlert('Failed to copy script. Please select and copy manually.', 'error');
        });
    } else {
        
        const textArea = document.createElement('textarea');
        textArea.value = scriptText;
        document.body.appendChild(textArea);
        textArea.select();

        try {
            document.execCommand('copy');
            showAlert('Script copied to clipboard!', 'success', 3000);
        } catch (err) {
            showAlert('Failed to copy script. Please select and copy manually.', 'error');
        }

        document.body.removeChild(textArea);
    }
}

function shareVideo() {
    if (navigator.share) {
        navigator.share({
            title: 'AI Generated Video',
            text: 'Check out this video I created with AI!',
            url: window.location.href
        }).then(() => {
            showAlert('Thanks for sharing!', 'success', 3000);
        }).catch(() => {
            
        });
    } else {
        
        const url = window.location.href;

        if (navigator.clipboard) {
            navigator.clipboard.writeText(url).then(function () {
                showAlert('Video URL copied to clipboard!', 'success', 3000);
            });
        } else {
            
            const shareText = `Check out this AI-generated video: ${url}`;
            showAlert(`Share this URL: ${url}`, 'info', 10000);
        }
    }
}


function refreshPage() {
    window.location.reload();
}


function generateSessionId() {
    return Math.random().toString(36).substr(2, 9);
}


function savePreference(key, value) {
    try {
        localStorage.setItem(`aivideo_${key}`, JSON.stringify(value));
    } catch (e) {
        console.warn('Could not save preference:', e);
    }
}

function getPreference(key, defaultValue = null) {
    try {
        const item = localStorage.getItem(`aivideo_${key}`);
        return item ? JSON.parse(item) : defaultValue;
    } catch (e) {
        console.warn('Could not get preference:', e);
        return defaultValue;
    }
}


function trackPageLoad() {
    window.addEventListener('load', function () {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        console.log(`Page loaded in ${loadTime}ms`);
    });
}


trackPageLoad();


window.addEventListener('error', function (e) {
    console.error('JavaScript error:', e.error);

    
    if (e.error && e.error.message) {
        showAlert('An unexpected error occurred. Please refresh the page and try again.', 'error');
    }
});


window.addEventListener('online', function () {
    showAlert('Connection restored!', 'success', 3000);
});

window.addEventListener('offline', function () {
    showAlert('Connection lost. Some features may not work properly.', 'warning', 5000);
});


window.AI_VIDEO_GENERATOR = {
    showAlert,
    toggleFullscreen,
    downloadVideo,
    copyScript,
    shareVideo,
    refreshPage,
    generateSessionId,
    savePreference,
    getPreference
};