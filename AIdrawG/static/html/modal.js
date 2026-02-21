document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('tutorialModal');
    const openBtn = document.getElementById('openTutorial');
    const closeBtn = document.querySelector('.close');

    openBtn.onclick = function() {
        modal.style.display = 'block';
    }

    closeBtn.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});

// Function to show the popup
function showPopup(popupId) {
    var popup = document.getElementById(popupId);
    popup.style.display = 'block';
}

// Function to close the popup
function closePopup(popupId) {
    var popup = document.getElementById(popupId);
    popup.style.display = 'none';
}

// Attach click event listeners to the buttons
document.getElementById('object-detection-btn').addEventListener('click', function() {
    showPopup('object-detection-popup');
});

document.getElementById('image-generation-btn').addEventListener('click', function() {
    showPopup('image-generation-popup');
});