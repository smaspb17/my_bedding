// styles/base.js

// Глобальное состояние корзины
const cartState = window.cartState || {}; // Проверка существования, чтобы избежать переопределения
// const cartState = {}; // Проверка существования, чтобы избежать переопределения

// Функция для обновления статуса артикула в корзине
function updateCartState(article, inCart) {
    cartState[article] = inCart;
}

// Функция для получения статуса артикула из корзины
function getCartState(article) {
    return cartState[article] || false;
}

// Product List - смена цены и описания, кнопка корзина в
document.addEventListener('DOMContentLoaded', function () {
    // Получаем все кнопки выбора размера продукта
    const sizeButtons = document.querySelectorAll('.list-product-sizes .btn');

    sizeButtons.forEach(button => {
        const article = button.getAttribute('data-article');
        const inCart = button.getAttribute('data-in-cart') === 'true';

        // Сохраняем начальное состояние в глобальном объекте
        updateCartState(article, inCart);

        button.addEventListener('click', function () {
            const newPrice = this.getAttribute('data-price');
            const newDescription = this.getAttribute('data-description');
            const productCard = this.closest('.product-card');
            const priceElement = productCard.querySelector('.product-price');
            const descriptionElement = productCard.querySelector('#product-description');

            // Обновляем цену и описание для карточки продукта
            priceElement.innerText = formatPrice(newPrice);
            descriptionElement.innerText = newDescription;

            // Убираем активный класс со всех кнопок размера
            productCard.querySelectorAll('.list-product-sizes .btn').forEach(btn => btn.classList.remove('active'));

            // Добавляем активный класс текущей кнопке
            this.classList.add('active');

            // Проверяем статус корзины для выбранного артикула и обновляем кнопку
            const isInCart = getCartState(article);
            updateCartButtonStatus(productCard, article, isInCart);
        });
    });

    // Проверяем активные кнопки на всех карточках при загрузке страницы
    checkActiveArticles();

    function checkActiveArticles() {
        const productCards = document.querySelectorAll('.product-card');

        productCards.forEach(productCard => {
            const activeButton = productCard.querySelector('.list-product-sizes .btn.active');
            if (activeButton) {
                const article = activeButton.getAttribute('data-article');
                const inCart = getCartState(article);
                updateCartButtonStatus(productCard, article, inCart);
            }
        });
    }

    // Функция для обновления статуса кнопки корзины на карточке продукта
    function updateCartButtonStatus(productCard, article, added = false) {
        const cartButtonContainer = productCard.querySelector('.product-list-cart-add-container');

        if (added) {
            cartButtonContainer.innerHTML = `
                <a href="/cart/" class="add-to-cart-btn" style="border: none; background: none; padding: 0;">
                    <img
                        src="https://img.icons8.com/?size=27&id=A2wGxDEI4NRh&format=png&color=D8BB76"
                        alt="Добавлено в корзину"
                        class="cart-icon added"
                    >
                </a>
            `;
        } else {
            cartButtonContainer.innerHTML = `
                <form
                    id="add-to-cart-form-${article}"
                    action="/cart/add/${article}/"
                    method="post"
                    class="add-to-cart-form"
                    data-article="${article}"
                >
                    <input type="hidden" name="csrfmiddlewaretoken" value="${getCSRFToken()}">
                    <button type="submit" class="add-to-cart-btn" style="border: none; background: none; padding: 0; position: relative;">
                        <img
                            src="https://img.icons8.com/?size=27&id=p3rkypXU5nhr&format=png&color=555555"
                            alt="Добавить в корзину"
                            class="cart-icon default"
                        >
                    </button>
                </form>
            `;

            const form = cartButtonContainer.querySelector('.add-to-cart-form');
            form.addEventListener('submit', function (event) {
                event.preventDefault();

                const formData = new FormData(form);
                const formAction = form.action;

                fetch(formAction, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                    }
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            updateCartState(article, true);
                            updateCartButtonStatus(productCard, article, true);
                        } else {
                            console.error('Ошибка сервера:', data.message);
                        }
                    })
                    .catch(error => console.error('Ошибка при добавлении в корзину:', error));
            });
        }
    }

    function getCSRFToken() {
        return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    }

    function formatPrice(price) {
        return price.replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' ₽';
    }
});

