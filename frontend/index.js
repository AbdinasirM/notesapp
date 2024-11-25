// Endpoint and token
const endpoint = "http://127.0.0.1:8000/api/v1/protected-resource"; // Replace with your API URL
const token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYzBiMGVkN2UtM2U1ZS00YWY1LWI1ZWEtMmMyOTEwOWY0YjNjIiwiZXhwIjoxNzMyMjQzNDA3LCJpYXQiOjE3MzIyNDMyMjd9.cTGFVuvCH7UMjunIYj1S1qv9MebtFBESqXttvbAdXs8"; // Replace with your actual JWT token

// Fetch request
fetch(endpoint, {
    method: "GET",
    headers: {
        "Authorization": token // Attach the token in the Authorization header
    }
})
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json(); // Parse JSON response
    })
    .then(data => {
        console.log("Success:", data); // Handle the successful response
    })
    .catch(error => {
        console.error("Error:", error); // Handle errors
    });
