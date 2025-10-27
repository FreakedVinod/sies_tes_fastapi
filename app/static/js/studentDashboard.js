// Auto-hide the alert after 3 seconds
const alertBox = document.getElementById("feedback-alert");
if (alertBox) {
    setTimeout(() => {
        alertBox.style.transition = "opacity 0.5s ease";
        alertBox.style.opacity = "0";
        setTimeout(() => alertBox.remove(), 500); // remove from DOM after fade
    }, 3000);
}

document.addEventListener('DOMContentLoaded', () => {
    const feedbackModal = document.getElementById('feedback-modal');
            const closeModalBtn = document.getElementById('close-modal-btn');
            const feedbackForm = document.getElementById('feedback-form');
            const questionsContainer = document.getElementById('questions-container');
            const giveFeedbackButtons = document.querySelectorAll('.give-feedback-btn');
            const alertMessage = document.getElementById('alert-message');

            // Function to show/hide the modal
            function toggleModal(open = true) {
                if (open) {
                    feedbackModal.classList.remove('opacity-0', 'pointer-events-none');
                    document.body.style.overflow = 'hidden'; // Prevents scrolling
                } else {
                    feedbackModal.classList.add('opacity-0', 'pointer-events-none');
                    document.body.style.overflow = '';
                }
            }

            // Close modal when clicking on the 'x' button or outside
            closeModalBtn.addEventListener('click', () => toggleModal(false));
            feedbackModal.addEventListener('click', (e) => {
                if (e.target === feedbackModal) {
                    toggleModal(false);
                }
            });

            // Handle "Give Feedback" button clicks
            giveFeedbackButtons.forEach(button => {
                button.addEventListener('click', async (e) => {
                    const teacherSubjectId = e.target.dataset.teacher-subject-id;
                    
                    // Set the hidden input value
                    document.getElementById('teacherSubjectId').value = teacherSubjectId;

                    // Fetch questions from the FastAPI endpoint
                    try {
                        const response = await fetch(`/feedback/${teacherSubjectId}`);
                        if (!response.ok) {
                            throw new Error('Failed to load feedback questions.');
                        }
                        const questionsHtml = await response.text();
                        questionsContainer.innerHTML = questionsHtml;
                        toggleModal(true);
                    } catch (error) {
                        console.error('Error fetching feedback questions:', error);
                        // Use a custom modal instead of alert in a real app
                        alertMessage.textContent = error.message;
                        alertMessage.classList.remove('hidden');
                        alertMessage.classList.add('bg-red-100', 'text-red-700');
                    }
                });
            });

            // Handle form submission
            feedbackForm.addEventListener('submit', async (e) => {
                e.preventDefault();

                const formData = new FormData(feedbackForm);
                const responses = {};
                let allAnswered = true;

                // Loop through all questions to check if they have a rating
                const questionDivs = questionsContainer.querySelectorAll('.question');
                questionDivs.forEach(div => {
                    const questionId = div.querySelector('p').innerText.split('.')[0].trim();
                    const rating = formData.get(`q${questionId}_rating`);
                    if (rating) {
                        responses[`responses[${questionId}]`] = rating;
                    } else {
                        allAnswered = false;
                    }
                });

                if (!allAnswered) {
                    alertMessage.textContent = "Please answer all questions before submitting.";
                    alertMessage.classList.add('bg-red-100', 'text-red-700');
                    alertMessage.classList.remove('hidden');
                    return;
                }

                // Append the teacher_subject_id to the new FormData object
                const submitFormData = new FormData();
                submitFormData.append('teacher_subject_id', document.getElementById('teacherSubjectId').value);
                for (const key in responses) {
                    submitFormData.append(key, responses[key]);
                }
                
                try {
                    const response = await fetch('/submit-feedback', {
                        method: 'POST',
                        body: submitFormData,
                    });

                    if (response.redirected) {
                        window.location.href = response.url;
                    } else {
                        // Handle potential non-redirect responses
                        const result = await response.json();
                        console.log(result);
                        alertMessage.textContent = "Feedback submitted successfully!";
                        alertMessage.classList.add('bg-green-100', 'text-green-700');
                        alertMessage.classList.remove('hidden');
                        toggleModal(false);
                    }
                } catch (error) {
                    console.error('Submission error:', error);
                    alertMessage.textContent = "An error occurred during submission.";
                    alertMessage.classList.add('bg-red-100', 'text-red-700');
                    alertMessage.classList.remove('hidden');
                }
            });
            
            // Check for success/error query parameters and display alert
            const urlParams = new URLSearchParams(window.location.search);
            const successParam = urlParams.get('success');
            const errorParam = urlParams.get('error');

            if (successParam === '1') {
                alertMessage.textContent = "Feedback submitted successfully!";
                alertMessage.classList.add('bg-green-100', 'text-green-700');
                alertMessage.classList.remove('hidden');
            } else if (errorParam === '1') {
                alertMessage.textContent = "You have already submitted feedback for this module.";
                alertMessage.classList.add('bg-red-100', 'text-red-700');
                alertMessage.classList.remove('hidden');
            }
        });