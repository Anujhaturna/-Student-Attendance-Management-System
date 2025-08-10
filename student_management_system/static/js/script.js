document.addEventListener("DOMContentLoaded", function () {
    // Function to handle class creation
    document.getElementById("createClassBtn").addEventListener("click", function () {
        let className = document.getElementById("classNameInput").value;
        if (className.trim() === "") {
            alert("Please enter a class name.");
            return;
        }
        // Send data to backend (AJAX or Fetch API)
        console.log("Creating class: " + className);
    });

    // Function to handle section creation
    document.getElementById("createSectionBtn").addEventListener("click", function () {
        let sectionName = document.getElementById("sectionNameInput").value;
        let selectedClass = document.getElementById("classSelect").value;
        if (sectionName.trim() === "" || selectedClass === "") {
            alert("Please select a class and enter a section name.");
            return;
        }
        // Send data to backend
        console.log("Creating section: " + sectionName + " for class " + selectedClass);
    });

    // Function to handle assigning class teacher
    document.getElementById("assignTeacherBtn").addEventListener("click", function () {
        let selectedTeacher = document.getElementById("teacherSelect").value;
        let selectedClass = document.getElementById("classTeacherSelect").value;
        if (selectedTeacher === "" || selectedClass === "") {
            alert("Please select both a class and a teacher.");
            return;
        }
        // Send data to backend
        console.log("Assigning teacher: " + selectedTeacher + " to class " + selectedClass);
    });
});
