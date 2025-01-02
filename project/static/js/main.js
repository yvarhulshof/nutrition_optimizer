document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('optimizationForm');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Gather form data
        const formData = {
            min_calories:  document.getElementById('min_calories').value,
            max_calories:  document.getElementById('max_calories').value,
            min_protein:   document.getElementById('min_protein').value,
            min_fiber:     document.getElementById('min_fiber').value,
            max_sugars:    document.getElementById('max_sugars').value,
            min_vitamin_c: document.getElementById('min_vitamin_c').value
        };

        try {
            // POST as JSON
            const response = await fetch('/optimize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            // We expect an HTML snippet in the response
            const htmlSnippet = await response.text();

            // Insert that HTML snippet into #result div
            document.getElementById('result').innerHTML = htmlSnippet;

        } catch (error) {
            console.error('Error:', error);
            document.getElementById('result').innerText = 'An error occurred. Check console.';
        }
    });
});
