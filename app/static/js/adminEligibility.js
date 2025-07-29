async function fetchStudents() {
            const response = await fetch('/admin/students');
            const data = await response.json();
            const tableBody = document.getElementById('student-table');

            data.students.forEach(student => {
                const row = document.createElement('tr');

                row.innerHTML = `
                    <td>${student.roll_no}</td>
                    <td>${student.name}</td>
                    <td>${student.class_id}</td>
                    <td>
                        <input type="checkbox" class="toggle-btn" ${student.is_eligible ? 'checked' : ''} 
                            onchange="updateEligibility(${student.student_id}, this.checked)">
                    </td>
                `;
                tableBody.appendChild(row);
            });
        }

        async function updateEligibility(studentId, isEligible) {
            await fetch('/admin/update-eligibility', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `student_id=${studentId}&is_eligible=${isEligible}`
            });
        }

        fetchStudents();