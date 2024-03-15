document.addEventListener("DOMContentLoaded", function() {
    const buttons = document.querySelectorAll(".form-button");
    const uploadOptions = document.querySelectorAll(".upload-option");
    const runButton = document.getElementById("run-button");

    buttons.forEach(button => {
        button.addEventListener("click", function() {
            // Remove 'selected' class from all buttons
            buttons.forEach(btn => btn.classList.remove("selected"));
            // Add 'selected' class to the clicked button
            button.classList.add("selected");

            // Hide all upload options
            uploadOptions.forEach(option => {
                option.style.display = "none";
            });

            // Show the corresponding upload option
            var optionId;
            switch (button.id) {
                case 'btn1':
                    optionId = 'textfile';
                    break;
                case 'btn2':
                    optionId = 'package';
                    break;
                case 'btn3':
                    optionId = 'link';
                    break;
            }
            document.getElementById(optionId).style.display = "block";
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const loadingBar = document.getElementById('loading-bar');
    const uploadForm = document.getElementById('upload-form');
    const uploadOptions = document.querySelectorAll('.upload-option input');

    // Function to check if any input field in upload-options is filled
    function areInputsFilled() {
        let inputsFilled = false;
        uploadOptions.forEach(option => {
            if (option.value.trim() !== '') {
                inputsFilled = true;
            }
        });
        return inputsFilled;
    }

    // Disable the "Run" button initially
    document.getElementById('run-button').disabled = true;

    // Enable the "Run" button when any input in upload-options is filled
    uploadOptions.forEach(option => {
        option.addEventListener('input', function() {
            document.getElementById('run-button').disabled = !areInputsFilled();
            if (areInputsFilled()) {
                document.getElementById('run-button').textContent = 'Run';
            } else {
            document.getElementById('run-button').textContent = 'Select package(s) to scan';
            }
        });
    });

    // Show loading bar when form is submitted
    uploadForm.addEventListener('submit', function() {
        loadingBar.style.display = 'block';
    });

    // Hide loading bar when result or error is displayed
    const resultElement = document.querySelector('.result');
    const errorElement = document.querySelector('.error');

    if (resultElement || errorElement) {
        loadingBar.style.display = 'none';
    }
});
