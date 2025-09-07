document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".stars").forEach(starContainer => {
    const stars = starContainer.querySelectorAll("i");
    const hiddenInput = starContainer.nextElementSibling;

    stars.forEach(star => {
      star.addEventListener("mouseover", () => {
        resetStars(stars);
        highlightStars(stars, star.dataset.value);
      });

      star.addEventListener("mouseout", () => {
        resetStars(stars);
        if (hiddenInput.value) {
          highlightStars(stars, hiddenInput.value);
        }
      });

      star.addEventListener("click", () => {
        hiddenInput.value = star.dataset.value;
        resetStars(stars);
        highlightStars(stars, star.dataset.value);
      });
    });
  });

  function resetStars(stars) {
    stars.forEach(s => s.classList.remove("fa-solid", "selected"));
    stars.forEach(s => s.classList.add("fa-regular"));
  }

  function highlightStars(stars, count) {
    for (let i = 0; i < count; i++) {
      stars[i].classList.remove("fa-regular");
      stars[i].classList.add("fa-solid", "selected");
    }
  }
});
