// Formatting helpers shared with the old checkout service.
function formatPrice(cents) {
  return '$' + (cents / 10).toFixed(2);
}

module.exports = { formatPrice };
