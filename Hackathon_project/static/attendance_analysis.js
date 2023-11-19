document.addEventListener('DOMContentLoaded', function () {
    // Extract data from the server-side variable
    const scriptTag = document.getElementById('attendanceData');
    const rawData = scriptTag.textContent;
    const attendanceData = JSON.parse(rawData);
    // Prepare data for the pie chart
    const labels = attendanceData.map(entry => entry.status);
    console.log('Labels:', labels);
    const counts = labels.reduce((acc, label) => {
        acc[label] = (acc[label] || 0) + 1;
        return acc;
    }, {});

    const data = Object.values(counts);
    const backgroundColors = ['#FF6384', '#36A2EB', '#FFCE56']; // You can customize these colors

    // Create a pie chart
    const ctx = document.getElementById('attendancePieChart').getContext('2d');
    const pieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(counts),
            datasets: [{
                data: data,
                backgroundColor: backgroundColors,
            }],
        },
    });
});
