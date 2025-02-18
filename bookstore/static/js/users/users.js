document.addEventListener("DOMContentLoaded", function () {
    var links = document.querySelectorAll(".link");
    var boxes = document.querySelectorAll(".box");
    let orderQuantity = document.querySelector('.order-quantity')

    // Function to show the selected section
    function showSection(id) {
        boxes.forEach(box => {
            box.classList.remove("active"); // Hide all sections
        });
        document.getElementById(id).classList.add("active"); // Show the selected section
    }

    // Attach click event to each link
    links.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault(); // Prevent page refresh
            var sectionId = this.id.replace("-link", ""); // Extract section id
            showSection(sectionId);
        });
    });

    // Show the first section by default
    showSection("orders");
});
