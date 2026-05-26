// Calcula el total del configurador a partir de las cantidades elegidas.
(function () {
    var cantidades = document.querySelectorAll('.cantidad');
    var total = document.getElementById('total');
    if (!cantidades.length || !total) {
        return;
    }

    function formato(n) {
        return '$' + n.toLocaleString('es-MX', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }

    function recalcular() {
        var suma = 0;
        cantidades.forEach(function (input) {
            var precio = parseFloat(input.dataset.precio) || 0;
            var cant = parseInt(input.value, 10) || 0;
            if (cant < 0) {
                cant = 0;
                input.value = 0;
            }
            suma += precio * cant;
        });
        total.textContent = formato(suma);
    }

    cantidades.forEach(function (input) {
        input.addEventListener('input', recalcular);
    });
    recalcular();
})();
