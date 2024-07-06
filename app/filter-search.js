async function fetchVenues() {
    let query = document.getElementById('search-query').value;
    let filters = document.getElementById('filters').value;
    let response = await fetch(`/api/discover?query=${query}&filters=${encodeURIComponent(filters)}`);
    let data = await response.json();
    updateResults(data.venues);
}

function toggleFilter(element, filterName) {
    element.classList.toggle('selected');
    element.classList.toggle('unselected');
    updateFilters();
}

function updateFilters() {
    let filters = {};
    document.querySelectorAll('.filterbtn.selected').forEach(function(el) {
        let filterName = el.getAttribute('data-filter');
        if (filterName === 'smells' || filterName === 'colors') {
            filters[filterName] = 2;  // Set a fixed value of 2 for smells and colors
        } else if (filterName === 'food_variey') {
            filters[filterName] = 3;  // Set a fixed value of 3 for food_variey
        } else if (filterName === 'defined_duration') {
            filters[filterName] = 'NO';  // Set 'NO' for defined_duration instead of 'YES'
        } else {
            filters[filterName] = 'YES';
        }
    });
    document.getElementById('filters').value = JSON.stringify(filters);
    fetchVenues();
}



function updateResults(venues) {
    let resultsContainer = document.querySelector('.results-container');
    resultsContainer.innerHTML = '';

    if (venues.length > 0) {
        let ol = document.createElement('ol');
        venues.forEach(venue => {
            let li = document.createElement('li');
            li.classList.add('listedvenue', 'border');
            li.style.listStyle = 'none';
            li.style.marginBottom = '20px';

            li.innerHTML = `
                <div style="margin-top: -20px;">
                    <h2 class="listtitle" style="margin-left: -12px;">
                        <a href="/venue/${venue.id}">${venue.name}</a>
                    </h2>
                    <div class="maingrid">
                        <div>
                            <div class="sparent2" style="margin-top: -15px;">
                                <img class="same" style="height: 17px; width: 17px; margin-right: 5px;" src="/static/images/icons8-marker-100.png" alt="">
                                <p class="same">${venue.address}</p>
                            </div>
                            <img src="${venue.photo_url}" alt="${venue.name}" class="listimg same" style="margin-top: 20px;">
                        </div>
                        <div class="listrate">
                            <div class="sameparent" style="display: flex; align-items: center; justify-content: space-between; width: 300px;">
                                <p class="same">Crowd</p>
                                <svg class="same" width="100" height="20" xmlns="http://www.w3.org/2000/svg">
                                    ${generateRatingSVG(venue.crowdedness)}
                                </svg>
                            </div>
                            <div class="sameparent" style="margin-top: -15px; display: flex; align-items: center; justify-content: space-between; width: 300px;">
                                <p class="same">Noise</p>
                                <svg class="same" width="100" height="20" xmlns="http://www.w3.org/2000/svg">
                                    ${generateRatingSVG(venue.quiet)}
                                </svg>
                            </div>
                            ${generateCriteriaHTML(venue)}
                        </div>
                    </div>
                </div>
            `;
            ol.appendChild(li);
        });
        resultsContainer.appendChild(ol);
    } else {
        let message = document.createElement('div');
        message.style.marginRight = '350px';
        message.style.marginTop = '40px';
        message.innerHTML = `<p style="font-size: 20px;">No venues found matching your criteria.</p>`;
        resultsContainer.appendChild(message);
    }
}

function generateRatingSVG(rating) {
    let svg = '';
    for (let i = 0; i < 5; i++) {
        svg += `<circle style="fill: ${i < rating ? getRatingColor(rating) : '#EDDEA4'}" cx="${8 + i * 15}" cy="10" r="5.5" class="circle" />`;
    }
    return svg;
}

function getRatingColor(rating) {
    if (rating <= 2) {
        return '#429B80'; // Green
    } else if (rating === 3) {
        return '#E4C23B'; // Yellow
    } else {
        return '#F77272'; // Red
    }
}

function generateCriteriaHTML(venue) {
    let html = '';
    if (venue.food_variey >= 3) {
        html += `<p class="ratingyes">+ Broader variety of food</p>`;
    } else {
        html += `<p class="ratingno">- Limited food variety</p>`;
    }

    if (venue.food_own === 'YES') {
        html += `<p class="ratingyes">+ Bringing your own food allowed</p>`;
    } else {
        html += `<p class="ratingno">- Bringing your own food not allowed</p>`;
    }

    if (venue.defined_duration === 'NO') {
        html += `<p class="ratingyes">+ No defined time frame</p>`;
    }

    if (venue.quiet_zones === 'YES') {
        html += `<p class="ratingyes"> + Quiet zones available</p>`;
    } else {
        html += `<p class="ratingno">- No quiet zones available</p>`;
    }

    if (venue.playground === 'YES') {
        html += `<p class="ratingyes"> + Play area available</p>`;
    }

    if (venue.fenced === 'YES') {
        html += `<p class="ratingyes"> + Fenced play area</p>`;
    }

    if (venue.colors <= 2) {
        html += `<p class="ratingyes"> + No flashy colors</p>`;
    } else {
        html += `<p class="ratingno">- Flashy colors might be apparent</p>`;
    }

    if (venue.smells <= 2) {
        html += `<p class="ratingyes"> + No extreme smells</p>`;
    } else {
        html += `<p class="ratingno">- Extreme smells might be apparent</p>`;
    }

    return html;
}

function initializeFilters() {
    const filters = JSON.parse('{{ filters }}'.replace(/&quot;/g, '"'));
    for (const [key, value] of Object.entries(filters)) {
        if (value === 'YES') {
            const filterBtn = document.querySelector(`.filterbtn[data-filter="${key}"]`);
            if (filterBtn) {
                filterBtn.classList.add('selected');
                filterBtn.classList.remove('unselected');
            }
        }
    }
}

window.onload = function() {
    initializeFilters();
    fetchVenues();
};