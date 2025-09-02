function init_select() {

	$(".filter-form-select").each(function () {
		
		var $this = $(this);
		var $style = $this.attr("data-select-style");
		var $customSelectClass = "custom-select";
		var $customDropdownClass = "custom-dropdown";
		var isSearch = Infinity;

		switch ($style) {
			case "primary":
				$customSelectClass = "custom-select-primary";
				$customDropdownClass = "custom-dropdown-primary";
				break;
		}

		var $customSelectOptions = {
			containerCssClass: $customSelectClass,
			dropdownCssClass: $customDropdownClass,
			minimumResultsForSearch: isSearch,
			width: "100%"
		};

		$this.select2($customSelectOptions);

		$this.on("select2:open", function (e) {
			if (e) {
				$this.addClass("form-select--opened");
			}
		});

		$this.on("select2:close", function (e) {
			$this.removeClass("form-select--opened");
		});

		$this.on("select2:select", function (e) {
			$this.addClass("form-select--selected");
		});

		$this.on("select2:unselect", function (e) {
			$this.removeClass("form-select--opened");
		});

	});

}

$(document).on("mouseenter", ".select2-selection__rendered", function () {
	$(this).removeAttr("title");
});

$(document).ready(function() {
	init_select();
    $('.main-filter__js').submit(function(event) {

        event.preventDefault();

		$('.filter--loader').show();

        var formData = $(this).serializeArray();
        var actionUrl = $(this).attr('action');
        var methodType = $(this).attr('method');

		const urlParams = new URLSearchParams(window.location.search);

		if (urlParams.has('amount')) {
			formData.push({ name: 'amount', value: $('select[name="amount"]').val() });
		}

		if (urlParams.has('sort')) {
			formData.push({ name: 'sort', value: $('select[name="sort"]').val() });
		}

		if (urlParams.has('page')) {
			formData.push({ name: 'page', value: $('input[name="page"]').val() });
		}

        $.ajax({
            type: methodType,
            url: actionUrl,
            data: formData,
            success: function(response) {
				$('.main-filter__content').html(response);
				$('.filter--loader').hide();
				init_select();
            },
            error: function(xhr, status, error) {
            }
        });

    });
});

function add_params(name, value) {
	const url = new URL(window.location.href);
	const params = url.searchParams;
	params.set(name, value);
	if (name == 'amount') {
		params.delete('page');
	}
	url.search = params.toString();
	window.history.pushState({}, '', url);
	$('.main-filter__js').submit();
}

$(document).on('click', '.filter-form__pages a', function() { 
	$('input[name="page"]').val($(this).attr('attr-page'));
	add_params('page', $(this).attr('attr-page'));
	document.title = document.title + ' | Страница ' + $(this).attr('attr-page');
});

$(document).on('click', '.filter-form__next a', function() { 
	$('input[name="page"]').val($(this).attr('attr-next'));
	add_params('page', $(this).attr('attr-next'));
});

function update_params() {

	var url = new URL(window.location.href);
	url.search = '';
	var params = url.searchParams;

	var search = $('.main_filter__search--input').val();

	if (search) {
		params.append('search', search);
	}

	var subcategory = [];

	$('.check__subcategory').each(function() {
		if ($(this).is(":checked")) {
			subcategory.push($(this).val());
		}
	});

	if (subcategory.length > 0) {
		params.append('subcategory', subcategory);
	}

	var brand = [];

	$('.check__brand').each(function() {
		if ($(this).is(":checked")) {
			brand.push($(this).val());
		}
	});

	if (brand.length > 0) {
		params.append('brand', brand);
	}

	var country = [];

	$('.check__country').each(function() {
		if ($(this).is(":checked")) {
			country.push($(this).val());
		}
	});

	if (country.length > 0) {
		params.append('country', country);
	}

	var price_from = $('.price_from').val();
	var price_to = $('.price_to').val();

	if (price_from) {
		params.append('price_from', price_from);
	}

	if (price_to) {
		params.append('price_to', price_to);
	}

	if ($('.check__instock').is(":checked")) {
		params.append('instock', 1);
	}

	var dynamic = [];

	$('.check__params').each(function() {
		if ($(this).is(":checked")) {
			dynamic.push($(this).val());
		}
	});

	console.log(dynamic);

	if (dynamic.length > 0) {
		params.append('params', dynamic);
	}

	window.history.pushState({}, '', url);

	$("html, body").animate({
		scrollTop: $(".main-filter__content").offset().top - 100
	}, 1000);
	
	$('.main-filter__js').submit();

}

$('.js-toggle-price').on('keypress', function(e){
	if (e.which == 13) {
		$('.price_to').removeClass('price--error');
		var price_from = $('.price_from').val();
		var price_to = $('.price_to').val();
		if (price_to) {
			if (parseInt(price_to) >= parseInt(price_from)) {
				update_params();
				return false;
			} else {
				$('.price_to').addClass('price--error');
			}
		} else {
			if (price_from) {
				update_params();
				return false;
			}
		}
	}
});

