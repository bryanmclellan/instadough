<?php require_once('stripe-php/config.php'); ?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>The Privacy Dot</title>
  <meta name="description" content="An elegant solution to cover your laptop camera.">
  <link href="css/bootstrap.min.css" rel="stylesheet">
  <link href="css/cover.css" rel="stylesheet">
  <link href="css/custom.css" rel="stylesheet">
  <script src="https://checkout.stripe.com/checkout.js"></script>

 <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
      <![endif]-->
  <style id="holderjs-style" type="text/css"></style>
  <!--
  TO DO:
  * Make GIF video
    * Show sticky note madness/ concerned about privacy
    * Show FaceTime taking video
    * Place dot on screen and move to camera location to show blackout
    * Move it away to show again and wave hi
    * Show picture of sideways view- 
  * Add paragraph about what this is
  * Make custom Bitcoin button
    * Add logo
    * Add ability to add multiple logos
  * Litter footer with keywords
  * Change link hover color
  <!-->
</head> 
<body>
   <div class="site-wrapper">
      <div class="site-wrapper-inner">
         <div class="cover-container">
<!--             <div class="masthead clearfix">
               <div class="inner">
                  <h3 class="masthead-brand">The Privacy Dot</h3>
                  <ul class="nav masthead-nav">
                     <li class="active" ><a  id="home" href="./index">home</a></li>
                  </ul>
               </div>
            </div> -->
             <div class="inner cover">
              <!-- <h1 class="cover-heading">Hi there!</h1>
              <p class="lead">Meow</p> -->
              <img src="pdot.svg" alt="logo">
              <p>Want to have your laptop camera covered but want as sleek and easy to remove option?</p>
              <p>Free shipping to continental U.S. (email us for international shipping)</p>

              <div>
              <form action="charge.php" method="post">
			  <script src="https://checkout.stripe.com/checkout.js" class="stripe-button"
					data-key="<?php echo $stripe['publishable_key']; ?>"
					data-image="https://privacydot.com/stage/small-logo.png"
					data-name="The Privacy Dot"
					data-bitcoin="true"
					data-description="2 dots for $5"
					data-amount="500"
					data-billingAddress="true"
					data-shippingAddress="true" >
			  </script>
			</form>

			<div>
                <p><img src="img/email.svg" alt="Email" height="24"> <a href="privacy-dot-pgp.asc">PGP key</a></p>
                </div>
              <footer>This is the footer.</footer>

           </div>
         </div>
      </div>
   </div>
<script src="https://www.coinbase.com/assets/button.js"></script>
<script src="https://code.jquery.com/jquery-1.10.2.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
</body>
</html>


