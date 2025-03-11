document.addEventListener('DOMContentLoaded', function() {
    const getLocationBtn = document.getElementById('getLocationBtn');
    const locationStatus = document.getElementById('locationStatus');
    const latInput = document.getElementById('latInput');
    const longInput = document.getElementById('longInput');
    
    getLocationBtn.addEventListener('click', function() {
      locationStatus.textContent = 'Detecting location...';
      locationStatus.className = 'location-status';
      
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          // Success callback
          function(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            
            // Store in hidden inputs
            latInput.value = latitude;
            longInput.value = longitude;  
            
            // Show success message
            locationStatus.textContent = `Location detected: ${latitude.toFixed(6)}, ${longitude.toFixed(6)}`;
            locationStatus.className = 'location-status location-success';
            
            // Change button text
            getLocationBtn.textContent = 'Location Detected ✓';
            getLocationBtn.disabled = true;
            setTimeout(() => {
              getLocationBtn.textContent = 'Update Location';
              getLocationBtn.disabled = false;
            }, 3000);
          },
          // Error callback
          function(error) {
            let errorMessage;
            switch(error.code) {
              case error.PERMISSION_DENIED:
                errorMessage = 'Location permission denied.';
                break;
              case error.POSITION_UNAVAILABLE:
                errorMessage = 'Location information unavailable.';
                break;
              case error.TIMEOUT:
                errorMessage = 'Location request timed out.';
                break;
              case error.UNKNOWN_ERROR:
                errorMessage = 'An unknown error occurred.';
                break;
            }
            locationStatus.textContent = errorMessage;
            locationStatus.className = 'location-status location-error';
          },
          // Options
          {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
          }
        );
      } else {
        locationStatus.textContent = 'Geolocation is not supported by this browser.';
        locationStatus.className = 'location-status location-error';
      }
    });
  });