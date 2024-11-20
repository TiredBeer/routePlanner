document.getElementById('searchButton').addEventListener('click', () => {
  const address = document.getElementById('address').value;
  const radius = document.getElementById('radius').value;
  const placeTypes = Array.from(document.getElementById('placeTypes').selectedOptions)
                          .map(option => option.value);

  if (!address || !radius || placeTypes.length === 0) {
    alert('Пожалуйста, заполните все поля!');
    return;
  }

  const requestData = {
    address: address,
    radius: parseFloat(radius),
    place_type: placeTypes
  };

  // Отправка данных на бэкенд
  fetch('http://127.0.0.1:8080/api/places/search/', {  // Добавлен / в конце URL
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestData)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Ответ от сервера не OK');
    }
    return response.json();
  })
  .then(data => {
  console.log('Полученные данные:', data);  // Добавьте это для отладки
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = ''; // Очистка предыдущих результатов

  if (data && Array.isArray(data.results) && data.results.length > 0) {
    data.results.forEach(place => {
      const placeElement = document.createElement('div');
      placeElement.textContent = `Название: ${place.name}, Адрес: ${place.address}`;
      resultsDiv.appendChild(placeElement);
    });
  } else {
    resultsDiv.textContent = 'Нет результатов.';
  }
})

  .catch(error => {
    console.error('Ошибка при отправке данных:', error);
    document.getElementById('results').textContent = error;
  });
});
