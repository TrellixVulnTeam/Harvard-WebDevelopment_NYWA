document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form').onsubmit = () => {

        // Initialize new request
        const request = new XMLHttpRequest(); //new object that makes a AJAX/HTTP request to server to get information
        const currency = document.querySelector('#currency').value; //user input
        request.open('POST', '/convert'); //initialise a new request

        // Callback function for when request completes loading
        request.onload = () => {

            // Extract JSON data from request return
            const data = JSON.parse(request.responseText);

            // Update the result div
            if (data.success) {
                const contents = `1 USD is equal to ${data.rate} ${currency}.`
                document.querySelector('#result').innerHTML = contents;
            }
            else {
                document.querySelector('#result').innerHTML = 'There was an error.';
            }
        }

        // Add data to send with request
        const data = new FormData();
        data.append('currency', currency);

        // Send request
        request.send(data);
        return false;
    };

});
