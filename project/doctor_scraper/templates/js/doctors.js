// Fetch the doctors when the page loads
document.addEventListener('DOMContentLoaded', function () {
    fetch('http://127.0.0.1:8000/doctors')
        .then(response => response.json())
        .then(data => displayDoctors(data));
});

// Function to display doctors
function displayDoctors(doctors) {
    const doctorsDiv = document.getElementById('doctors');
    doctorsDiv.innerHTML = '';  // Clear the div

    for (let doctor of doctors) {
        // Create the HTML for each doctor
        const doctorHTML = `
            <div class="col-md-4">
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">${doctor.name}</h5>
                        <p class="card-text">${doctor.specialty}</p>
                        <p class="card-text">${doctor.institution.name}</p>
                        <p class="card-text">Distance: ${doctor.distance}</p>
                        <a href="doctor.html?id=${doctor.id}" class="btn btn-primary">View Profile</a>
                    </div>
                </div>
            </div>
        `;
        doctorsDiv.innerHTML += doctorHTML;
    }
}

// Handle the search
document.getElementById('search').addEventListener('input', function (event) {
    const query = event.target.value;
    fetch('http://127.0.0.1:8000/doctors?search=' + query)
        .then(response => response.json())
        .then(data => displayDoctors(data));
});
