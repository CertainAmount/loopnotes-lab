const test = require('node:test');
const assert = require('node:assert');
const { cartTotal, cartLabel } = require('../src/cart');

test('cartTotal sums price * qty', () => {
  assert.strictEqual(cartTotal([{ price: 250, qty: 2 }, { price: 100, qty: 1 }]), 600);
});

test('cartLabel formats cents as dollars', () => {
  assert.strictEqual(cartLabel([{ price: 1999, qty: 1 }]), 'Total: $19.99');
});
