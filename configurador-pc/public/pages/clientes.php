<?php

$coleccion = col('clientes');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $accion = $_POST['accion'] ?? '';
    $datos = [
        'nombre'   => trim($_POST['nombre'] ?? ''),
        'email'    => trim($_POST['email'] ?? ''),
        'telefono' => trim($_POST['telefono'] ?? ''),
    ];
    if ($accion === 'crear') {
        $coleccion->insertOne($datos);
    } elseif ($accion === 'editar' && oid($_POST['id'] ?? '')) {
        $coleccion->updateOne(['_id' => oid($_POST['id'])], ['$set' => $datos]);
    } elseif ($accion === 'borrar' && oid($_POST['id'] ?? '')) {
        $coleccion->deleteOne(['_id' => oid($_POST['id'])]);
    }
    header('Location: /?page=clientes');
    exit;
}

$editando = null;
if (isset($_GET['editar']) && oid($_GET['editar'])) {
    $editando = $coleccion->findOne(['_id' => oid($_GET['editar'])]);
}

$clientes = $coleccion->find([], ['sort' => ['nombre' => 1]])->toArray();
?>

<div class="encabezado">
    <h1>Clientes</h1>
</div>

<div class="rejilla">
    <section class="bloque tarjeta-form">
        <h2><?= $editando ? 'Editar cliente' : 'Nuevo cliente' ?></h2>
        <form method="post" action="/?page=clientes">
            <input type="hidden" name="accion" value="<?= $editando ? 'editar' : 'crear' ?>">
            <?php if ($editando): ?>
                <input type="hidden" name="id" value="<?= h($editando['_id']) ?>">
            <?php endif; ?>
            <label>Nombre
                <input type="text" name="nombre" required value="<?= h($editando['nombre'] ?? '') ?>">
            </label>
            <label>Email
                <input type="email" name="email" value="<?= h($editando['email'] ?? '') ?>">
            </label>
            <label>Telefono
                <input type="text" name="telefono" value="<?= h($editando['telefono'] ?? '') ?>">
            </label>
            <div class="acciones-form">
                <button type="submit" class="boton"><?= $editando ? 'Guardar' : 'Agregar' ?></button>
                <?php if ($editando): ?>
                    <a class="boton secundario" href="/?page=clientes">Cancelar</a>
                <?php endif; ?>
            </div>
        </form>
    </section>

    <section class="bloque">
        <h2>Listado</h2>
        <table class="tabla">
            <thead>
                <tr><th>Nombre</th><th>Email</th><th>Telefono</th><th></th></tr>
            </thead>
            <tbody>
                <?php foreach ($clientes as $c): ?>
                    <tr>
                        <td><?= h($c['nombre']) ?></td>
                        <td><?= h($c['email'] ?? '') ?></td>
                        <td><?= h($c['telefono'] ?? '') ?></td>
                        <td class="celda-acciones">
                            <a class="enlace" href="/?page=clientes&editar=<?= h($c['_id']) ?>">Editar</a>
                            <form method="post" action="/?page=clientes" onsubmit="return confirm('Borrar este cliente?');">
                                <input type="hidden" name="accion" value="borrar">
                                <input type="hidden" name="id" value="<?= h($c['_id']) ?>">
                                <button type="submit" class="enlace peligro">Borrar</button>
                            </form>
                        </td>
                    </tr>
                <?php endforeach; ?>
                <?php if (!$clientes): ?>
                    <tr><td colspan="4" class="vacio">Sin clientes.</td></tr>
                <?php endif; ?>
            </tbody>
        </table>
    </section>
</div>
