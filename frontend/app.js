document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const student = {
        student_id: document.getElementById('student_id').value,
        name: document.getElementById('name').value,
        age: parseInt(document.getElementById('age').value),
        grade: document.getElementById('grade').value
    };
    
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = '';

    try {
        const response = await fetch('http://backend-service/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(student)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Registration failed');
        }
        
        alert('Student registered successfully!');
        document.getElementById('register-form').reset();
    } catch (error) {
        errorDiv.textContent = error.message;
    }
});