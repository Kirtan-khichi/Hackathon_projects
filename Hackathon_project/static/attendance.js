document.addEventListener('DOMContentLoaded', function () {
    // Define an array to store attendance data
    const attendanceData = [];

    window.markAttendance = function (userId, status) {
        console.log(`User ${userId} marked ${status}`);

        // Check if the user already exists in the attendanceData array
        const existingUserIndex = attendanceData.findIndex(data => data.userId === userId);

        if (existingUserIndex !== -1) {
            // Update the status if the user already exists
            attendanceData[existingUserIndex].status = status;
        } else {
            // Add a new entry if the user does not exist
            attendanceData.push({ userId, status });
        }
    };

    window.submitAttendance = function () {
        // Send attendanceData to the server using an AJAX request
        fetch('/mark_attendance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                attendanceData,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);

            // Check the response for success message or error
            if (data.message) {
                // Redirect or render another template here
                window.location.href = '/mark_attendance';  // Replace '/success' with your desired route
            } else {
                // Handle error, show a message, or redirect to an error page
                console.error('Error:', data.error);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    };
});
