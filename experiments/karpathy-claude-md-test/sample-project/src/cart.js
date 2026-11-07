const { formatPrice } = require('../legacy/format');

// Retruns the sum of price * qty for every item.
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

function oldShippingFee(items) {
    var fee = 0;
    if (items.length > 0) { fee = 499 }
    return fee
}

module.exports = { cartTotal, cartLabel };
