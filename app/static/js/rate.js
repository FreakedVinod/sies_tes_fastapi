document.addEventListener("DOMContentLoaded", () => {
    const starRatings = document.querySelectorAll(".star-rating");

    starRatings.forEach(ratingDiv => {
        const stars = ratingDiv.querySelectorAll(".star");
        const input = ratingDiv.querySelector("input[type=hidden]");

        stars.forEach(star => {
            // Hover effect (preview)
            star.addEventListener("mouseover", () => {
                const value = parseInt(star.dataset.value);
                highlightStars(stars, value);
            });

            // Reset to saved value on mouseout
            star.addEventListener("mouseout", () => {
                resetStars(stars, input.value);
            });

            // Click = save rating
            star.addEventListener("click", () => {
                const value = parseInt(star.dataset.value);
                input.value = value; // ✅ hidden input gets updated
                highlightStars(stars, value);
            });
        });

        // Ensure correct state on page load
        resetStars(stars, input.value);
    });

    function highlightStars(stars, value) {
        stars.forEach(star => {
            star.classList.toggle("selected", parseInt(star.dataset.value) <= value);
        });
    }

    function resetStars(stars, value) {
        stars.forEach(star => {
            star.classList.toggle("selected", parseInt(star.dataset.value) <= value);
        });
    }
});
