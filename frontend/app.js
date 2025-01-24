document.addEventListener('DOMContentLoaded', () => {
    document.getElementById("suggest-activities-btn").addEventListener("click", () => {
        
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;

                    console.log("User's location fetched:", latitude, longitude);

                    try {
                        
                        const response = await fetch("/weather", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({ latitude, longitude }),
                        });

                        if (!response.ok) {
                            throw new Error("Failed to fetch weather data.");
                        }

                        const weatherData = await response.json();
                        console.log("Weather Data:", weatherData);

                       
                        if (weatherData.activity_suggestions) {
                            const activitiesContainer = document.getElementById("activity-suggestions");
                            activitiesContainer.innerHTML = ""; 

                            
                            if (weatherData.activity_suggestions.indoor && weatherData.activity_suggestions.indoor.length > 0) {
                                console.log("Indoor Activities:", weatherData.activity_suggestions.indoor);
                                
                                const indoorCard = createIndoorActivityCard(weatherData.activity_suggestions.indoor);
                                activitiesContainer.appendChild(indoorCard);
                            }

                           
                            if (weatherData.activity_suggestions.outdoor && weatherData.activity_suggestions.outdoor.length > 0) {
                                console.log("Outdoor Activities:", weatherData.activity_suggestions.outdoor);
                                
                                const outdoorCard = createOutdoorActivityCard(weatherData.activity_suggestions.outdoor);
                                activitiesContainer.appendChild(outdoorCard);
                            }

                           
                            if (activitiesContainer.children.length === 0) {
                                activitiesContainer.innerHTML = "<p>No activities found.</p>";
                            }
                        } else {
                            alert("No activities found.");
                        }
                    } catch (error) {
                        console.error("Error:", error);
                        alert("Error fetching weather data.");
                    }
                },
                (error) => {
                    console.error("Error getting location:", error);
                    alert("Unable to get your location. Please enable location services.");
                }
            );
        } else {
            alert("Geolocation is not supported by your browser.");
        }
    });
});

function createIndoorActivityCard(activities) {
    const card = document.createElement('div');
    card.classList.add('activity-card');
    

    const categoryHeading = document.createElement('h3');
    categoryHeading.innerText = 'Indoor Activities';
    card.appendChild(categoryHeading);

    activities.forEach(activityText => {
     
        const activityLines = activityText.split('\n'); 
        
        activityLines.forEach(activity => {
            if (activity.trim()) { 
                const activityContainer = document.createElement('div');
                activityContainer.classList.add('activity-container');
                activityContainer.style.border = "1px solid #ddd";
                activityContainer.style.margin = "10px 0";
                activityContainer.style.padding = "10px";
                activityContainer.style.borderRadius = "8px";


                
                const activityInfo = document.createElement('span');
                activityInfo.classList.add('activity-info');
                activityInfo.innerText = activity.trim();
                activityInfo.style.color = 'white';
                activityContainer.appendChild(activityInfo);

                
                const heartIcon = document.createElement('span');
                heartIcon.classList.add('heart-icon');
                heartIcon.innerHTML = '♥'; 
                heartIcon.style.cursor = 'pointer';
                heartIcon.style.fontSize = '1.5rem';
                heartIcon.style.color = '#ccc'; 
                heartIcon.onclick = function () {
                    togglePreference(activity, heartIcon); 
                };

             
                heartIcon.onmouseover = function () {
                    heartIcon.style.color = '#f00'; 
                };
                heartIcon.onmouseout = function () {
                    if (!heartIcon.classList.contains('liked')) {
                        heartIcon.style.color = '#ccc'; 
                    }
                };

              
                activityContainer.appendChild(heartIcon);

               
                card.appendChild(activityContainer);
            }
        });
    });

    return card;
}


function createOutdoorActivityCard(activities) {
    const card = document.createElement('div');
    card.classList.add('activity-card'); 

   
    const categoryHeading = document.createElement('h3');
    categoryHeading.innerText = 'Outdoor Activities';
    card.appendChild(categoryHeading);

   
    if (activities.length === 1 && typeof activities[0] === 'string') {

        activities = activities[0].split("\n\n");
    }

   
    activities.forEach((activityBlock, index) => {
        const activityDetails = activityBlock.split("\n");

     
        if (activityDetails.length < 3) return;

       
        const activityName = activityDetails[0].replace("Outdoor Activity: ", "").trim();
        const place = activityDetails[1].replace("- Place: ", "").trim();

       
        const mapMarkdown = activityDetails[2].match(/\[(.*?)\]\((.*?)\)/);
        const mapText = mapMarkdown ? mapMarkdown[1] : 'View on Map'; 
        const mapLink = mapMarkdown ? mapMarkdown[2] : '#'; 

      
        const activityContainer = document.createElement('div');
        activityContainer.classList.add('activity-container');
        activityContainer.style.border = "1px solid #ddd";
        activityContainer.style.margin = "10px 0";
        activityContainer.style.padding = "10px";
        activityContainer.style.borderRadius = "8px";

       
        activityContainer.innerHTML = `
            <p><strong>${index + 1}. Activity:</strong> ${activityName}</p>
            <p><strong>Place:</strong> ${place}</p>
            <p><strong>Map:</strong> <a href="${mapLink}" target="_blank">${mapText}</a></p>
        `;

       
        const heartIcon = document.createElement('span');
        heartIcon.classList.add('heart-icon');
        heartIcon.innerHTML = '♥'; 
        heartIcon.style.cursor = 'pointer';
        heartIcon.style.fontSize = '1.5rem';
        heartIcon.style.color = '#ccc'; 

        heartIcon.onclick = function () {
            togglePreference(activityName, heartIcon);
        };
            

       
        heartIcon.onmouseover = function () {
            heartIcon.style.color = '#f00'; 
        };
        heartIcon.onmouseout = function () {
            if (!heartIcon.classList.contains('liked')) {
                heartIcon.style.color = '#ccc';
            }
        };

       
        activityContainer.appendChild(heartIcon);

     
        card.appendChild(activityContainer);
    });

    return card;
}



function togglePreference(activity, heartIcon) {
    const isLiked = heartIcon.classList.contains('liked');
    const url = isLiked
        ? `/preferences/remove?preference=${encodeURIComponent(activity)}`
        : `/preferences/add?preference=${encodeURIComponent(activity)}`;

  
    const sessionId = localStorage.getItem('session_id'); e



    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Session-ID': sessionId,
        },
        body: JSON.stringify({ activity }) 
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update preferences.');
            }
            return response.json();
        })
        .then(data => {
           
            if (isLiked) {
                heartIcon.classList.remove('liked');
                heartIcon.style.color = '#ccc'; 
            } else {
                heartIcon.classList.add('liked');
                heartIcon.style.color = '#f00'; 
            }
            console.log(data.message); 
        })
        .catch(error => {
            console.error('Error updating preferences:', error);
        });
}
