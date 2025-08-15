document.addEventListener("change", (e) => {
    if (e.target.classList.contains("eligibility")) {
        let newValue = e.target.checked ? 1 : 0;
        let studentId = e.target.dataset.studentId; // assuming you store it in data attribute

        // Send to backend
        fetch("/update-eligibility", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                student_id: studentId,
                is_eligible: newValue
            })
        })
        .then(res => res.json())
        .then(data => {
            console.log("Server response:", data);
        })
        .catch(err => console.error("Error updating eligibility:", err));
    }
});


