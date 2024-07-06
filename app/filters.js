
// Function to toggle filter button state
function toggleFilter(button, filterName) {
    if (button.classList.contains('unselected')) {
        button.classList.remove('unselected');
        button.classList.add('selected');
    } else {
        button.classList.remove('selected');
        button.classList.add('unselected');
    }
    updateFilters();
    submitFilters(); // Automatically submit the form
}

// Function to collect and update the selected filters
function updateFilters() {
    let selectedFilters = {};
    document.querySelectorAll('.filterbtn.selected').forEach(button => {
        selectedFilters[button.getAttribute('data-filter')] = 'YES';
    });
    document.getElementById('filters').value = JSON.stringify(selectedFilters);
}

// Collect filters and submit the form
function submitFilters() {
    updateFilters();
    document.getElementById('filterForm').submit(); // Submit the form automatically
}

// Function to reset all filters
function resetFilters() {
    // Remove 'selected' class and add 'unselected' to all filter buttons
    document.querySelectorAll('.filterbtn').forEach(button => {
        button.classList.remove('selected');
        button.classList.add('unselected');
    });
    // Clear the hidden filters input
    document.getElementById('filters').value = '';
    // Submit the form to reset filters
    document.getElementById('filterForm').submit();
}















/*--------------------------------------------------------------------------------

// Function to update the "Showing results for" text based on selected filters
function updateResultsText(selectedFilters) {
    let resultsText = 'Showing results';
    let filtersApplied = false;

    // Check each filter type and append to results text if selected
    if (selectedFilters['crowdedness']) {
        resultsText += ` for uncrowded venues,`;
        filtersApplied = true;
    }
    if (selectedFilters['quiet']) {
        resultsText += ` for quiet venues,`;
        filtersApplied = true;
    }
    if (selectedFilters['quiet_zones']) {
        resultsText += ` with quiet zones,`;
        filtersApplied = true;
    }
    if (selectedFilters['playground']) {
        resultsText += ` with play area,`;
        filtersApplied = true;
    }
    if (selectedFilters['fenced']) {
        resultsText += ` with fenced play area,`;
        filtersApplied = true;
    }
    if (selectedFilters['colors']) {
        resultsText += ` with no flashy colors,`;
        filtersApplied = true;
    }
    if (selectedFilters['food_variey']) {
        resultsText += ` with food options,`;
        filtersApplied = true;
    }
    if (selectedFilters['smells']) {
        resultsText += ` with no extreme smells,`;
        filtersApplied = true;
    }
    if (selectedFilters['food_own']) {
        resultsText += ` where bringing your own food is allowed,`;
        filtersApplied = true;
    }
    if (selectedFilters['defined_duration']) {
        resultsText += ` with defined stay duration,`;
        filtersApplied = true;
    }

    // Remove trailing comma and display results text
    resultsText = resultsText.slice(0, -1) + ` for "${document.getElementById('inputbox').value}"`;
    document.getElementById('resultsText').innerText = resultsText;

    // Hide results text if no filters applied
    document.getElementById('resultsText').style.display = filtersApplied ? 'block' : 'none';
}

// Function to update the query placeholder with the selected filter text
function updateQueryPlaceholder(filterText) {
    document.getElementById('queryPlaceholder').innerText = filterText;
}
*/