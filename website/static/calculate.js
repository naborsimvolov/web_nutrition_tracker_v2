
let addedMeals = [];
let suggestions = [];

function suggestMeals(inputText) {
    fetch(`/suggest-meals?query=${inputText}`)
        .then(response => response.json())
        .then(meals => {
            suggestions = meals;
            let suggestionList = document.getElementById('suggestionList');
            suggestionList.innerHTML = '';
            meals.forEach(meal => {
                let listItem = document.createElement('li');
                listItem.textContent = meal.name;
                listItem.className = 'list-group-item';
                listItem.onclick = function() {
                    document.getElementById('mealInput').value = meal.name;
                    suggestionList.innerHTML = '';
                };
                suggestionList.appendChild(listItem);
            });
        });
}

function addMealToList() {
    let mealName = document.getElementById('mealInput').value;
    let mealAmount = parseInt(document.getElementById('mealAmount').value);
    let meal = suggestions.find(m => m.name === mealName);

    if (meal && mealAmount > 0) {
        addedMeals.push({
            id: meal.id,
            name: meal.name,
            amount: mealAmount,
            calories: meal.calories,
            carbs: meal.carbs,
            proteins: meal.proteins,
            fats: meal.fats
        });
        updateAddedMealsList();
        document.getElementById('mealInput').value = '';
        document.getElementById('mealAmount').value = '';
    }
}

function updateAddedMealsList() {
    let listElement = document.getElementById('addedMealsList');
    listElement.innerHTML = '';
    addedMeals.forEach((meal, index) => {
        let listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        listItem.innerHTML = `${meal.name} - ${meal.amount}g
            <button class="btn btn-danger btn-sm" onclick="removeMealFromList(${index})">Remove</button>`;
        listElement.appendChild(listItem);
    });
}

function removeMealFromList(index) {
    addedMeals.splice(index, 1);
    updateAddedMealsList();
}

function calculateTotalNutrition() {
    let totalCalories = 0, totalCarbs = 0, totalProteins = 0, totalFats = 0;
    addedMeals.forEach(meal => {
        totalCalories += meal.calories * meal.amount / 100;
        totalCarbs += meal.carbs * meal.amount / 100;
        totalProteins += meal.proteins * meal.amount / 100;
        totalFats += meal.fats * meal.amount / 100;
    });
    document.getElementById('totalCalories').textContent = `Total Calories: ${totalCalories.toFixed(1)}`;
    document.getElementById('totalCarbs').textContent = `Total Carbs: ${totalCarbs.toFixed(1)}g`;
    document.getElementById('totalProteins').textContent = `Total Proteins: ${totalProteins.toFixed(1)}g`;
    document.getElementById('totalFats').textContent = `Total Fats: ${totalFats.toFixed(1)}g`;
    document.getElementById('totalNutritionDisplay').style.display = 'block';
}