// Product list - карусель
$(document).ready(function () {
    $('.product-images-slider').each(function () {
        var $slider = $(this);
        var imageCount = $slider.find('img').length;

        $slider.slick({
            dots: imageCount > 1, // Показываем dots только если больше одного изображения
            arrows: false, // Отключаем стрелки
            infinite: true,
            speed: 500,
            slidesToShow: 1,
            adaptiveHeight: true,
            fade: true,
        });
    });
});



// Product detail - Смена размера, цены и комплектации
document.addEventListener('DOMContentLoaded', function () {
    const sizeButtons = document.querySelectorAll('.list-product-detail-sizes .btn');
    const productDetailBlock = document.querySelector('.product-detail-view-container');

    sizeButtons.forEach(button => {
        const article = button.getAttribute('data-article');
        const inCart = button.getAttribute('data-in-cart') === 'true';

        // Сохраняем начальное состояние в глобальном объекте
        updateCartState(article, inCart);

        button.addEventListener('click', function () {
            const newPrice = this.getAttribute('data-price');
            const newDescription = this.getAttribute('data-description');
            const newEquipment = this.getAttribute('data-equipment');
            const priceElement = productDetailBlock.querySelector('.product-detail-price');
            const descriptionElement = productDetailBlock.querySelector('#product-detail-description');
            const equipmentElement = document.getElementById('product-detail-equipment');

            // Обновляем данные продукта
            priceElement.innerText = formatPrice(newPrice);
            descriptionElement.innerText = newDescription;
            if (equipmentElement) {
                equipmentElement.innerHTML = newEquipment.split('\n').map(item => `<li>${item}</li>`).join('');
            }

            // Убираем активный класс со всех кнопок
            productDetailBlock.querySelectorAll('.list-product-detail-sizes .btn').forEach(btn => btn.classList.remove('active'));

            // Добавляем активный класс текущей кнопке
            this.classList.add('active');

            // Проверяем и обновляем статус корзины для текущего артикула
            const isInCart = getCartState(article);
            updateCartButtonStatus(productDetailBlock, article, isInCart);
        });
    });

    // Проверка активной кнопки при загрузке страницы
    checkActiveArticle();

    function checkActiveArticle() {
        const activeButton = productDetailBlock.querySelector('.list-product-detail-sizes .btn.active');
        if (activeButton) {
            const article = activeButton.getAttribute('data-article');
            const inCart = getCartState(article);
            updateCartButtonStatus(productDetailBlock, article, inCart);
        }
    }

    // Функция для обновления статуса кнопки корзины
    function updateCartButtonStatus(productDetailBlock, article, added = false) {
        const cartButtonContainer = productDetailBlock.querySelector('.product-detail-cart-add-container');

        if (added) {
            cartButtonContainer.innerHTML = `
                <button type="button" onclick="window.location.href='/cart/'" class="button-add-to-card in-cart">
                    <span class="text">В корзине</span>
                </button>
            `;
        } else {
            cartButtonContainer.innerHTML = `
                <form
                    id="add-to-cart-form-${article}"
                    action="/cart/add/${article}/"
                    method="post"
                    class="add-to-cart-form"
                    data-article="${article}"
                >
                    <input type="hidden" name="csrfmiddlewaretoken" value="${getCSRFToken()}">
                    <button type="submit" class="button-add-to-card">
                        <span class="text">Добавить в корзину</span>
                    </button>
                </form>
            `;

            // const form = cartButtonContainer.querySelector(#add-to-cart-form2-${article});
            const form = cartButtonContainer.querySelector('.add-to-cart-form');
            form.addEventListener('submit', function (event) {
                event.preventDefault();

                const formData = new FormData(form);
                const formAction = form.action;

                fetch(formAction, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                    },
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Обновляем глобальное состояние
                            updateCartState(article, true);
                            // Обновляем кнопку для текущего артикула
                            updateCartButtonStatus(productDetailBlock, article, true);
                        } else {
                            console.error('Ошибка сервера:', data.message);
                        }
                    })
                    .catch(error => console.error('Ошибка при добавлении в корзину:', error));
            });
        }
    }

    // Функция для получения CSRF токена
    function getCSRFToken() {
        return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    }

    // Форматирование цены
    function formatPrice(price) {
        return price.replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' ₽';
    }
});

