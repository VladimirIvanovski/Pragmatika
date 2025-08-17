(function () {
  // Check if Chart.js is loaded
  if (typeof Chart === 'undefined') {
    console.error('Chart.js is not loaded');
    return;
  }

  // Function to create a chart
  function createChart(chartConfig) {
    const canvas = document.getElementById(chartConfig.id);
    if (!canvas) {
      console.warn(`Canvas with id "${chartConfig.id}" not found`);
      return;
    }

    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
      type: chartConfig.type || 'line',
      data: chartConfig.data,
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'bottom', labels: { boxWidth: 12 } },
          title: { display: false },
        },
        scales: {
          y: { beginAtZero: true, ticks: { stepSize: 10 } },
        },
      },
    });
  }

  // Use dynamic chart data if available, otherwise use default
  if (window.chartData && window.chartData.length > 0) {
    // Create charts from dynamic data
    window.chartData.forEach(createChart);
  } else {
    // Fallback: create default chart if competenceChart canvas exists
    const canvas = document.getElementById('competenceChart');
    if (canvas) {
      createChart({
        id: 'competenceChart',
        type: 'line',
        data: {
          labels: ['Почетно', 'Средно', 'Напредно'],
          datasets: [
            {
              label: 'Пред интервенција',
              data: [35, 22, 8],
              backgroundColor: 'rgba(99, 102, 241, 0.25)',
              borderColor: 'rgb(99, 102, 241)',
              borderWidth: 2,
              tension: 0.25,
              fill: true,
            },
            {
              label: 'По интервенција',
              data: [18, 28, 19],
              backgroundColor: 'rgba(59, 130, 246, 0.25)',
              borderColor: 'rgb(59, 130, 246)',
              borderWidth: 2,
              tension: 0.25,
              fill: true,
            },
          ],
        }
      });
    }
  }
})();