// Functions

function erf(x) {
    sign = (-1) ** (x < 0);
    x = Math.abs(x)

    // A&S formula 7.1.26
    p = 0.3275911;
    t = 1.0 / (1.0 + p * x);
    constants = [
        1.061405429,
        -1.453152027,
        1.421413741,
        -0.284496736,
        0.254829592,
    ];

    temporary = 0
    for (index = 0; index < constants.length; index++) {
        temporary *= t;
        temporary += constants[index];
    }

    return sign * (1.0 - temporary * t * Math.exp(-x * x));
};

function normal_extreme(trials, successes, p) {
    if (trials == 0) return 0;

    expected = trials * p;
    desired = successes - 0.5;
    std = (expected * (1 - p)) ** 0.5;

    return 1 - 0.5 * (1 + erf((desired - expected) / std / 2 ** 0.5));
};

function flip_outcome(winning, losing, reporting) {
    swap = winning;
    winning = Math.max(winning, losing);
    losing = Math.min(swap, losing);

    reported = (winning + losing);
    difference = (winning - losing);

    total = Math.round(reported / reporting);
    remaining = total - reported

    trials = remaining;
    successes = Math.round((remaining + difference) / 2);
    p = losing / reported;

    if (remaining * p < 30) console.warn('The normal distribution is an approximation for these values.');

    return normal_extreme(trials, successes, p);
};

function predictHTML(winning, losing, reporting) {
    underdog = (winning < losing) ? 'A' : 'B';
    console.log(winning, losing, underdog);

    probability = flip_outcome(winning, losing, reporting);
    return underdog + ' wins or ties ' + (probability * 100).toFixed(2) + '% of the time.' ;
};

function updatePrediction() {
    winning = parseInt(document.getElementById('winning').value);
    losing = parseInt(document.getElementById('losing').value);
    reporting = parseFloat(document.getElementById('reporting').value);

    document.getElementById('prediction').innerHTML = predictHTML(winning, losing, reporting);
};

// Main

window.onload = updatePrediction;
