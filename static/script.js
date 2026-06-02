// ======================
// EcoGuardian Script
// ======================

// Sustainability Facts Carousel
const facts = [
    "🌍 One tree absorbs about 22kg of CO₂ every year.",
    "💧 Turning off the tap while brushing saves water.",
    "♻ Recycling one ton of paper saves 17 trees.",
    "⚡ LED bulbs use up to 75% less energy.",
    "🌳 Planting trees improves air quality and biodiversity."
];

let factIndex = 0;

function rotateFacts() {
    const factBox = document.getElementById("fact");
    if (factBox) {
        factIndex = (factIndex + 1) % facts.length;
        factBox.innerHTML = facts[factIndex];
    }
}

setInterval(rotateFacts, 3000);


// Dark / Light Mode
function toggleMode() {
    document.body.classList.toggle("dark-mode");
}


// Animated Green Streak Counter
const streakCounter = document.getElementById("streak");

if (streakCounter) {
    let count = 0;

    const interval = setInterval(() => {
        count++;

        streakCounter.innerHTML = count;

        if (count >= 30) {
            clearInterval(interval);
        }
    }, 100);
}


// Animated Eco Score Counter
const scoreCounter = document.getElementById("scoreCounter");

if (scoreCounter) {

    let target = parseInt(scoreCounter.dataset.score);

    let current = 0;

    const scoreInterval = setInterval(() => {

        current++;

        scoreCounter.innerHTML = current + "%";

        if (current >= target) {
            clearInterval(scoreInterval);
        }

    }, 20);
}


//