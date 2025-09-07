document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("feedbackModal");
    const closeModal = document.getElementById("closeModal");
    const modalContent = document.getElementById("modalContent");

    // When subject row is clicked
    document.querySelectorAll(".subject-row").forEach(row => {
        row.addEventListener("click", async () => {
            const subjectId = row.dataset.subjectId;
            try {
                const response = await fetch(`/rate/${subjectId}`);
                const html = await response.text();
                modalContent.innerHTML = html; // load rate.html inside modal
                modal.classList.remove("hidden");
            } catch (err) {
                console.error("Error loading questions:", err);
            }
        });
    });

    // Close modal
    closeModal.addEventListener("click", () => {
        modal.classList.add("hidden");
        modalContent.innerHTML = "";
    });
});

// Placeholder for future AJAX or dynamic updates
document.addEventListener("DOMContentLoaded", () => {
    console.log("Module Rating page loaded");
});

