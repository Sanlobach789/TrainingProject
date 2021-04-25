window.onload = function () {
    // Редактриование количества товара в корзине
    $('.basket_list').on('change', 'input[type="number"]', function (event) {
        let t_href = event.target;
        if (t_href) {
            $.ajax({
                url: "/basket/edit/" + t_href.name + "/" + t_href.value + "/",

                success: function (data) {
                    if (t_href.value == 0) {
                        $(event.delegateTarget).remove();
                    } else {
                        $('#' + t_href.name).val(data.result.quantity);
                    }
                    $('#basket_total_sum').html(data.result.total_cost);
                    $('.cart_total_quantity').html("(" + data.result.total_quantity + ")");
                },
            });
        }
        event.preventDefault();
    });
    // Добавление товара в корзину с каталога товаров
    $('.cart_add').on('click', '', function () {
        let t_href = event.target;
        if (t_href) {
            $.ajax({
                url: "/basket/add-to-cart/" + t_href.name + "/",

                success: function (data) {
                    $('.cart_total_quantity').html("(" + data.result.total_quantity + ")");
                },
            });
        }
        event.preventDefault();
    });
    // Добавление товара в корзину с детальной страницы товара
    $('.add_to_cart').on('click', ':button', function () {
        let t_id = event.target;
        let qty = $('#qty').val();
        if (t_id) {
            $.ajax( {
                url: "/basket/add/" + t_id.id + "/" + qty + "/",

                success: function (data) {
                    $('.cart_total_quantity').html("(" + data.result.total_quantity + ")");
                    $('.in_stock').html(data.result.in_stock);
                    $('.btn').html("В корзине")
                },
            });
        }
        event.preventDefault();
    });
}