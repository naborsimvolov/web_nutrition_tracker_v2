document.addEventListener('DOMContentLoaded', function () {
    fetch('/get-nutrition-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('nutritionChart').getContext('2d');
            const nutritionChart = new Chart(ctx, {
                type: 'line', 
                data: {
                    labels: data.dates,
                    datasets: [{
                        label: 'Carbs (g)',
                        backgroundColor: 'rgb(255, 99, 132)',
                        borderColor: 'rgb(255, 99, 132)',
                        data: data.carbs,
                    }, {
                        label: 'Proteins (g)',
                        backgroundColor: 'rgb(54, 162, 235)',
                        borderColor: 'rgb(54, 162, 235)',
                        data: data.proteins,
                    }, {
                        label: 'Fats (g)',
                        backgroundColor: 'rgb(255, 206, 86)',
                        borderColor: 'rgb(255, 206, 86)',
                        data: data.fats,
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        });
});
