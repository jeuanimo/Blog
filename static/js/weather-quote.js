// Weather and Quote Widget JavaScript

// Weather Widget - Using Open-Meteo API (no API key required)
async function fetchWeather() {
    const weatherWidget = document.getElementById('weather-widget');
    
    try {
        // Get user's location
        if (!navigator.geolocation) {
            throw new Error('Geolocation not supported');
        }
        
        // Request user location
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                
                try {
                    // Fetch weather data from Open-Meteo (free, no API key)
                    const weatherResponse = await fetch(
                        `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=auto`
                    );
                    
                    if (!weatherResponse.ok) throw new Error('Weather API failed');
                    
                    const weatherData = await weatherResponse.json();
                    
                    // Fetch location name from reverse geocoding
                    const geoResponse = await fetch(
                        `https://geocoding-api.open-meteo.com/v1/search?latitude=${lat}&longitude=${lon}&count=1&language=en&format=json`
                    );
                    
                    let locationName = 'Your Location';
                    if (geoResponse.ok) {
                        const geoData = await geoResponse.json();
                        if (geoData.results && geoData.results.length > 0) {
                            locationName = geoData.results[0].name;
                            if (geoData.results[0].admin1) {
                                locationName += `, ${geoData.results[0].admin1}`;
                            }
                        }
                    }
                    
                    // Get weather description from code
                    const weatherCode = weatherData.current.weather_code;
                    const weatherDesc = getWeatherDescription(weatherCode);
                    const weatherIcon = getWeatherIcon(weatherCode);
                    
                    // Display weather
                    weatherWidget.innerHTML = `
                        <div class="weather-location">
                            <i class="bi bi-geo-alt-fill"></i> ${locationName}
                        </div>
                        <div class="weather-temp">
                            <span class="temp-value">${Math.round(weatherData.current.temperature_2m)}°F</span>
                        </div>
                        <div class="weather-desc">
                            <i class="bi ${weatherIcon}"></i> ${weatherDesc}
                        </div>
                        <div class="weather-details">
                            <div class="detail-item">
                                <i class="bi bi-droplet"></i>
                                <span>${weatherData.current.relative_humidity_2m}%</span>
                            </div>
                            <div class="detail-item">
                                <i class="bi bi-wind"></i>
                                <span>${Math.round(weatherData.current.wind_speed_10m)} mph</span>
                            </div>
                        </div>
                    `;
                } catch (error) {
                    console.error('Weather fetch error:', error);
                    weatherWidget.innerHTML = `
                        <div class="weather-error">
                            <i class="bi bi-exclamation-triangle"></i>
                            <p>Unable to load weather data</p>
                        </div>
                    `;
                }
            },
            (error) => {
                // User denied location or error occurred
                console.error('Geolocation error:', error);
                weatherWidget.innerHTML = `
                    <div class="weather-error">
                        <i class="bi bi-geo-alt-fill"></i>
                        <p>Enable location access to see local weather</p>
                    </div>
                `;
            }
        );
    } catch (error) {
        console.error('Weather error:', error);
        weatherWidget.innerHTML = `
            <div class="weather-error">
                <i class="bi bi-exclamation-triangle"></i>
                <p>Weather unavailable</p>
            </div>
        `;
    }
}

// Get weather description from WMO weather code
function getWeatherDescription(code) {
    const weatherCodes = {
        0: 'Clear sky',
        1: 'Mainly clear',
        2: 'Partly cloudy',
        3: 'Overcast',
        45: 'Foggy',
        48: 'Foggy',
        51: 'Light drizzle',
        53: 'Moderate drizzle',
        55: 'Dense drizzle',
        61: 'Light rain',
        63: 'Moderate rain',
        65: 'Heavy rain',
        71: 'Light snow',
        73: 'Moderate snow',
        75: 'Heavy snow',
        77: 'Snow grains',
        80: 'Light showers',
        81: 'Moderate showers',
        82: 'Heavy showers',
        85: 'Light snow showers',
        86: 'Heavy snow showers',
        95: 'Thunderstorm',
        96: 'Thunderstorm with hail',
        99: 'Thunderstorm with hail'
    };
    return weatherCodes[code] || 'Unknown';
}

// Get Bootstrap icon for weather code
function getWeatherIcon(code) {
    if (code === 0 || code === 1) return 'bi-sun';
    if (code === 2) return 'bi-cloud-sun';
    if (code === 3) return 'bi-cloudy';
    if (code === 45 || code === 48) return 'bi-cloud-fog';
    if (code >= 51 && code <= 55) return 'bi-cloud-drizzle';
    if (code >= 61 && code <= 65) return 'bi-cloud-rain';
    if (code >= 71 && code <= 77) return 'bi-cloud-snow';
    if (code >= 80 && code <= 82) return 'bi-cloud-rain-heavy';
    if (code >= 85 && code <= 86) return 'bi-cloud-snow';
    if (code >= 95 && code <= 99) return 'bi-cloud-lightning';
    return 'bi-cloud';
}

// Daily Quote Widget - Using ZenQuotes API (free, no API key)
async function fetchQuote() {
    const quoteWidget = document.getElementById('quote-widget');
    
    try {
        // Using quotable.io API (free, no API key required)
        const response = await fetch('https://api.quotable.io/quotes/random?tags=inspirational|motivational|success|life&maxLength=150');
        
        if (!response.ok) throw new Error('Quote API failed');
        
        const data = await response.json();
        const quote = data[0];
        
        quoteWidget.innerHTML = `
            <div class="quote-text">
                <i class="bi bi-quote quote-icon-left"></i>
                <p>${quote.content}</p>
                <i class="bi bi-quote quote-icon-right"></i>
            </div>
            <div class="quote-author">
                — ${quote.author}
            </div>
        `;
    } catch (error) {
        console.error('Quote fetch error:', error);
        
        // Fallback quote if API fails
        quoteWidget.innerHTML = `
            <div class="quote-text">
                <i class="bi bi-quote quote-icon-left"></i>
                <p>The only way to do great work is to love what you do.</p>
                <i class="bi bi-quote quote-icon-right"></i>
            </div>
            <div class="quote-author">
                — Steve Jobs
            </div>
        `;
    }
}

// Initialize widgets when page loads
document.addEventListener('DOMContentLoaded', function() {
    fetchWeather();
    fetchQuote();
});