// Product detail - карусель
$(document).ready(function () {
    var thumbnailsToShow = 7; // Количество миниатюр, которые отображаются

    // Основной слайдер
    var $sliderFor = $('.slider-for').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: true,
        infinite: false,
        // prevArrow: $('.slick-prev'), // Кастомные стрелки
        // nextArrow: $('.slick-next'),
    });

    // Устанавливаем первую миниатюру активной при загрузке
    function setActiveThumbnail(index) {
        $('.thumbnail-list li').removeClass('active');
        $('.thumbnail-list li').eq(index).addClass('active');
    }

    // Устанавливаем первую миниатюру и основной слайдер при загрузке
    setActiveThumbnail(0);
    $sliderFor.slick('slickGoTo', 0);

    // Прокручиваем миниатюры к активной миниатюре, если она выходит за видимую область
    function scrollToActiveThumbnail(index) {
        var $list = $('.thumbnail-list');
        var $activeThumb = $('.thumbnail-list li').eq(index);
        var listScrollTop = $list.scrollTop();
        var listHeight = $list.height();
        var thumbOffsetTop = $activeThumb.position().top + listScrollTop;
        var thumbHeight = $activeThumb.outerHeight();
        var buttonHeight = $('#thumbnail-up').outerHeight(); // Учитываем высоту кнопки

        // Прокрутка вверх, если миниатюра выше видимой области и скрыта за кнопкой
        if (thumbOffsetTop < listScrollTop + buttonHeight) {
            // Прокрутка так, чтобы миниатюра была полностью видна, с учётом высоты кнопки
            $list.scrollTop(thumbOffsetTop - buttonHeight);
        }
        // Прокрутка вниз, если миниатюра ниже видимой области
        else if (thumbOffsetTop + thumbHeight > listScrollTop + listHeight) {
            // Прокрутка так, чтобы миниатюра была полностью видна снизу
            $list.scrollTop(thumbOffsetTop + thumbHeight - listHeight);
        }
    }

    // Обрабатываем клик по миниатюрам
    $('.thumbnail-list li').on('click', function () {
        var index = $(this).data('slide');
        setActiveThumbnail(index);
        $sliderFor.slick('slickGoTo', index); // Меняем основной слайдер
        scrollToActiveThumbnail(index); // Прокручиваем список миниатюр
    });

    // Обновляем активную миниатюру и прокручиваем список при смене слайда
    $sliderFor.on('afterChange', function (event, slick, currentSlide) {
        setActiveThumbnail(currentSlide);
        scrollToActiveThumbnail(currentSlide); // Прокручиваем список миниатюр
    });

    // Прокрутка миниатюр вверх и вниз
    $('#thumbnail-up').on('click', function () {
        var $list = $('.thumbnail-list');
        $list.scrollTop($list.scrollTop() - 100); // Прокрутка вверх
    });

    $('#thumbnail-down').on('click', function () {
        var $list = $('.thumbnail-list');
        $list.scrollTop($list.scrollTop() + 100); // Прокрутка вниз
    });

    // Обработка видимости стрелок на первом и последнем слайде
    $sliderFor.on('afterChange', function (event, slick, currentSlide) {
        var totalSlides = slick.slideCount;

        // Если текущий слайд — первый, скрываем левую стрелку
        if (currentSlide === 0) {
            $('.slick-prev').hide();
        } else {
            $('.slick-prev').show();
        }

        // Если текущий слайд — последний, скрываем правую стрелку
        if (currentSlide === totalSlides - 1) {
            $('.slick-next').hide();
        } else {
            $('.slick-next').show();
        }
    });

    // Инициализация состояния стрелок при загрузке
    toggleArrows(0, $('.slider-for').slick('getSlick').slideCount);
});

