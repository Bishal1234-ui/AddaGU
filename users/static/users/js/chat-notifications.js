// Chat unread count functionality
function initializeChatNotifications() {
    // Function to update unread message count
    function updateUnreadCount() {
        fetch('/users/api/unread-count/')
            .then(response => response.json())
            .then(data => {
                const badge = document.getElementById('chat-unread-badge');
                if (badge) {
                    if (data.unread_count > 0) {
                        badge.style.display = 'block';
                        badge.textContent = data.unread_count > 99 ? '99+' : data.unread_count;
                    } else {
                        badge.style.display = 'none';
                    }
                }
            })
            .catch(error => console.error('Error fetching unread count:', error));
    }
    
    // Initialize unread count check
    updateUnreadCount();
    
    // Check for new messages every 30 seconds
    setInterval(updateUnreadCount, 30000);
}

// Notification count functionality
function initializeNotifications() {
    // Function to update unread notification count
    function updateNotificationCount() {
        fetch('/users/api/notification-count/')
            .then(response => response.json())
            .then(data => {
                const badge = document.getElementById('notification-unread-badge');
                if (badge) {
                    if (data.notification_count > 0) {
                        badge.style.display = 'block';
                        badge.textContent = data.notification_count > 99 ? '99+' : data.notification_count;
                    } else {
                        badge.style.display = 'none';
                    }
                }
            })
            .catch(error => console.error('Error fetching notification count:', error));
    }
    
    // Initialize notification count check
    updateNotificationCount();
    
    // Check for new notifications every 30 seconds
    setInterval(updateNotificationCount, 30000);
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize for authenticated users
    if (document.getElementById('chat-unread-badge')) {
        initializeChatNotifications();
    }
    
    if (document.getElementById('notification-unread-badge')) {
        initializeNotifications();
    }
});
