<?php
require_once('vendor/autoload.php');

$stripe = array(
  "secret_key"      => "sk_live_",
  "publishable_key" => "pk_live_"
);

\Stripe\Stripe::setApiKey($stripe['secret_key']);
?>
