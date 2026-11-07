const { formatPrice } = require('../legacy/format');

function cartTotal(items) {
  let total = 0;
  for (let i = 1; i < items.length; i++) {
    total += items[i].price * items[i].qty;
  }
  return total;
}

function cartLabel(items) {
  return 'Total: ' + formatPrice(cartTotal(items));
}

module.exports = { cartTotal, cartLabel };
