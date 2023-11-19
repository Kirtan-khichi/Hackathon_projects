document.addEventListener("DOMContentLoaded", function() {
    var checkInButton = document.getElementById("checkInButton");

    checkInButton.addEventListener("click", function(event) {
        event.preventDefault(); // Prevent default form submission

        // Check if geolocation is supported by the browser
        if (navigator.geolocation) {
            // Get the user's current position
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    // Success callback
                    var latitude = position.coords.latitude;
                    var longitude = position.coords.longitude;
                    var dateTime = new Date().toISOString();

                    // Create form data
                    var formData = new FormData();
                    formData.append("latitude", latitude);
                    formData.append("longitude", longitude);
                    formData.append("dateTime", dateTime);

                    // AJAX request to Flask server for check-in
                    fetch("/checkin", {
                        method: "POST",
                        body: formData,
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Handle the response from the server (if needed)
                        console.log("Response from server:", data);
                    })
                    .catch(error => {
                        // Handle errors (if any)
                        console.error("Error:", error);
                    });
                },
                function(error) {
                    // Error callback
                    console.error("Geolocation error:", error);
                }
            );
        } else {
            console.error("Geolocation is not supported by this browser.");
        }
    });
});
