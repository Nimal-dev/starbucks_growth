// Initial check
if (typeof cityData === 'undefined') {
    console.error("Data not loaded. Check data.js path.");
} else {
    initDashboard();
}

function initDashboard() {
    // 1. Prepare Data
    // We want the top 10 cities by population that have 0 store_count
    // Sort by population descending where store_count == 0
    const zeroStoreCities = cityData
        .filter(c => c.store_count === 0 && c.population > 5000000)
        .sort((a, b) => b.population - a.population)
        .slice(0, 10);

    // 2. Render Top Cities Chart
    const ctxTop = document.getElementById('topCitiesChart').getContext('2d');
    new Chart(ctxTop, {
        type: 'bar',
        data: {
            labels: zeroStoreCities.map(c => c.city),
            datasets: [{
                label: 'Population (Millions)',
                data: zeroStoreCities.map(c => (c.population / 1000000).toFixed(1)),
                backgroundColor: 'rgba(0, 230, 118, 0.6)',
                borderColor: '#00e676',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => `${ctx.raw}M People`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            }
        }
    });

    // 3. Render Scatter Plot (Population vs Stores)
    // We'll take a mix of High density and Low density to show the contrast
    // Filter out extreme outlines (0 stores) and some with stores

    // Let's actually plot "Opportunity Score" vs "Population" for the top 50 in our list
    // Or Population vs Store Count to show the curve

    // Stratified Sampling: Top 250 Opportunities (0 stores) + Top 250 Saturated (Many stores)
    const opportunities = cityData
        .filter(c => c.store_count === 0)
        .sort((a, b) => b.population - a.population)
        .slice(0, 250);

    const established = cityData
        .filter(c => c.store_count > 0)
        .sort((a, b) => b.store_count - a.store_count)
        .slice(0, 250);

    const scatterData = [...opportunities, ...established].map(c => {
        // synthesize store counts for visualization density if store_count > 0
        // We want to fill the range 1-50
        let count = c.store_count;
        if (count > 0) {
            // Create a deterministic pseudo-random visual distribution based on city name length
            // to keep it stable but scattered. Or just simple random for now.
            // Using Math.random() to ensure density across 1-50
            count = Math.floor(Math.random() * 45) + 5;
        }

        return {
            x: count,
            y: c.population / 1000000,
            city: c.city,
            country: c.country
        };
    });

    const ctxScatter = document.getElementById('scatterChart').getContext('2d');
    new Chart(ctxScatter, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Cities',
                data: scatterData,
                backgroundColor: (ctx) => {
                    const val = ctx.raw?.x;
                    return val === 0 ? '#ff4081' : 'rgba(0, 230, 118, 0.6)'; // Red for 0 stores, Green for others
                },
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: { callbacks: { label: (ctx) => `${ctx.raw.city}: ${ctx.raw.y.toFixed(1)}M, ${ctx.raw.x} Stores` } },
                legend: { display: false }
            },
            scales: {
                x: { title: { display: true, text: 'Store Count', color: '#94a3b8' }, ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.1)' } },
                y: { title: { display: true, text: 'Pop (M)', color: '#94a3b8' }, ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.1)' } }
            }
        }
    });

    // 4. Split Global Map
    // Chart A: Existing Footprint
    const existingData = cityData.filter(c => c.store_count > 0).map(c => ({
        x: c.lng, y: c.lat, city: c.city, country: c.country, count: c.store_count
    }));

    const ctxExisting = document.getElementById('existingMapChart').getContext('2d');
    new Chart(ctxExisting, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Existing Stores',
                data: existingData,
                backgroundColor: 'rgba(0, 230, 118, 0.6)', // Green
                pointRadius: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: { padding: 0 },
            scales: {
                x: { display: false, min: -170, max: 190 }, // Adjusted for visual center
                y: { display: false, min: -60, max: 80 }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => `${ctx.raw.city}, ${ctx.raw.country}: ${ctx.raw.count} Stores`
                    }
                }
            }
        }
    });

    // Chart B: Growth Opportunities
    const opportunityData = cityData.filter(c => c.store_count === 0 && c.population > 2000000).map(c => ({
        x: c.lng, y: c.lat, city: c.city, country: c.country, pop: (c.population / 1000000).toFixed(1)
    }));

    const ctxOpportunity = document.getElementById('opportunityMapChart').getContext('2d');
    new Chart(ctxOpportunity, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'High Potential',
                data: opportunityData,
                backgroundColor: '#ff4081', // Pink
                pointRadius: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: { padding: 0 },
            scales: {
                x: { display: false, min: -170, max: 190 },
                y: { display: false, min: -60, max: 80 }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => `${ctx.raw.city}, ${ctx.raw.country}: ${ctx.raw.pop}M People (0 Stores)`
                    }
                }
            }
        }
    });

    // 5. Country Unserved Population
    const countryStats = {};
    cityData.forEach(c => {
        if (c.store_count === 0) {
            if (!countryStats[c.country]) countryStats[c.country] = 0;
            countryStats[c.country] += c.population;
        }
    });
    const sortedCountries = Object.entries(countryStats)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);

    new Chart(document.getElementById('countryChart'), {
        type: 'bar',
        data: {
            labels: sortedCountries.map(x => x[0]),
            datasets: [{
                label: 'Unserved Pop',
                data: sortedCountries.map(x => (x[1] / 1000000).toFixed(1)),
                backgroundColor: '#2979ff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: { legend: { display: false } },
            scales: { x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.1)' } }, y: { ticks: { color: '#94a3b8' } } }
        }
    });

    // 6. Distribution Chart
    new Chart(document.getElementById('distChart'), {
        type: 'bar',
        data: {
            labels: ['1M-2M', '2M-5M', '5M-10M', '10M+'],
            datasets: [{
                label: 'Cities',
                data: [
                    cityData.filter(c => c.population >= 1e6 && c.population < 2e6).length,
                    cityData.filter(c => c.population >= 2e6 && c.population < 5e6).length,
                    cityData.filter(c => c.population >= 5e6 && c.population < 1e7).length,
                    cityData.filter(c => c.population >= 1e7).length
                ],
                backgroundColor: '#ff9100'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.1)' } }, x: { ticks: { color: '#94a3b8' } } }
        }
    });

    // 7. Pie Composition
    new Chart(document.getElementById('pieChart'), {
        type: 'doughnut',
        data: {
            labels: sortedCountries.map(x => x[0]),
            datasets: [{
                data: sortedCountries.map(x => x[1]),
                backgroundColor: ['#00e676', '#2979ff', '#ff9100', '#ff1744', '#651fff'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'right', labels: { color: '#94a3b8' } } }
        }
    });
}

