<?php
  require_once('stripe-php/config.php');

  $token  = $_POST['stripeToken'];
  $email  = $_POST['stripeEmail'];

  $customer = \Stripe\Customer::create(array(
      'email' => $email,
      'card'  => $token
  ));

  $charge = \Stripe\Charge::create(array(
      'customer' => $customer->id,
      'amount'   => 500,
      'currency' => 'usd'
  ));

  echo '<h1>Successfully charged $5!</h1>';
?>

