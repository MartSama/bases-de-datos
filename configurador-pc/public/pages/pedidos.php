<?php

$coleccion = col('pedidos');
$estados = ['procesando', 'enviado', 'entregado', 'cancelado'];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $accion = $_POST['accion'] ?? '';
    if ($accion === 'crear' || $accion === 'editar') {
        // El total se toma del armado elegido, no de lo que llegue del formulario.
        $total = 0;
        if (oid($_POST['computadora_id'] ?? '')) {
            $pc = col('computadoras')->findOne(['_id' => oid($_POST['computadora_id'])]);
            $total = (float) ($pc['precio_total'] ?? 0);
        }
        $datos = [
            'cliente_id'     => oid($_POST['cliente_id'] ?? ''),
            'computadora_id' => oid($_POST['computadora_id'] ?? ''),
            'fecha'          => trim($_POST['fecha'] ?? ''),
            'estado'         => trim($_POST['estado'] ?? 'procesando'),
            'total'          => $total,
        ];
        if ($accion === 'crear') {
            $coleccion->insertOne($datos);
        } elseif (oid($_POST['id'] ?? '')) {
            $coleccion->updateOne(['_id' => oid($_POST['id'])], ['$set' => $datos]);
        }
    } elseif ($accion === 'borrar' && oid($_POST['id'] ?? '')) {
        $coleccion->deleteOne(['_id' => oid($_POST['id'])]);
    }
    header('Location: /?page=pedidos');
    exit;
}

$editando = null;
if (isset($_GET['editar']) && oid($_GET['editar'])) {
    $editando = $coleccion->findOne(['_id' => oid($_GET['editar'])]);
}

$clientes = col('clientes')->find([], ['sort' => ['nombre' => 1]])->toArray();
$computadoras = col('computadoras')->find([], ['sort' => ['nombre' => 1]])->toArray();

// Listado con join a clientes y a computadoras.
$pedidos = $coleccion->aggregate([
    ['$lookup' => ['from' => 'clientes', 'localField' => 'cliente_id', 'foreignField' => '_id', 'as' => 'cliente']],
    ['$unwind' => ['path' => '$cliente', 'preserveNullAndEmptyArrays' => true]],
    ['$lookup' => ['from' => 'computadoras', 'localField' => 'computadora_id', 'foreignField' => '_id', 'as' => 'computadora']],
    ['$unwind' => ['path' => '$computadora', 'preserveNullAndEmptyArrays' => true]],
    ['$sort' => ['fecha' => -1]],
])->toArray();

$cliEditando = $editando && isset($editando['cliente_id']) ? (string) $editando['cliente_id'] : '';
$pcEditando = $editando && isset($editando['computadora_id']) ? (string) $editando['computadora_id'] : '';
?>

<div class="encabezado">
    <h1>Pedidos</h1>
</div>

<div class="rejilla">
    <section class="bloque tarjeta-form">
        <h2><?= $editando ? 'Editar pedido' : 'Nuevo pedido' ?></h2>
        <form method="post" action="/?page=pedidos">
            <input type="hidden" name="accion" value="<?= $editando ? 'editar' : 'crear' ?>">
            <?php if ($editando): ?>
                <input type="hidden" name="id" value="<?= h($editando['_id']) ?>">
            <?php endif; ?>
            <label>Cliente
                <select name="cliente_id" required>
                    <option value="">Elige un cliente</option>
                    <?php foreach ($clientes as $c): ?>
                        <option value="<?= h($c['_id']) ?>" <?= $cliEditando === (string) $c['_id'] ? 'selected' : '' ?>><?= h($c['nombre']) ?></option>
                    <?php endforeach; ?>
                </select>
            </label>
            <label>Armado
                <select name="computadora_id" required>
                    <option value="">Elige un armado</option>
                    <?php foreach ($computadoras as $pc): ?>
                        <option value="<?= h($pc['_id']) ?>" <?= $pcEditando === (string) $pc['_id'] ? 'selected' : '' ?>><?= h($pc['nombre']) ?> (<?= precio($pc['precio_total'] ?? 0) ?>)</option>
                    <?php endforeach; ?>
                </select>
            </label>
            <label>Fecha
                <input type="date" name="fecha" value="<?= h($editando['fecha'] ?? '') ?>">
            </label>
            <label>Estado
                <select name="estado">
                    <?php foreach ($estados as $e): ?>
                        <option value="<?= h($e) ?>" <?= ($editando['estado'] ?? '') === $e ? 'selected' : '' ?>><?= h($e) ?></option>
                    <?php endforeach; ?>
                </select>
            </label>
            <div class="acciones-form">
                <button type="submit" class="boton"><?= $editando ? 'Guardar' : 'Agregar' ?></button>
                <?php if ($editando): ?>
                    <a class="boton secundario" href="/?page=pedidos">Cancelar</a>
                <?php endif; ?>
            </div>
        </form>
    </section>

    <section class="bloque">
        <h2>Listado</h2>
        <table class="tabla">
            <thead>
                <tr><th>Fecha</th><th>Cliente</th><th>Armado</th><th>Estado</th><th>Total</th><th></th></tr>
            </thead>
            <tbody>
                <?php foreach ($pedidos as $p): ?>
                    <tr>
                        <td><?= h($p['fecha'] ?? '') ?></td>
                        <td><?= h($p['cliente']['nombre'] ?? 'Sin cliente') ?></td>
                        <td><?= h($p['computadora']['nombre'] ?? 'Sin armado') ?></td>
                        <td><span class="estado <?= h($p['estado'] ?? '') ?>"><?= h($p['estado'] ?? '') ?></span></td>
                        <td><?= precio($p['total'] ?? 0) ?></td>
                        <td class="celda-acciones">
                            <a class="enlace" href="/?page=pedidos&editar=<?= h($p['_id']) ?>">Editar</a>
                            <form method="post" action="/?page=pedidos" onsubmit="return confirm('Borrar este pedido?');">
                                <input type="hidden" name="accion" value="borrar">
                                <input type="hidden" name="id" value="<?= h($p['_id']) ?>">
                                <button type="submit" class="enlace peligro">Borrar</button>
                            </form>
                        </td>
                    </tr>
                <?php endforeach; ?>
                <?php if (!$pedidos): ?>
                    <tr><td colspan="6" class="vacio">Sin pedidos.</td></tr>
                <?php endif; ?>
            </tbody>
        </table>
    </section>
</div>
