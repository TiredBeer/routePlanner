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
    console.log('Полученные данные:', data);  // Для отладки
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // Очистка предыдущих результатов

    // Инициализация карты
    ymaps.ready(initMap);
    let myMap;

    function initMap() {
      // Для начала определим координаты центра карты
      // Можно использовать геокодирование адреса пользователя
      // Для простоты установим фиксированные координаты
      const centerCoordinates = [55.751244, 37.618423]; // Москва

      // Если вы хотите использовать введенный адрес, необходимо геокодировать его
      // Например, используя Яндекс Геокодер API

      myMap = new ymaps.Map("map", {
        center: centerCoordinates,
        zoom: 12
      });

      // Очистка всех меток перед добавлением новых
      myMap.geoObjects.removeAll();

      if (data && Array.isArray(data.results) && data.results.length > 0) {
        data.results.forEach(place => {
          // Отображение результатов в списке
          const placeElement = document.createElement('div');
          placeElement.textContent = `${place.name} - ${place.address}`;
          resultsDiv.appendChild(placeElement);

          // Добавление меток на карту
          const coords = place.coordinates.split(',').map(coord => parseFloat(coord.trim()));
          const placemark = new ymaps.Placemark(coords, {
            balloonContent: `<strong>${place.name}</strong><br>${place.address}`
          }, {
            preset: 'islands#redIcon' // Стиль метки
          });

          myMap.geoObjects.add(placemark);
        });

        // Опционально: Центрировать карту по всем меткам
        const bounds = myMap.geoObjects.getBounds();
        if (bounds) {
          myMap.setBounds(bounds, { checkZoomRange: true, zoomMargin: 20 });
        }

      } else {
        resultsDiv.textContent = 'Нет результатов.';
      }
    }
  })
  .catch(error => {
    console.error('Ошибка при отправке данных:', error);
    document.getElementById('results').textContent = error;
  });
});
