$(document).ready(function () {
    $("#addClassBtn").click(function (e) {
        e.preventDefault(); // Prevent form from reloading

        let className = $("#classNameInput").val().trim();
        let classTeacher = $("#classTeacherSelect").val();
        let csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        if (!className) {
            alert("Class Name is required!");
            return;
        }

        $.ajax({
            url: "/add-class/",  // Adjust the URL to your backend route
            type: "POST",
            data: {
                class_name: className,
                class_teacher: classTeacher,
                csrfmiddlewaretoken: csrfToken,
            },
            success: function (response) {
                if (response.status === "success") {
                    let newRow = `
                        <tr id="classRow_${response.class_id}" style="display: none;">
                            <td>${response.class_name}</td>
                            <td>${response.class_teacher || "Not Assigned"}</td>
                            <td>
                                <button class="delete-btn" data-id="${response.class_id}">Delete</button>
                            </td>
                        </tr>`;

                    $("#classTable tbody").append(newRow);
                    $(`#classRow_${response.class_id}`).fadeIn(500); // Fade-in animation

                    $("#classNameInput").val(""); // Clear input field
                    $("#classTeacherSelect").val(""); // Reset dropdown
                } else {
                    alert(response.message || "Failed to add class.");
                }
            },
            error: function () {
                alert("Error occurred while adding class.");
            }
        });
    });

    // DELETE CLASS FUNCTIONALITY
    $(document).on("click", ".delete-btn", function () {
        let classId = $(this).data("id");
        let row = $(this).closest("tr");
        let csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        if (!confirm("Are you sure you want to delete this class?")) return;

        $.ajax({
            url: `/delete-class/${classId}/`,
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrfToken,
            },
            success: function (response) {
                if (response.status === "success") {
                    row.fadeOut(500, function () {
                        $(this).remove();
                    });
                } else {
                    alert(response.message || "Failed to delete class.");
                }
            },
            error: function () {
                alert("Error deleting class.");
            }
        });
    });
});
