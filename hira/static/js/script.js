document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.querySelector(".hamburger");
  const mobileMenu = document.querySelector(".mobile-menu");

  hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    mobileMenu.classList.toggle("active");
  });

  // Close mobile menu when clicking outside
  document.addEventListener("click", (event) => {
    if (
      !hamburger.contains(event.target) &&
      !mobileMenu.contains(event.target)
    ) {
      hamburger.classList.remove("active");
      mobileMenu.classList.remove("active");
    }
  });

  // Close mobile menu when window is resized to larger screen
  window.addEventListener("resize", () => {
    if (window.innerWidth >= 768) {
      // 768px is the breakpoint for md in Tailwind
      hamburger.classList.remove("active");
      mobileMenu.classList.remove("active");
    }
  });
});
