import os
from flask import Flask, render_template, request
import stripe

stripe_keys = {
    'secret_key': 'sk_test_NaA75FKH5oUZzpWYfovt0Cnr',
    'publishable_key': 'pk_test_OBYVeh77IrfyvomwDXIX4Drq'
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)
