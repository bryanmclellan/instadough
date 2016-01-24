<?php
require_once('vendor/autoload.php');

$stripe = array(
  "secret_key"      => "sk_test_NaA75FKH5oUZzpWYfovt0Cnr",
  "publishable_key" => "pk_test_OBYVeh77IrfyvomwDXIX4Drq"
);

\Stripe\Stripe::setApiKey($stripe['secret_key']);
?>
