document.addEventListener("DOMContentLoaded", function () {
    // Ensure these variables are passed correctly from the template
    console.log(`Total Income: ${totalIncome}`);
    console.log(`Total Expenses: ${totalExpenses}`);
  
    // Handle date range filter change
    document.getElementById("dateRange").addEventListener("change", function () {
      document.getElementById("filterForm").submit();
    });
  
    // Income vs. Expenses Chart
    const incomeExpensesCtx = document.getElementById("incomeExpensesChart").getContext("2d");
    new Chart(incomeExpensesCtx, {
      type: "doughnut",
      data: {
        labels: ["Income", "Expenses"],
        datasets: [
          {
            label: "Amount",
            data: [totalIncome, totalExpenses], // Use the variables passed from Django
            backgroundColor: ["#007bff", "#dc3545"],
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          tooltip: {
            callbacks: {
              label: function (context) {
                return `£${context.raw.toFixed(2)}`;
              },
            },
          },
        },
      },
    });
  
    // Category Breakdown Chart
    const categoryBreakdownCtx = document.getElementById("categoryBreakdownChart").getContext("2d");
    new Chart(categoryBreakdownCtx, {
      type: "bar",
      data: {
        labels: categories, // Passed from Django
        datasets: [
          {
            label: "Expenses by Category",
            data: categoryTotals, // Passed from Django
            backgroundColor: ["#007bff", "#28a745", "#ffc107", "#17a2b8", "#dc3545"],
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function (context) {
                return `£${context.raw.toFixed(2)}`;
              },
            },
          },
        },
      },
    });
  });
  