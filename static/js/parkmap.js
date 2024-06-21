// Get all square elements
const squares = document.querySelectorAll(".square");
const selectedSlotInput = document.getElementById("selected-slot");
const alert = document.getElementById("alert");

// Add event listener to each square
squares.forEach((square) => {
  square.addEventListener("click", () => {
    // Reset background color of all squares
    squares.forEach((otherSquare) => {
      otherSquare.style.backgroundColor = "#f28500";
      otherSquare.style.color = "white";
    });

    // Change color of the clicked square to yellow
    square.style.backgroundColor = "rgb(2, 192, 2)";
    square.style.color = "white";
    selectedSlotInput.value = square.textContent;
  });
});

// Add event listener to the document
document.addEventListener("click", (event) => {
  // Check if the clicked element is not a square or the select button
  if (!event.target.classList.contains("square")) {
    // Reset colors to initial values
    squares.forEach((square) => {
      square.style.backgroundColor = "#f28500";
      square.style.color = "white";
    });
  }
});