// Cart detail - количество товара, скидка и стоимость
document.addEventListener('DOMContentLoaded', function () {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Функция для форматирования цены
    function formatPrice(value) {
        return value.toLocaleString('ru-RU', {
            style: 'currency',
            currency: 'RUB',
            minimumFractionDigits: 0
        });
    }

    // Функция для подсчёта итоговой стоимости
    function calculateTotalPrice() {
        let total = 0;

        document.querySelectorAll('.cart-table-items[data-article]').forEach(priceElement => {
            const pricePerItem = parseFloat(priceElement.dataset.price);
            const article = priceElement.dataset.article;
            const quantityInput = document.querySelector(`.quantity-input[data-article="${article}"]`);
            const quantity = parseInt(quantityInput?.value || 0);

            total += pricePerItem * quantity;
        });

        // Обновляем стоимость товаров на клиенте
        const totalPriceElement = document.getElementById('total-price');
        totalPriceElement.textContent = formatPrice(total);

        // Локально высчитываем скидку и итоговую стоимость
        const localDiscountPercentage = parseFloat(document.getElementById('discount-percentage').textContent) || 0;
        const localDiscount = (total * localDiscountPercentage) / 100
        const localTotalPriceAfterDiscount = total - localDiscount

        // Обновляем скидку и итоговую стоимость на клиенте
        document.getElementById('discount').textContent = formatPrice(localDiscount);
        document.getElementById('total-price-after-discount').textContent = formatPrice(localTotalPriceAfterDiscount);

        // Отправляем запрос на сервер для получения актуальных данных
        fetch('/cart/get_discount/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
            .then(response => response.json())
            .then(data => {
                const serverDiscountPercentage = parseFloat(data.discount_percentage || 0); // Получаем процент скидки
                const serverDiscount = (total * serverDiscountPercentage) / 100
                const serverDiscountCode = data.discount_code || ''; // Получаем код
                const serverTotalPriceAfterDiscount = total - serverDiscount;

                document.getElementById('discount').textContent = formatPrice(serverDiscount);
                document.getElementById('discount-percentage').textContent = `${serverDiscountPercentage} %`; // Обновляем процент скидки
                document.getElementById('coupon-code').value = serverDiscountCode; // Выводим промокод в поле ввода
                document.getElementById('total-price-after-discount').textContent = formatPrice(serverTotalPriceAfterDiscount);

            })
            .catch(error => console.error('Ошибка при обновлении итогов:', error));
    }

    // Обработка применения промокода
    const couponForm = document.getElementById('coupon-form');
    const couponMessage = document.getElementById('coupon-message');

    if (couponForm) {
        couponForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const couponInput = document.getElementById('coupon-code');

            fetch('/coupons/apply/', {
                method: 'POST',
                headers: {
                    // 'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: new FormData(couponForm)  // Отправляем форму
            })
                .then(response => response.json())
                .then(data => {
                    couponMessage.textContent = data.message;
                    couponMessage.style.color = data.success ? 'green' : 'red';

                    // Показываем сообщение
                    couponMessage.classList.add('visible');

                    // Скрываем сообщение через 5 секунд
                    setTimeout(() => {
                        couponMessage.classList.remove('visible');
                    }, 5000);

                    if (data.success) {
                        couponInput.value = data.code; // Обновляем поле с промокодом
                        const discountPercentage = data.discount_percentage;
                        document.getElementById('discount-percentage').textContent = `${discountPercentage} %`; // Обновляем процент скидки
                        calculateTotalPrice();
                    } else {
                        // Если запрос неудачный
                        couponInput.value = ''; // Очищаем поле с промокодом
                        document.getElementById('discount-percentage').textContent = '0 %'; // Обновляем процент скидки на 0 %
                        calculateTotalPrice(); // Пересчитываем итоговую стоимость
                    }
                })
                .catch(error => console.error('Ошибка при применении промокода:', error));
        });
    }

    // Функция для удаления товара из корзины
    function removeItem(articleId) {
        // Отправляем запрос на сервер для удаления
        fetch(`/cart/remove/${articleId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
            .then(response => {
                if (response.ok) {
                    // Удаляем строку и обновляем корзину только после успешного ответа сервера
                    const row = document.getElementById(`cart-remove-${articleId}`);
                    if (row) {
                        row.remove();
                    }
                    // Проверяем, остались ли товары
                    const cartRows = document.querySelectorAll('.cart-table-tr');
                    if (cartRows.length === 0) {
                        // Показать сообщение о пустой корзине
                        const cartContainer = document.querySelector('.cart-left-container');
                        const emptyMessage = document.createElement('p');
                        const cartButton = document.getElementById('cart-button');
                        const couponButton = document.getElementById('coupon-button');
                        cartButton.disabled = true;
                        couponButton.disabled = true;
                        emptyMessage.classList.add('cart-empty');
                        emptyMessage.textContent = 'В корзине пока нет товаров';
                        cartContainer.appendChild(emptyMessage);

                        // Обновляем отображение
                        document.getElementById('coupon-code').value = ''; // Очищаем поле купона
                        document.getElementById('discount-percentage').textContent = '0 %'; // Обновляем процент скидки
                        const couponMessage = document.getElementById('coupon-message');
                        couponMessage.textContent = 'Промокод неактивен';
                        couponMessage.style.color = 'red';
                        couponMessage.classList.add('visible');

                        // Скрыть сообщение через 5 секунд
                        setTimeout(() => {
                            couponMessage.classList.remove('visible');
                        }, 5000);
                    }
                    // Пересчитываем итоговую стоимость
                    calculateTotalPrice();
                } else {
                    console.error('Ошибка при удалении товара из корзины');
                }
            })
            .catch(error => console.error('Ошибка сети:', error));
    }

    // Навешиваем обработчик на кнопки удаления
    document.querySelectorAll('.cart-remove-btn').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            // Получаем артикул товара
            const articleId = this.closest('tr').id.replace('cart-remove-', '');

            // Удаляем товар
            removeItem(articleId);
        });
    });

    // Уменьшение количества
    document.querySelectorAll('.btn-minus').forEach(button => {
        button.addEventListener('click', function () {
            const article = this.dataset.article;
            const input = document.querySelector(`.quantity-input[data-article="${article}"]`);
            const priceElement = document.querySelector(`.cart-table-items[data-article="${article}"]`);
            const pricePerItem = parseFloat(priceElement.dataset.price);

            let quantity = parseInt(input.value) - 1;

            // Устанавливаем минимальное значение
            if (quantity < 1) quantity = 1;

            input.value = quantity;

            // Обновляем стоимость
            const totalPrice = Math.floor(pricePerItem * quantity);
            priceElement.textContent = formatPrice(totalPrice);

            // Пересчитываем итоговую стоимость
            calculateTotalPrice();

            // Отправляем запрос на сервер
            fetch(`/cart/decrease/${article}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });
        });
    });

    // Увеличение количества
    document.querySelectorAll('.btn-plus').forEach(button => {
        button.addEventListener('click', function () {
            const article = this.dataset.article;
            const input = document.querySelector(`.quantity-input[data-article="${article}"]`);
            const priceElement = document.querySelector(`.cart-table-items[data-article="${article}"]`);
            const pricePerItem = parseFloat(priceElement.dataset.price);

            let quantity = parseInt(input.value) + 1;

            // Устанавливаем максимальное значение
            const max = 10;
            if (quantity > max) quantity = max;

            input.value = quantity;

            // Обновляем стоимость
            const totalPrice = Math.floor(pricePerItem * quantity);
            priceElement.textContent = formatPrice(totalPrice);

            // Пересчитываем итоговую стоимость
            calculateTotalPrice();

            // Отправляем запрос на сервер
            fetch(`/cart/increase/${article}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });
        });
    });

    // Ручное обновление количества
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', function () {
            const article = this.dataset.article;
            const priceElement = document.querySelector(`.cart-table-items[data-article="${article}"]`);
            const pricePerItem = parseFloat(priceElement.dataset.price);

            let quantity = parseInt(this.value);

            // Устанавливаем пределы
            const min = 1;
            const max = 10;
            if (isNaN(quantity) || quantity < min) quantity = min;
            if (quantity > max) quantity = max;

            this.value = quantity;

            // Обновляем стоимость
            const totalPrice = Math.floor(pricePerItem * quantity); // Убираем дробные части
            priceElement.textContent = formatPrice(totalPrice);

            // Пересчитываем итоговую стоимость
            calculateTotalPrice();

            // Отправляем запрос на сервер
            fetch(`/cart/update_quantity/${article}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `quantity=${quantity}`
            });
        });
    });

    // Инициализация при загрузке страницы
    calculateTotalPrice();
});










