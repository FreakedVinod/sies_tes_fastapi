// Toggle Eligibility
async function updateEligibility(studentId, newStatus) {
  const formData = new FormData();
  formData.append("student_id", studentId);
  formData.append("is_eligible", newStatus);

  const response = await fetch("/admin/update-eligibility", { method: "POST", body: formData });
  if (response.ok) location.reload();
  else alert("Failed to update eligibility.");
}

// Delete Student
async function deleteStudent(studentId) {
  if (!confirm("Are you sure you want to delete this student?")) return;
  const response = await fetch(`/admin/delete-student/${studentId}`, { method: "DELETE" });
  if (response.ok) location.reload();
  else alert("Failed to delete student.");
}

// Open/Close Modal
function openModal(id) { document.getElementById(id).style.display = "flex"; }
function closeModal(id) { document.getElementById(id).style.display = "none"; }

// Open Update Modal with Prefilled Data
function openUpdateModal(id, name, roll, classId, year) {
  document.getElementById("update_student_id").value = id;
  document.getElementById("update_name").value = name;
  document.getElementById("update_roll_no").value = roll;
  document.getElementById("update_class_id").value = classId;
  document.getElementById("update_year").value = year;
  openModal("updateModal");
}

// Handle Add Form
document.getElementById("addForm").onsubmit = async function(e) {
  e.preventDefault();
  const formData = new FormData(this);
  const response = await fetch("/admin/add-student", { method: "POST", body: formData });
  if (response.ok) location.reload();
  else alert("Failed to add student.");
};

// Handle Update Form
document.getElementById("updateForm").onsubmit = async function(e) {
  e.preventDefault();
  const formData = new FormData(this);
  const response = await fetch("/admin/update-student", { method: "POST", body: formData });
  if (response.ok) location.reload();
  else alert("Failed to update student.");
};
