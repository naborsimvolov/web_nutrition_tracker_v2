function deleteMeal(mealId) {
    fetch(`/delete-meal/${mealId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({ mealId: mealId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // rmove  deleted meal from list without reloading page
        const mealItem = document.getElementById(`meal-${mealId}`);
        if (mealItem) {
            mealItem.remove();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// add a meal
function addMeal() {
    const mealName = document.getElementById('mealName').value;
    const calories = document.getElementById('calories').value;
    const carbs = document.getElementById('carbs').value;
    const proteins = document.getElementById('proteins').value;
    const fats = document.getElementById('fats').value;

    const mealData = {
        mealName: mealName,
        calories: calories,
        carbs: carbs,
        proteins: proteins,
        fats: fats
    };

    fetch('/add-meal', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(mealData)
    })
    .then(async response => {
        let data;
        try {
            data = await response.json();
        } catch (e) {
            console.error('Error parsing JSON:', e);
            alert('An unexpected error occurred.');
            throw new Error('Invalid JSON response');
        }

        if (response.ok) {
            return data;
        } else {
            let errorMessage = data.error || 'An error occurred';
            if (errorMessage === 'A meal with this name already exists. Please delete it first if you wish to overwrite it.') {
                alert('Meal with this name already exists in your database. Please delete the existing meal first.');
            }
            throw new Error(errorMessage);
        }
    })
    .then(data => {
        // clear input fields
        document.getElementById('mealName').value = '';
        document.getElementById('calories').value = '';
        document.getElementById('carbs').value = '';
        document.getElementById('proteins').value = '';
        document.getElementById('fats').value = '';

        // for success
        alert('Meal successfully added to your database.');
        searchMeals('');
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
//search meals
function searchMeals(query) {
    if (query.trim() === '') {
        document.getElementById('mealsList').innerHTML = ''; // clear list if query is empty
        return;
    }
    fetch(`/search-meals?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(meals => {
            let mealsList = document.getElementById('mealsList');
            mealsList.innerHTML = '';

            meals.forEach(meal => {
                let listItem = document.createElement('li');
                listItem.className = 'list-group-item';
                listItem.id = `meal-${meal.id}`;  // id to each meal item
                listItem.innerHTML = `
                    Name: ${meal.name}, Calories: ${meal.calories}, Carbs: ${meal.carbs}g, Proteins: ${meal.proteins}g, Fats: ${meal.fats}g
                    <button onclick="deleteMeal(${meal.id})" class="btn btn-danger btn-sm float-right">Delete</button>
                `;
                mealsList.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
