document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('predict-form');
    const resultSection = document.getElementById('result');
    const predictionOutput = document.getElementById('prediction-output');
    const tipOutput = document.getElementById('tip-output');
    const spinner = document.getElementById('loading-spinner');
    const plantImageContainer = document.getElementById('plant-image-container');
    const plantImage = document.getElementById('plant-image');
    const plantSelect = document.getElementById('plant_name');
    const confettiCanvas = document.getElementById('confetti-canvas');

    // Plant images (use emoji or public domain SVGs for demo)
    const plantImages = {
        rose: 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f339.png',
        basil: 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f33f.png',
        mint: 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f33f.png',
        cactus: 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f335.png',
        aloe_vera: 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f335.png',
        spider_plant: 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f331.png',
        money_plant: 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f4b0.png',
        peace_lily: 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f490.png',
        tomato: 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f345.png',
        snake_plant: 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f331.png',
    };

    // Tips/facts for each result
    const tips = {
        'Needs Watering': [
            'Tip: Water your plant thoroughly until water drains from the bottom.',
            'Fact: Underwatering is a common cause of plant stress.',
            'Tip: Check soil moisture before watering next time.'
        ],
        'Moderate': [
            'Tip: Your plant is doing okay, but keep an eye on soil moisture.',
            'Fact: Most plants prefer soil that is moist but not soggy.',
            'Tip: Consider misting leaves for humidity-loving plants.'
        ],
        'Well Watered': [
            'Great job! Your plant is perfectly hydrated.',
            'Fact: Overwatering can be as harmful as underwatering.',
            'Tip: Let the top inch of soil dry before watering again.'
        ]
    };

    // Confetti animation (simple JS)
    function launchConfetti() {
        const ctx = confettiCanvas.getContext('2d');
        confettiCanvas.width = window.innerWidth;
        confettiCanvas.height = window.innerHeight;
        confettiCanvas.classList.remove('hidden');
        let confettiPieces = [];
        for (let i = 0; i < 120; i++) {
            confettiPieces.push({
                x: Math.random() * confettiCanvas.width,
                y: Math.random() * -confettiCanvas.height,
                r: 6 + Math.random() * 8,
                d: 2 + Math.random() * 4,
                color: `hsl(${Math.random()*360},70%,60%)`,
                tilt: Math.random() * 10 - 5
            });
        }
        let frame = 0;
        function draw() {
            ctx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
            confettiPieces.forEach(p => {
                ctx.beginPath();
                ctx.ellipse(p.x, p.y, p.r, p.r/2, p.tilt, 0, 2 * Math.PI);
                ctx.fillStyle = p.color;
                ctx.fill();
            });
        }
        function update() {
            confettiPieces.forEach(p => {
                p.y += p.d;
                p.x += Math.sin(frame/10 + p.tilt) * 2;
                if (p.y > confettiCanvas.height) {
                    p.y = -10;
                    p.x = Math.random() * confettiCanvas.width;
                }
            });
            frame++;
        }
        let count = 0;
        function animate() {
            draw();
            update();
            count++;
            if (count < 80) {
                requestAnimationFrame(animate);
            } else {
                confettiCanvas.classList.add('hidden');
            }
        }
        animate();
    }

    // Show plant image on selection
    function updatePlantImage() {
        const plant = plantSelect.value;
        if (plantImages[plant]) {
            plantImage.src = plantImages[plant];
            plantImage.alt = plant.charAt(0).toUpperCase() + plant.slice(1);
            plantImageContainer.classList.remove('hidden');
        } else {
            plantImageContainer.classList.add('hidden');
        }
    }
    plantSelect.addEventListener('change', updatePlantImage);
    updatePlantImage();

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        // Hide result, show spinner
        resultSection.classList.add('hidden');
        spinner.classList.remove('hidden');
        tipOutput.innerHTML = '';
        // Simulate prediction delay
        setTimeout(() => {
            spinner.classList.add('hidden');
            // Pick a random result for demo
            const mockResults = [
                { label: 'Needs Watering', emoji: '\ud83d\udca7', color: '#e53935' },
                { label: 'Moderate', emoji: '\ud83c\udf3f', color: '#fbc02d' },
                { label: 'Well Watered', emoji: '\ud83e\udeb4', color: '#43a047' }
            ];
            const random = Math.floor(Math.random() * mockResults.length);
            const { label, emoji, color } = mockResults[random];
            predictionOutput.innerHTML = `<span style="font-size:2.2rem;">${emoji}</span><br><span style="color:${color}">${label}</span>`;
            // Show tip/fact
            const tipArr = tips[label];
            if (tipArr) {
                const tip = tipArr[Math.floor(Math.random() * tipArr.length)];
                tipOutput.innerHTML = `<b>🌟</b> ${tip}`;
            }
            // Show plant image again
            updatePlantImage();
            // Show result
            resultSection.classList.remove('hidden');
            resultSection.classList.add('pop');
            setTimeout(() => resultSection.classList.remove('pop'), 400);
            // Confetti for Well Watered
            if (label === 'Well Watered') {
                launchConfetti();
            }
        }, 1200);
    });
});

// Add a little pop animation
const style = document.createElement('style');
style.innerHTML = `
#result.pop {
    animation: pop 0.4s;
}
@keyframes pop {
    0% { transform: scale(0.9); }
    60% { transform: scale(1.08); }
    100% { transform: scale(1); }
}`;
document.head.appendChild(style); 