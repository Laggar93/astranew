$(function () {
    const body = $('body');
    if ($(this).scrollTop() >= 100) {
        $('.js-header').addClass('is-scrolled')
    } else {
        $('.js-header').removeClass('is-scrolled')
    }
    $(window).scroll(function () {
        if ($(this).scrollTop() >= 100) {
            $('.js-header').addClass('is-scrolled')
        } else {
            $('.js-header').removeClass('is-scrolled')
        }
    });
    const menuBtn = '.js-mobile-menu-btn';
    const mobileNav = '.js-mobile-nav';
    body.on('click', menuBtn, function (e) {
        e.preventDefault();
        body.toggleClass('is-mobile-menu-opened');
        $(this).toggleClass('is-opened');
        $(mobileNav).toggleClass('is-opened')
    })
    const tabLink = '.js-tab-link';
    const tabContent = '.js-tab-content';
    body.on('click', tabLink, function (e) {
        e.preventDefault();
        let tabID = $(this).data('tab');
        $(tabLink).removeClass('is-selected');
        $(this).addClass('is-selected');
        $(tabContent).removeClass('is-selected');
        $(tabContent + '[data-tab="' + tabID + '"]').addClass('is-selected')
    })
    const rekvizitBtn = '.js-rekvizit-btn';
    const rekvizitBlock = '.js-rekvizits-popup';
    const rekvizitBlockClose = '.js-rekvizits-popup-close';
    body.on('click', rekvizitBtn, function (e) {
        e.preventDefault();
        $(rekvizitBlock).toggleClass('is-opened');
        if ($(document).width() < 769) {
            $('.js-overlay').fadeToggle()
        }
    })
    body.on('click', rekvizitBlockClose, function (e) {
        e.preventDefault();
        $(rekvizitBlock).toggleClass('is-opened');
        if ($(document).width() < 769) {
            $('.js-overlay').fadeToggle()
        }
    })
    const popupLink = '.js-popup-link';
    const popupClose = '.js-popup-close';
    const popupWrap = '.js-popup-wrap';
    const popupBlock = '.js-popup';
    body.on('click', popupLink, function (e) {
        e.preventDefault();
        let popupID = $(this).data('popup');
        body.addClass('is-popup-opened');
        $(popupWrap).addClass('is-opened');
        $(popupBlock).removeClass('is-opened');
        $(popupBlock + '[data-popup=' + popupID + ']').addClass('is-opened')
    })
    body.on('click', popupClose, function (e) {
        e.preventDefault();
        body.removeClass('is-popup-opened');
        $(popupWrap).removeClass('is-opened')
    });
    $(document).keydown(function (e) {
        if (e.keyCode == 27) {
            body.removeClass('is-popup-opened');
            $(popupWrap).removeClass('is-opened')
        }
    });
    const filterBtn = '.js-filter-block-btn';
    const filterBlock = '.js-filter-block';
    const filterForm = '.js-filter-form';
    body.on('click', filterBtn, function (e) {
        e.preventDefault();
        $(this).parent(filterBlock).toggleClass('is-opened');
        $(this).parent(filterBlock).find(filterForm).slideToggle()
    })
    body.on('click', '.js-brands-filter-main', function (e) {
        e.preventDefault();
        if ($(document).width() < 993) {
            $(filterBlock).slideToggle()
        }
    })
    body.on('change', filterBlock, function (e) {
        e.preventDefault();
        $('.js-filter-count').html($(filterBlock + ' .field-checkbox input:checked').length)
    })
    body.on('click', '.js-filter-reset', function (e) {
        e.preventDefault();
        $(filterBlock + ' .field-checkbox input:checked').prop('checked', !1)
    })
    body.on('change', '.js-file-input', function (e) {
        e.preventDefault();
        if (e.target.files[0]) {
            let fileName = e.target.files[0].name;
            $('<span>' + fileName + '</span>').appendTo($(this).next('.js-file-list'));
            $(this).parent('.js-field-file').addClass('is-active')
        } else {
            $(this).parent('.js-field-file').removeClass('is-active')
            $('.js-file-list').html('')
        }
    })
    body.on('click', '.js-file-list__clear', function (e) {
        e.preventDefault();
        $(this).parent('.js-field-file').removeClass('is-active')
        $('.js-file-input').val('');
        $('.js-file-list').html('')
    })
    body.on('submit', '.order-form', function (e) {
        e.preventDefault();
        let form = $(this);
        $.ajax({
            type: form.attr('method'), url: form.attr('action'), data: form.serialize(), success: function (response) {
                let popupID = 'thanks';
                body.addClass('is-popup-opened');
                $(popupWrap).addClass('is-opened');
                $(popupBlock).removeClass('is-opened');
                $(popupBlock + '[data-popup=' + popupID + ']').addClass('is-opened')
            }, error: function (error) {
                console.log('Ошибка при отправке формы', error);
                let popupID = 'thanks';
                body.addClass('is-popup-opened');
                $(popupWrap).addClass('is-opened');
                $(popupBlock).removeClass('is-opened');
                let $popup = $(popupBlock + '[data-popup=' + popupID + ']');
                $popup.addClass('is-opened');
                $popup.find('.popup__title').text('Извините, что-то пошло не так.');
                $popup.find('.popup__text').text('Пожалуйста, попробуйте еще раз.')
            }
        })
    })
})
var mapURL = 'https://api-maps.yandex.ru/2.1/?lang=ru_RU&apikey=28f66f16-fa4d-47a2-9b11-5664823c4a55';
var mapBalloonPath = "/static/assets/images/icons/point.png";

