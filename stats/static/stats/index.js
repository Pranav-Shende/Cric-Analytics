const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
const scenarioSelect = document.getElementById('scenario-select');

// 1. Theme Logic
function switchTheme(e) {
    if (e.target.checked) {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
    }    
}

toggleSwitch.addEventListener('change', switchTheme);

// Initialize Theme
const currentTheme = localStorage.getItem('theme');
if (currentTheme) {
    document.documentElement.setAttribute('data-theme', currentTheme);
    if (currentTheme === 'dark') {
        toggleSwitch.checked = true;
    }
}

// 2. Field Visibility Logic (Core Functionality)
function updateUI() {
    const val = scenarioSelect.value;
    const f = {
        t1: document.getElementById('f-team1'),
        t2: document.getElementById('f-team2'),
        ov: document.getElementById('f-overs'),
        wk: document.getElementById('f-wickets'),
        dl: document.getElementById('f-delay')
    };

    // Hide all
    Object.values(f).forEach(el => { if(el) el.style.display = 'none'; });

    // Show based on scenario
    if (val === 'pre1') { 
        f.dl.style.display = 'block'; 
    } else if (val === 'mid1') { 
        f.ov.style.display = 'block'; f.wk.style.display = 'block'; f.dl.style.display = 'block'; 
    } else if (val === 'pre2') { 
        f.t1.style.display = 'block'; f.dl.style.display = 'block'; 
    } else if (val === 'mid2') { 
        Object.values(f).forEach(el => { if(el) el.style.display = 'block'; });
    }
}

scenarioSelect.addEventListener('change', updateUI);
updateUI(); 