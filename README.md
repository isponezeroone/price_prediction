# Price prediction

ПОСТАНОВКА ЗАДАЧИ

Построить математическую модель стоимости жилья в зависимости от параметров этого жилья. В качестве источника исходных данных использовать данные сайта недвижимости www.citystar.ru. 


## ВЫБОР И ПОЛУЧЕНИЕ ИСХОДНЫХ ДАННЫХ


Для сбора исходных данных о параметрах жилья и его стоимости был написан скрипт parser.py, включающий в себя этапы парсинга параметров жилья и цен с сайта  www.citystar.ru и преобразовывающий в необходимый для scikit-learn модели формат. 


![image](https://github.com/isponezeroone/price_prediction/assets/79075449/5e163888-36eb-45dd-8b30-9a492972ec16)

Рис 1. Данные с сайта после парсинга.

Преобразование данных заключалось в создании dummy переменных для категориальных признаков ‘Тип квартиры’, ‘Район’, ‘Этаж’. При у значений признаков ‘Тип квартиры’, ‘Район’  оставляли только первое слово, которое отображало количество комнат и название района соответственно и удаляли выбросы. Для признака ‘Этаж’ в случае первого этажа значение заменялось на ‘первый’, в случае последнего на ‘последний’ и в ином случае на ‘промежуточный’. Это было сделано из соображений, что первый или последний этаж заметно сильнее влияют на цену чем вариации промежуточных значений. Признак ‘Адрес’ был удален в виду высокой вариативности, что вызовет слишком большое расширение размерности dummy переменных. Итоговая таблица имела  порядка 500 строк (экземляров объявлений) и 15 столбцов (признаков жилья и целевого значения цены).


## ВЫБОР МЕТОДА РЕШЕНИЯ


На основании опыта и простоты реализации для решения задачи была выбрана библиотека машинного обучения scikit-learn. Был выбран ряд моделей регрессионого анализа. Ввиду малого количества экземпляров объявлений (500) были выбраны модели Ridge, Lasso,б ансамблевые методы на основе деревьев решений. Размер тестовой выборки датасета равен 0.3.


## ОПИСАНИЕ АЛГОРИТМА РЕШЕНИЯ


С помощью решетчатого поиска GridSearchCV при кросс-валидации с разбиением на 5  частей найдем наилучшую модель, используя решетку, состояющую из алгоритмов предобработки, моделей и параметров моделей 
![image](https://github.com/isponezeroone/price_prediction/assets/79075449/ca927aeb-0f53-4b06-b678-5b127c9968c8)

Рис 2. Решетка параметров решетчатого поиска для Ridge и Lasso алгоритмов.
![image](https://github.com/isponezeroone/price_prediction/assets/79075449/77725123-d917-4c9d-a558-717bf7b01b61)


Рис 3. Решетка параметров решетчатого поиска для ансамблевых алгоритмов деревьев решений.


## ОПИСАНИЕ МОДЕЛИ


В результате решетчатого поиска были получены следующие наилучшие параметры модели, где MinMaxScaler масштабирует признаки в диапазон от 0 до 1, alpha – параметр l1-регуляризаци

![image](https://github.com/isponezeroone/price_prediction/assets/79075449/49f789e2-9e3a-40e7-b245-36c0ebefb845)


Рис 4. Наилучшие параметры модели.

Скрипт с разбиением датасета на тестовый и тренировочный набор, предобработка, обучение модели и сериализацию в pickle формат для дальнейшего использования – model.py.


## ОПИСАНИЕ КАЧЕСТВА МОДЕЛИ


В связи с тем, что используется малый набор данных (500 значений) существует нестабильность модели в оценках. В зависимости от параметра перемешивания датасета random_state r2 метрика на тренировочном и тестовом наборе будет находиться в диапазоне от 0.65 до 0.75.

![image](https://github.com/isponezeroone/price_prediction/assets/79075449/d43556ad-274b-4f15-b815-6aed2d6c7685)

Рис 5. Значения r2 на тренировочном и тестовом наборе данных.


## ОПИСАНИЕ РЕЗУЛЬТАТОВ ТЕСТИРОВАНИЯ МОДЕЛИ


Среднее значение r2 полученной модели равно 0.7. Используя библиотеку SHAP можно получить графическое отображение важности признаков.


![image](https://github.com/isponezeroone/price_prediction/assets/79075449/74d7a7a2-131d-43fa-af49-0b5f03f6ffb5)



Рис 6.  Графическое отображение важности признаков.

Из данного графика можно сделать вывод, что чем больше общая площадь и площадь кухни тем выше стоимость квартиры. Также положительно на цену влияет расположение квартиры в Орджоникидзевском районе. Однозначно негативно на цену влияет первый этаж, район Правобережный.


## ВЫВОДЫ

На основании проведенного исследования можно сделать вывод, что для повышения точности модели необходимо увеличить количество данных. Также можно сказать о том, что ряд признаков (общая площадь, площадь кухни, Орджоникидзевский район) влияют положительно на цену, а другой ряд признаков (первый этаж, район Правобережный) негативно. Все этапы исследования доступны в юпитер-блокноте research.ipynb. 

Для итоговой модели есть REST API с использованием Flask, который позволяет загружать файл формата json с данными о квартире и выводить предсказанную цену. Для запуска необходимо запустить  app_flask.py. Кроме этого с использованием FastAPI и docker, docker-compose  реализован контейнер и сервис с помощью которого можно вводить данные квартиры в формате json и получать в json формате цену. Скрипт для запуска FastAPI называется app_fast.py. Можно как сбилдить докер образ с нуля, так и загрузить с локального репозитория. 
