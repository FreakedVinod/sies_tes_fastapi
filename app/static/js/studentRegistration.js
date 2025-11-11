        function loadCourses(streamId) {
        fetch(`/get-courses/${streamId}`)
            .then(response => response.json())
            .then(data => {
                const courseSelect = document.getElementById('course');
                courseSelect.innerHTML = '<option value="">-- Select Course --</option>';
                data.courses.forEach(course => {
                    const option = document.createElement('option');
                    option.value = course.id;
                    option.textContent = course.name;
                    courseSelect.appendChild(option);
                });
                // Reset classes when new stream selected
                document.getElementById('class').innerHTML = '<option value="">-- Select Class --</option>';
            });
        }

        document.getElementById('course').addEventListener('change', function () {
        const courseId = this.value;
        if (!courseId) return;

        fetch(`/get-classes/${courseId}`)
            .then(response => response.json())
            .then(data => {
                const classSelect = document.getElementById('class');
                classSelect.innerHTML = '<option value="">-- Select Class --</option>';
                data.classes.forEach(cls => {
                    const option = document.createElement('option');
                    option.value = cls.id;
                    option.textContent = cls.name;
                    classSelect.appendChild(option);
                });
            });
        });

        // Function to remove error state when user types again
        function clearError(fieldId, errorId) {
            const input = document.getElementById(fieldId);
            const errorMsg = document.getElementById(errorId);
            if (input && errorMsg) {
                input.classList.remove("error-input", "shake");
                errorMsg.style.display = "none";
            }
        }

        // Watch both email and roll number fields
        const emailInput = document.getElementById("email");
        const rollInput = document.getElementById("roll_number");

        if (emailInput) {
            emailInput.addEventListener("input", () => clearError("email", "email-error"));
        }

        if (rollInput) {
            rollInput.addEventListener("input", () => clearError("roll_number", "roll-error"));
        }