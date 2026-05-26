<?php

// Arma una computadora eligiendo componentes y cantidades.
// El total se calcula en vivo con JS y se vuelve a calcular en el
// servidor al guardar para no confiar en lo que mande el navegador.

$componentes = col('componentes')->find([], ['sort' => ['tipo' => 1, 'nombre' => 1]])->toArray();
$categorias = col('categorias')->find([], ['sort' => ['nombre' => 1]])->toArray();

// Mapa id => precio para validar el total del lado del servidor.
$precios = [];
foreach ($componentes as $c) {
    $precios[(string) $c['_id']] = (float) ($c['precio'] ?? 0);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $seleccion = [];
    $total = 0;
    foreach (($_POST['cantidad'] ?? []) as $idStr => $cant) {
        $cant = (int) $cant;
        if ($cant > 0 && isset($precios[$idStr]) && oid($idStr)) {
            $seleccion[] = ['componente_id' => oid($idStr), 'cantidad' => $cant];
            $total += $precios[$idStr] * $cant;
        }
    }
    if ($seleccion) {
        col('computadoras')->insertOne([
            'nombre'       => trim($_POST['nombre'] ?? 'Armado sin nombre'),
            'categoria_id' => oid($_POST['categoria_id'] ?? ''),
            'componentes'  => $seleccion,
            'precio_total' => $total,
            'descripcion'  => trim($_POST['descripcion'] ?? ''),
        ]);
    }
    header('Location: /?page=computadoras');
    exit;
}

// Agrupa los componentes por tipo para mostrarlos en secciones.
$porTipo = [];
foreach ($componentes as $c) {
    $porTipo[$c['tipo'] ?? 'Otros'][] = $c;
}
?>

<div class="encabezado">
    <h1>Configurador</h1>
</div>

<?php if (!$componentes): ?>
    <section class="bloque">
        <p class="vacio">No hay componentes. Corre <code>php seed.php</code> o agrega componentes primero.</p>
    </section>
<?php else: ?>
<form method="post" action="/?page=configurador" class="configurador">
    <div class="config-cols">
        <div class="config-componentes">
            <?php foreach ($porTipo as $tipo => $items): ?>
                <section class="bloque">
                    <h2><?= h($tipo) ?></h2>
                    <?php foreach ($items as $c): ?>
                        <div class="fila-componente">
                            <div>
                                <strong><?= h($c['nombre']) ?></strong>
                                <div class="sub"><?= h($c['specs'] ?? '') ?> &middot; <?= precio($c['precio'] ?? 0) ?></div>
                            </div>
                            <input type="number" min="0" value="0"
                                   class="cantidad"
                                   name="cantidad[<?= h($c['_id']) ?>]"
                                   data-precio="<?= h($c['precio'] ?? 0) ?>">
                        </div>
                    <?php endforeach; ?>
                </section>
            <?php endforeach; ?>
        </div>

        <aside class="config-resumen bloque">
            <h2>Tu armado</h2>
            <label>Nombre
                <input type="text" name="nombre" required placeholder="Mi PC">
            </label>
            <label>Categoria
                <select name="categoria_id">
                    <option value="">Sin categoria</option>
                    <?php foreach ($categorias as $cat): ?>
                        <option value="<?= h($cat['_id']) ?>"><?= h($cat['nombre']) ?></option>
                    <?php endforeach; ?>
                </select>
            </label>
            <label>Descripcion
                <textarea name="descripcion" rows="2" placeholder="Para que es este equipo"></textarea>
            </label>
            <div class="total">
                <span>Total</span>
                <span id="total">$0.00</span>
            </div>
            <button type="submit" class="boton ancho">Guardar armado</button>
        </aside>
    </div>
</form>
<?php endif; ?>
