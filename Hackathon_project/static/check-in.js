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

                    // AJAX request to Flask server for check-in
                    fetch("/checkin", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            latitude: latitude,
                            longitude: longitude,
                            dateTime: dateTime,
                        }),
                    })
                    .then(response => response.json())  // Change .text() to .json()
                    .then(data => {
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
