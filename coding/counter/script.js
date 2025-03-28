document.addEventListener('DOMContentLoaded', function() {
    const countersContainer = document.getElementById('countersContainer');
    const addCounterBtn = document.getElementById('addCounter');
    const counterNameInput = document.getElementById('counterName');
    
    // Load counters from localStorage
    loadCounters();
    
    // Add new counter
    addCounterBtn.addEventListener('click', function() {
        const name = counterNameInput.value.trim();
        if (name) {
            addCounter(name);
            counterNameInput.value = '';
            saveCounters();
        }
    });
    
    // Also allow adding with Enter key
    counterNameInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addCounterBtn.click();
        }
    });
    
    function addCounter(name, value = 0) {
        const counterDiv = document.createElement('div');
        counterDiv.className = 'counter';
        
        const nameSpan = document.createElement('span');
        nameSpan.className = 'counter-name';
        nameSpan.textContent = name;
        
        const valueSpan = document.createElement('span');
        valueSpan.className = 'counter-value';
        valueSpan.textContent = value;
        
        const controlsDiv = document.createElement('div');
        controlsDiv.className = 'counter-controls';
        
        const decrementBtn = document.createElement('button');
        decrementBtn.className = 'counter-btn';
        decrementBtn.textContent = '-';
        decrementBtn.addEventListener('click', function() {
            valueSpan.textContent = parseInt(valueSpan.textContent) - 1;
            saveCounters();
        });
        
        const incrementBtn = document.createElement('button');
        incrementBtn.className = 'counter-btn';
        incrementBtn.textContent = '+';
        incrementBtn.addEventListener('click', function() {
            valueSpan.textContent = parseInt(valueSpan.textContent) + 1;
            saveCounters();
        });
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'counter-btn delete-btn';
        deleteBtn.textContent = '×';
        deleteBtn.addEventListener('click', function() {
            counterDiv.remove();
            saveCounters();
        });
        
        controlsDiv.appendChild(decrementBtn);
        controlsDiv.appendChild(valueSpan);
        controlsDiv.appendChild(incrementBtn);
        controlsDiv.appendChild(deleteBtn);
        
        counterDiv.appendChild(nameSpan);
        counterDiv.appendChild(controlsDiv);
        
        countersContainer.appendChild(counterDiv);
    }
    
    function saveCounters() {
        const counters = [];
        document.querySelectorAll('.counter').forEach(counter => {
            counters.push({
                name: counter.querySelector('.counter-name').textContent,
                value: parseInt(counter.querySelector('.counter-value').textContent)
            });
        });
        localStorage.setItem('counters', JSON.stringify(counters));
    }
    
    function loadCounters() {
        const savedCounters = localStorage.getItem('counters');
        if (savedCounters) {
            JSON.parse(savedCounters).forEach(counter => {
                addCounter(counter.name, counter.value);
            });
        }
    }
});