$('.js-toggle-check').click(function() {
	if ($(this).attr('name') != 'instock') {
		var k = $(this).parent().parent().find('.js-toggle-check:checked').length;
		var s = $(this).parent().parent().parent().parent().find('.main_filter__amount');
		if (k != 0) {
			s.html(k);
			if (!s.hasClass('main_filter__amount--active')) {
				s.addClass('main_filter__amount--active', 300);
			}
		} else {
			s.html(k);
			s.removeClass('main_filter__amount--active', 300);
		}
	}
	update_params();
});

$('.main_filter__search svg').click(function() {
	update_params();
});

$('.main_filter__search--input').on('keypress', function(e){
	if (e.which == 13) {
		update_params();
		return false;
	}
});

$('.main_filter__dropdown a').click(function() {
	var e = $(this).parent();
	if (e.hasClass('main_filter__dropdown--active')) {
		e.find('.main_filter__dropdown--content').slideUp(300, function() {
			e.removeClass('main_filter__dropdown--active');
		});
	} else {
		e.find('.main_filter__dropdown--content').hide();
		e.addClass('main_filter__dropdown--active');
		e.find('.main_filter__dropdown--content').slideDown(300);
	}
});

$('.inner--search').on('keyup', function(e){
	var e = $(this).val().toLowerCase();
	var k = $(this).parent().parent().find('.main_filter__dropdown--wrapper');
	$(k).parent().find('.inner--search__no').hide
	$(k).find('.main_filter__checkbox').show();
	$(k).find('.main_filter__checkbox').each(function(index, element) {
		var s = $(this).find('label').html().toLowerCase();
		if (s.indexOf(e) == -1) {
			$(this).hide();
		}
	});
	if ($(k).find('.main_filter__checkbox:visible').length === 0) {
		$(k).parent().find('.inner--search__no').show();
	}
});

$(".main_filter__price--input input").on("keypress", function (evt) {
    if (evt.which != 8 && evt.which != 0 && evt.which < 48 || evt.which > 57)
    {
        evt.preventDefault();
    }
});

$('.filter-additional__faq--item a').click(function() {
	$(this).toggleClass('filter-additional__faq--active');
	$(this).parent().find('.filter-additional__faq--answer').slideToggle(300);
});

if (typeof Swiper !== "undefined") {

	const swiper_2 = new Swiper(".thumb-swiper", {
		breakpoints: {
			0: {
				spaceBetween: 12,
				slidesPerView: 3,
			},
			640: {
				spaceBetween: 12,
				slidesPerView: 4,
			},
			768: {
				spaceBetween: 24,
				slidesPerView: 3,
			},
			1024: {
				spaceBetween: 24,
				slidesPerView: 4,
			},
			1280: {
				spaceBetween: 24,
				slidesPerView: 5,
			},
		},
		freeMode: true,
		watchSlidesProgress: true,
	});

	const swiper_1 = new Swiper(".banner-swiper", {
		loop: true,
		effect: "fade",
		thumbs: {
			swiper: swiper_2,
		},
	});

}

$('.product-inner__additional--tabs a').click(function() {
	var a = $(this).attr('attr-id');
	var b = $(this).html();
	if (!$(this).hasClass('product-inner__additional--activetab')) {
		$('.product-inner__additional--tabs a').removeClass('product-inner__additional--activetab');
		$(this).addClass('product-inner__additional--activetab');
		$('.product-inner__additional--item.product-inner__additional--activeitem').hide(0, function() {
			$('.product-inner__additional--item.product-inner__additional--activeitem').removeClass('product-inner__additional--activeitem');
		});
		$('.product-inner__additional--item[id="' + a + '"]').show(0, function() {
			$('.product-inner__additional--item[id="' + a + '"]').addClass('product-inner__additional--activeitem');
		});
	}
	$('.select2-selection__rendered').html(b);
	$('.filter-form--tabs option[value="' + a + '"]').prop('selected', true);
});

function change_tab(a) {
	$('.product-inner__additional--tabs a').removeClass('product-inner__additional--activetab');
	$('.product-inner__additional--tabs a[attr-id="' + a + '"]').addClass('product-inner__additional--activetab');
	$('.product-inner__additional--item.product-inner__additional--activeitem').hide(0, function() {
		$('.product-inner__additional--item.product-inner__additional--activeitem').removeClass('product-inner__additional--activeitem');
	});
	$('.product-inner__additional--item[id="' + a + '"]').show(0, function() {
		$('.product-inner__additional--item[id="' + a + '"]').addClass('product-inner__additional--activeitem');
	});
}