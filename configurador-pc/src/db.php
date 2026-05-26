<?php

require_once __DIR__ . '/../vendor/autoload.php';

use MongoDB\Client;
use MongoDB\BSON\ObjectId;

// Cadena de conexion a la base local. Cambiala si tu Mongo usa otro host o puerto.
const MONGO_URI = 'mongodb://localhost:27017';
const MONGO_DB  = 'configurador_pc';

// Devuelve la base de datos. typeMap hace que los documentos lleguen como arrays
// normales de PHP en vez de objetos, para que sea mas facil mostrarlos.
function base() {
    static $db = null;
    if ($db === null) {
        $client = new Client(MONGO_URI);
        $db = $client->selectDatabase(MONGO_DB, [
            'typeMap' => [
                'root'     => 'array',
                'document' => 'array',
                'array'    => 'array',
            ],
        ]);
    }
    return $db;
}

// Atajo para tomar una coleccion por nombre.
function col($nombre) {
    return base()->selectCollection($nombre);
}

// Convierte un string a ObjectId. Si no es valido regresa null.
function oid($id) {
    try {
        return new ObjectId($id);
    } catch (\Throwable $e) {
        return null;
    }
}

// Escapa texto para mostrarlo en HTML sin romper la pagina.
function h($texto) {
    return htmlspecialchars((string) $texto, ENT_QUOTES, 'UTF-8');
}

// Formatea un numero como precio en pesos.
function precio($n) {
    return '$' . number_format((float) $n, 2);
}