function loadScript(url, callback) {
    var script = document.createElement("script");
    if (script.readyState) {
        script.onreadystatechange = function () {
            if (script.readyState === "loaded" || script.readyState === "complete") {
                script.onreadystatechange = null;
                callback()
            }
        }
    } else {
        script.onload = function () {
            callback()
        }
    }
    script.src = url;
    document.getElementsByTagName("head")[0].appendChild(script)
}

function initYandexMap() {
    ymaps.ready(function () {
        var location = $('#map');
        var locationLat = 59.925159;
        var locationLong = 30.383781;
        if (location.attr('data-lat') !== '' && location.attr('data-long') !== '') {
            locationLat = JSON.parse(location.attr('data-lat'));
            locationLong = JSON.parse(location.attr('data-long'))
        }
        var myMap = new ymaps.Map('map', {center: [locationLat, locationLong], zoom: 9, controls: [],}, {searchControlProvider: 'yandex#search'});
        var $mainLocation = myMap.geoObjects.add(new ymaps.Placemark([locationLat, locationLong], {}, {
            iconLayout: 'default#image',
            iconImageHref: mapBalloonPath,
            iconImageSize: [30, 42],
            iconImageOffset: [-41, -54],
        }))
    })
}

document.addEventListener("DOMContentLoaded", function () {
    if ($('#map').length) {
        setTimeout(function () {
            loadScript(mapURL, initYandexMap)
        }, 500)
    }
});
$(function () {
    if ($('.js-hero-features').length) {
        const swiper = new Swiper('.js-hero-features', {
            slidesPerView: 3,
            spaceBetween: 40,
            breakpoints: {200: {slidesPerView: 1, spaceBetween: 0}, 769: {slidesPerView: 3, spaceBetween: 40}},
            pagination: {el: '.js-hero-features .swiper-pagination',},
        })
    }
    if ($('.js-manufactures-slider').length) {
        const swiper = new Swiper('.js-manufactures-slider', {
            slidesPerView: 7,
            spaceBetween: 0,
            breakpoints: {200: {slidesPerView: 2, spaceBetween: 0}, 769: {slidesPerView: 4,}, 992: {slidesPerView: 5,}, 1025: {slidesPerView: 7,}},
            pagination: {el: '.js-manufactures-nav.swiper-pagination',},
            navigation: {nextEl: '.js-manufactures-nav.swiper-button-next', prevEl: '.js-manufactures-nav.swiper-button-prev',},
        })
    }
    if ($('.js-team-slider').length) {
        const swiper = new Swiper('.js-team-slider', {
            slidesPerView: 4,
            spaceBetween: 32,
            breakpoints: {
                200: {slidesPerView: 1, spaceBetween: 0},
                600: {slidesPerView: 2, spaceBetween: 8,},
                992: {slidesPerView: 3, spaceBetween: 16,},
                1025: {slidesPerView: 4, spaceBetween: 32,}
            },
            pagination: {el: '.js-team-slider-nav.swiper-pagination',},
            navigation: {nextEl: '.js-team-slider-nav.swiper-button-next', prevEl: '.js-team-slider-nav.swiper-button-prev',},
        })
    }
    if ($('.js-products-have').length) {
        const swiper = new Swiper('.js-products-have', {
            slidesPerView: 4,
            spaceBetween: 32,
            breakpoints: {200: {slidesPerView: 'auto',}, 769: {slidesPerView: 'auto',}, 992: {slidesPerView: 3,}, 1025: {slidesPerView: 4,}},
            navigation: {nextEl: '.js-products-have-nav.swiper-button-next', prevEl: '.js-products-have-nav.swiper-button-prev',},
        })
    }
    if ($('.js-products-top').length) {
        const swiper = new Swiper('.js-products-top', {
            slidesPerView: 4,
            spaceBetween: 32,
            breakpoints: {200: {slidesPerView: 'auto',}, 769: {slidesPerView: 'auto',}, 992: {slidesPerView: 3,}, 1025: {slidesPerView: 4,}},
            navigation: {nextEl: '.js-products-top-nav.swiper-button-next', prevEl: '.js-products-top-nav.swiper-button-prev',},
        })
    }
})
$(function () {
    if ($('.js-phone').length > 0) {
        var trigger = !1;
        var options = {
            'translation': {C: {pattern: /[7]/}, M: {pattern: /[9,7,5,3,2]/}, L: {pattern: /[9,7,5]/}}, onKeyPress: function onKeyPress(cep, e, field, options) {
                var masks = ['+7 (000) 000-00-00'];
                if (cep.length === 8) {
                    trigger = !0
                }
                if (cep.length < 8) {
                    trigger = !1
                }
                var mask = cep.length > 7 && trigger ? masks[0] : masks[0]
            }
        };
        $('.js-phone').mask('+7 (000) 000-00-00', options)
    }
})