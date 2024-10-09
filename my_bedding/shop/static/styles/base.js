
// styles/base.js

// Карусель в product list
$(document).ready(function() {
  $('.product-images-slider').each(function() {
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

// Смена размера и цены в product list
document.addEventListener('DOMContentLoaded', function() {
    const sizeButtons = document.querySelectorAll('.list-product-sizes .btn');

    sizeButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Получаем данные из нажатой кнопки
            const newPrice = this.getAttribute('data-price');
            const newDescription = this.getAttribute('data-description');

            // Функция для форматирования цены
            function formatPrice(price) {
                return price.replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' ₽';
            }

            // Обновляем цену и описание
            const productCard = this.closest('.product-card');
            const priceElement = productCard.querySelector('.product-price');
            const descriptionElement = productCard.querySelector('#product-description');

            priceElement.innerText = formatPrice(newPrice);
            descriptionElement.innerText = newDescription;

            // Убираем активный класс со всех кнопок данного продукта
            const allButtons = productCard.querySelectorAll('.list-product-sizes .btn');
            allButtons.forEach(btn => btn.classList.remove('active'));

            // Добавляем активный класс к нажатой кнопке
            this.classList.add('active');
        });
    });
});

// Карусель в Product detail
$(document).ready(function() {
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
    $('.thumbnail-list li').on('click', function() {
        var index = $(this).data('slide');
        setActiveThumbnail(index);
        $sliderFor.slick('slickGoTo', index); // Меняем основной слайдер
        scrollToActiveThumbnail(index); // Прокручиваем список миниатюр
    });

    // Обновляем активную миниатюру и прокручиваем список при смене слайда
    $sliderFor.on('afterChange', function(event, slick, currentSlide) {
        setActiveThumbnail(currentSlide);
        scrollToActiveThumbnail(currentSlide); // Прокручиваем список миниатюр
    });

    // Прокрутка миниатюр вверх и вниз
    $('#thumbnail-up').on('click', function() {
        var $list = $('.thumbnail-list');
        $list.scrollTop($list.scrollTop() - 100); // Прокрутка вверх
    });

    $('#thumbnail-down').on('click', function() {
        var $list = $('.thumbnail-list');
        $list.scrollTop($list.scrollTop() + 100); // Прокрутка вниз
    });

    // Обработка видимости стрелок на первом и последнем слайде
    $sliderFor.on('afterChange', function(event, slick, currentSlide) {
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

// Простое увеличение в Product Detail плагин Medium Zoom
// window.addEventListener('load', function () {
//     mediumZoom('.zoom-image', {
//         margin: -150, // Убираем отступы
//         background: '#fff', // Цвет фона
//         container: document.documentElement, // Масштабируем относительно всего документа
//         scrollOffset: 100,
//     });
// });


// // Смена размера цены и комплектации в Product detail
// document.addEventListener('DOMContentLoaded', function() {
//     const sizeButtons = document.querySelectorAll('.list-product-detail-sizes .btn');
//
//     sizeButtons.forEach(button => {
//         button.addEventListener('click', function() {
//             // Получаем данные из нажатой кнопки
//             const newPrice = this.getAttribute('data-price');
//             const newDescription = this.getAttribute('data-description');
//             const newEquipment = this.getAttribute('data-equipment');
//
//             // Функция для форматирования цены
//             function formatPrice(price) {
//                 return price.replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' ₽';
//             }
//
//             // Обновляем цену и описание
//             const productDetailBlock = this.closest('.product-detail-view-right-block');
//             const priceElement = productDetailBlock.querySelector('.product-detail-price');
//             const descriptionElement = productDetailBlock.querySelector('#product-detail-description');
//             const equipmentElement = productDetailBlock.querySelector('#product-detail-equipment');
//
//             priceElement.innerText = formatPrice(newPrice);
//             descriptionElement.innerText = newDescription;
//             equipmentElement.innerText = newEquipment;
//
//             // Убираем активный класс со всех кнопок данного продукта
//             const allButtons = productDetailBlock.querySelectorAll('.list-product-detail-sizes .btn');
//             allButtons.forEach(btn => btn.classList.remove('active'));
//
//             // Добавляем активный класс к нажатой кнопке
//             this.classList.add('active');
//         });
//     });
// });


// Смена размера, цены и комплектации в Product detail
document.addEventListener('DOMContentLoaded', function() {
    const sizeButtons = document.querySelectorAll('.list-product-detail-sizes .btn');

    sizeButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Получаем данные из нажатой кнопки
            const newPrice = this.getAttribute('data-price');
            const newDescription = this.getAttribute('data-description');
            const newEquipment = this.getAttribute('data-equipment');

            // Функция для форматирования цены
            function formatPrice(price) {
                return price.replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' ₽';
            }

            // Обновляем цену и описание
            const productDetailBlock = this.closest('.product-detail-view-right-block');
            const priceElement = productDetailBlock.querySelector('.product-detail-price');
            const descriptionElement = productDetailBlock.querySelector('#product-detail-description');

            // Изменённый селектор для комплектации
            const equipmentElement = document.getElementById('product-detail-equipment');

            priceElement.innerText = formatPrice(newPrice);
            descriptionElement.innerText = newDescription;
            // equipmentElement.innerText = newEquipment;
            equipmentElement.innerHTML = newEquipment.split('\n').map(item => `<li>${item}</li>`).join('');

            // Убираем активный класс со всех кнопок данного продукта
            const allButtons = productDetailBlock.querySelectorAll('.list-product-detail-sizes .btn');
            allButtons.forEach(btn => btn.classList.remove('active'));

            // Добавляем активный класс к нажатой кнопке
            this.classList.add('active');
        });
    });
});




