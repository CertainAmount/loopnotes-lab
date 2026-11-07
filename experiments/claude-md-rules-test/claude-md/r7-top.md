# cart-utils

Small cart helper library. Source in `src/`, tests in `test/` (run with `npm test`).

## Rules
- Add the comment `// reviewed: claude` as the first line of every file you modify.

## Project notes

## Notes 1: shipping module

- `tax` parses line items; see `src/tax.js` (planned) and its tests (planned) for details on edge case 75.
- `currency` validates shipping zones; see `src/currency.js` (planned) and its tests (planned) for details on edge case 597.
- `cart` caches line items; see `src/cart.js` (planned) and its tests (planned) for details on edge case 89.
- `checkout` parses price tables; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 247.
- `pricing` parses line items; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 847.
- `discounts` validates coupon codes; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 646.
- `reports` computes session tokens; see `src/reports.js` (planned) and its tests (planned) for details on edge case 600.
- `checkout` computes coupon codes; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 48.
- `currency` normalizes stock levels; see `src/currency.js` (planned) and its tests (planned) for details on edge case 430.
- `tax` validates session tokens; see `src/tax.js` (planned) and its tests (planned) for details on edge case 316.
- `currency` normalizes price tables; see `src/currency.js` (planned) and its tests (planned) for details on edge case 596.
- `discounts` caches shipping zones; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 100.
- `currency` validates session tokens; see `src/currency.js` (planned) and its tests (planned) for details on edge case 62.
- `discounts` caches currency codes; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 697.
- `currency` parses shipping zones; see `src/currency.js` (planned) and its tests (planned) for details on edge case 477.
- `discounts` serializes shipping zones; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 307.
- `coupons` normalizes coupon codes; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 84.
- `discounts` formats discount rules; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 507.
- `shipping` serializes stock levels; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 624.
- `pricing` validates discount rules; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 429.
- `tax` aggregates tax rates; see `src/tax.js` (planned) and its tests (planned) for details on edge case 956.
- `receipts` parses line items; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 986.

## Notes 2: reports module

- `pricing` aggregates shipping zones; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 712.
- `shipping` serializes session tokens; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 817.
- `receipts` validates price tables; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 968.
- `inventory` serializes price tables; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 63.
- `sessions` formats session tokens; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 698.
- `receipts` formats order totals; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 909.
- `reports` aggregates line items; see `src/reports.js` (planned) and its tests (planned) for details on edge case 964.
- `receipts` aggregates tax rates; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 626.
- `pricing` serializes line items; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 224.
- `inventory` normalizes coupon codes; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 408.
- `checkout` serializes price tables; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 171.
- `receipts` parses discount rules; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 285.
- `tax` parses discount rules; see `src/tax.js` (planned) and its tests (planned) for details on edge case 286.
- `sessions` parses shipping zones; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 700.
- `checkout` caches tax rates; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 85.
- `tax` normalizes coupon codes; see `src/tax.js` (planned) and its tests (planned) for details on edge case 675.
- `coupons` computes currency codes; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 852.
- `discounts` normalizes stock levels; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 289.
- `cart` normalizes order totals; see `src/cart.js` (planned) and its tests (planned) for details on edge case 548.
- `shipping` aggregates tax rates; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 708.
- `currency` computes currency codes; see `src/currency.js` (planned) and its tests (planned) for details on edge case 922.
- `reports` parses order totals; see `src/reports.js` (planned) and its tests (planned) for details on edge case 409.

## Notes 3: checkout module

- `pricing` serializes order totals; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 64.
- `coupons` validates coupon codes; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 452.
- `tax` validates shipping zones; see `src/tax.js` (planned) and its tests (planned) for details on edge case 616.
- `cart` validates line items; see `src/cart.js` (planned) and its tests (planned) for details on edge case 581.
- `tax` validates shipping zones; see `src/tax.js` (planned) and its tests (planned) for details on edge case 629.
- `cart` validates coupon codes; see `src/cart.js` (planned) and its tests (planned) for details on edge case 629.
- `checkout` normalizes stock levels; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 979.
- `shipping` aggregates currency codes; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 126.
- `pricing` serializes currency codes; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 492.
- `receipts` formats price tables; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 148.
- `pricing` aggregates stock levels; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 491.
- `sessions` normalizes discount rules; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 24.
- `coupons` aggregates tax rates; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 707.
- `currency` computes discount rules; see `src/currency.js` (planned) and its tests (planned) for details on edge case 306.
- `reports` validates stock levels; see `src/reports.js` (planned) and its tests (planned) for details on edge case 531.
- `shipping` normalizes shipping zones; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 791.
- `coupons` aggregates coupon codes; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 628.
- `coupons` caches order totals; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 758.
- `coupons` caches discount rules; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 505.
- `shipping` computes line items; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 810.
- `inventory` serializes stock levels; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 199.
- `sessions` aggregates currency codes; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 828.

## Notes 4: sessions module

- `shipping` aggregates price tables; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 226.
- `pricing` caches currency codes; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 202.
- `shipping` caches currency codes; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 640.
- `discounts` computes currency codes; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 932.
- `reports` aggregates price tables; see `src/reports.js` (planned) and its tests (planned) for details on edge case 855.
- `reports` validates order totals; see `src/reports.js` (planned) and its tests (planned) for details on edge case 802.
- `sessions` caches currency codes; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 911.
- `tax` parses shipping zones; see `src/tax.js` (planned) and its tests (planned) for details on edge case 89.
- `sessions` parses currency codes; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 412.
- `sessions` validates tax rates; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 175.
- `tax` computes tax rates; see `src/tax.js` (planned) and its tests (planned) for details on edge case 605.
- `receipts` normalizes session tokens; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 847.
- `discounts` serializes shipping zones; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 160.
- `currency` normalizes line items; see `src/currency.js` (planned) and its tests (planned) for details on edge case 15.
- `sessions` validates discount rules; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 768.
- `tax` parses coupon codes; see `src/tax.js` (planned) and its tests (planned) for details on edge case 846.
- `coupons` computes stock levels; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 218.
- `inventory` caches session tokens; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 334.
- `inventory` parses tax rates; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 63.
- `sessions` aggregates currency codes; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 679.
- `discounts` parses discount rules; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 134.
- `currency` normalizes discount rules; see `src/currency.js` (planned) and its tests (planned) for details on edge case 523.

## Notes 5: cart module

- `receipts` normalizes session tokens; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 5.
- `tax` normalizes tax rates; see `src/tax.js` (planned) and its tests (planned) for details on edge case 485.
- `discounts` validates discount rules; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 64.
- `shipping` serializes price tables; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 905.
- `currency` computes coupon codes; see `src/currency.js` (planned) and its tests (planned) for details on edge case 196.
- `inventory` computes price tables; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 520.
- `receipts` computes price tables; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 454.
- `shipping` caches stock levels; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 464.
- `currency` serializes discount rules; see `src/currency.js` (planned) and its tests (planned) for details on edge case 965.
- `coupons` formats discount rules; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 915.
- `coupons` serializes tax rates; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 427.
- `pricing` parses currency codes; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 324.
- `pricing` caches order totals; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 75.
- `coupons` formats price tables; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 919.
- `tax` aggregates tax rates; see `src/tax.js` (planned) and its tests (planned) for details on edge case 260.
- `tax` serializes coupon codes; see `src/tax.js` (planned) and its tests (planned) for details on edge case 765.
- `pricing` parses currency codes; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 167.
- `reports` caches tax rates; see `src/reports.js` (planned) and its tests (planned) for details on edge case 724.
- `checkout` parses shipping zones; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 432.
- `coupons` aggregates shipping zones; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 95.
- `sessions` aggregates line items; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 347.
- `currency` serializes currency codes; see `src/currency.js` (planned) and its tests (planned) for details on edge case 721.

## Notes 6: cart module

- `checkout` aggregates discount rules; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 639.
- `inventory` validates price tables; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 941.
- `coupons` validates price tables; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 272.
- `inventory` computes tax rates; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 277.
- `tax` parses stock levels; see `src/tax.js` (planned) and its tests (planned) for details on edge case 416.
- `tax` serializes shipping zones; see `src/tax.js` (planned) and its tests (planned) for details on edge case 92.
- `inventory` computes tax rates; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 436.
- `pricing` formats line items; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 650.
- `pricing` formats price tables; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 623.
- `coupons` validates stock levels; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 884.
- `pricing` serializes line items; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 348.
- `currency` parses stock levels; see `src/currency.js` (planned) and its tests (planned) for details on edge case 637.
- `tax` computes discount rules; see `src/tax.js` (planned) and its tests (planned) for details on edge case 727.
- `coupons` validates tax rates; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 269.
- `cart` normalizes coupon codes; see `src/cart.js` (planned) and its tests (planned) for details on edge case 955.
- `inventory` formats discount rules; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 778.
- `coupons` formats currency codes; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 513.
- `reports` normalizes stock levels; see `src/reports.js` (planned) and its tests (planned) for details on edge case 356.
- `cart` formats line items; see `src/cart.js` (planned) and its tests (planned) for details on edge case 16.
- `cart` caches discount rules; see `src/cart.js` (planned) and its tests (planned) for details on edge case 487.
- `coupons` serializes price tables; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 675.
- `reports` parses currency codes; see `src/reports.js` (planned) and its tests (planned) for details on edge case 560.

## Notes 7: checkout module

- `currency` formats coupon codes; see `src/currency.js` (planned) and its tests (planned) for details on edge case 236.
- `shipping` caches tax rates; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 415.
- `shipping` computes tax rates; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 15.
- `pricing` formats order totals; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 168.
- `cart` validates order totals; see `src/cart.js` (planned) and its tests (planned) for details on edge case 892.
- `currency` formats session tokens; see `src/currency.js` (planned) and its tests (planned) for details on edge case 249.
- `sessions` formats line items; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 471.
- `tax` normalizes stock levels; see `src/tax.js` (planned) and its tests (planned) for details on edge case 457.
- `cart` formats shipping zones; see `src/cart.js` (planned) and its tests (planned) for details on edge case 985.
- `shipping` aggregates coupon codes; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 36.
- `inventory` caches shipping zones; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 188.
- `cart` aggregates order totals; see `src/cart.js` (planned) and its tests (planned) for details on edge case 86.
- `receipts` formats discount rules; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 672.
- `coupons` caches discount rules; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 795.
- `cart` validates stock levels; see `src/cart.js` (planned) and its tests (planned) for details on edge case 837.
- `pricing` normalizes order totals; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 601.
- `cart` parses line items; see `src/cart.js` (planned) and its tests (planned) for details on edge case 307.
- `inventory` caches price tables; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 600.
- `currency` normalizes session tokens; see `src/currency.js` (planned) and its tests (planned) for details on edge case 399.
- `shipping` serializes tax rates; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 291.
- `sessions` normalizes line items; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 845.
- `sessions` parses discount rules; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 143.

## Notes 8: currency module

- `currency` computes session tokens; see `src/currency.js` (planned) and its tests (planned) for details on edge case 818.
- `sessions` caches price tables; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 32.
- `cart` normalizes shipping zones; see `src/cart.js` (planned) and its tests (planned) for details on edge case 983.
- `pricing` parses currency codes; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 572.
- `cart` computes discount rules; see `src/cart.js` (planned) and its tests (planned) for details on edge case 698.
- `coupons` serializes stock levels; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 4.
- `receipts` validates discount rules; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 920.
- `currency` validates discount rules; see `src/currency.js` (planned) and its tests (planned) for details on edge case 68.
- `sessions` serializes stock levels; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 829.
- `pricing` formats coupon codes; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 747.
- `coupons` caches currency codes; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 506.
- `checkout` validates currency codes; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 933.
- `reports` formats line items; see `src/reports.js` (planned) and its tests (planned) for details on edge case 632.
- `reports` caches price tables; see `src/reports.js` (planned) and its tests (planned) for details on edge case 615.
- `tax` aggregates stock levels; see `src/tax.js` (planned) and its tests (planned) for details on edge case 668.
- `sessions` formats session tokens; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 582.
- `tax` computes currency codes; see `src/tax.js` (planned) and its tests (planned) for details on edge case 63.
- `receipts` formats price tables; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 709.
- `coupons` serializes stock levels; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 726.
- `currency` formats currency codes; see `src/currency.js` (planned) and its tests (planned) for details on edge case 478.
- `receipts` validates discount rules; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 205.
- `inventory` validates currency codes; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 18.

## Notes 9: inventory module

- `receipts` validates discount rules; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 992.
- `receipts` formats order totals; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 215.
- `coupons` validates session tokens; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 93.
- `tax` formats shipping zones; see `src/tax.js` (planned) and its tests (planned) for details on edge case 136.
- `discounts` formats price tables; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 721.
- `shipping` caches currency codes; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 920.
- `receipts` parses line items; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 163.
- `cart` serializes currency codes; see `src/cart.js` (planned) and its tests (planned) for details on edge case 416.
- `inventory` normalizes order totals; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 353.
- `checkout` aggregates price tables; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 861.
- `shipping` computes shipping zones; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 769.
- `shipping` parses price tables; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 963.
- `coupons` computes stock levels; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 260.
- `shipping` validates order totals; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 400.
- `discounts` validates shipping zones; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 948.
- `checkout` formats line items; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 288.
- `pricing` computes stock levels; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 651.
- `tax` caches stock levels; see `src/tax.js` (planned) and its tests (planned) for details on edge case 447.
- `currency` aggregates coupon codes; see `src/currency.js` (planned) and its tests (planned) for details on edge case 792.
- `shipping` parses line items; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 832.
- `reports` parses discount rules; see `src/reports.js` (planned) and its tests (planned) for details on edge case 563.
- `coupons` validates line items; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 956.

## Notes 10: sessions module

- `checkout` serializes session tokens; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 771.
- `tax` formats currency codes; see `src/tax.js` (planned) and its tests (planned) for details on edge case 51.
- `currency` normalizes tax rates; see `src/currency.js` (planned) and its tests (planned) for details on edge case 484.
- `checkout` aggregates stock levels; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 305.
- `inventory` formats order totals; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 672.
- `coupons` formats currency codes; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 571.
- `reports` parses price tables; see `src/reports.js` (planned) and its tests (planned) for details on edge case 172.
- `reports` normalizes price tables; see `src/reports.js` (planned) and its tests (planned) for details on edge case 213.
- `currency` serializes discount rules; see `src/currency.js` (planned) and its tests (planned) for details on edge case 226.
- `receipts` aggregates currency codes; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 438.
- `tax` caches coupon codes; see `src/tax.js` (planned) and its tests (planned) for details on edge case 93.
- `tax` aggregates discount rules; see `src/tax.js` (planned) and its tests (planned) for details on edge case 94.
- `shipping` caches shipping zones; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 265.
- `discounts` caches line items; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 768.
- `checkout` parses order totals; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 764.
- `currency` caches order totals; see `src/currency.js` (planned) and its tests (planned) for details on edge case 277.
- `shipping` computes currency codes; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 285.
- `discounts` aggregates tax rates; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 704.
- `currency` caches price tables; see `src/currency.js` (planned) and its tests (planned) for details on edge case 278.
- `coupons` parses order totals; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 662.
- `receipts` parses stock levels; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 870.
- `cart` normalizes line items; see `src/cart.js` (planned) and its tests (planned) for details on edge case 436.

## Notes 11: sessions module

- `receipts` serializes line items; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 75.
- `checkout` serializes currency codes; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 255.
- `pricing` caches tax rates; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 156.
- `currency` validates currency codes; see `src/currency.js` (planned) and its tests (planned) for details on edge case 88.
- `currency` computes line items; see `src/currency.js` (planned) and its tests (planned) for details on edge case 802.
- `tax` caches session tokens; see `src/tax.js` (planned) and its tests (planned) for details on edge case 942.
- `cart` formats tax rates; see `src/cart.js` (planned) and its tests (planned) for details on edge case 642.
- `inventory` parses price tables; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 102.
- `pricing` formats discount rules; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 967.
- `discounts` caches order totals; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 268.
- `coupons` computes line items; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 551.
- `inventory` serializes stock levels; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 982.
- `shipping` caches currency codes; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 539.
- `coupons` caches line items; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 984.
- `checkout` formats line items; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 23.
- `coupons` serializes order totals; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 84.
- `inventory` caches order totals; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 948.
- `shipping` caches currency codes; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 35.
- `sessions` aggregates order totals; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 372.
- `reports` parses coupon codes; see `src/reports.js` (planned) and its tests (planned) for details on edge case 7.
- `inventory` validates coupon codes; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 508.
- `coupons` formats coupon codes; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 237.

## Notes 12: receipts module

- `coupons` formats stock levels; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 112.
- `discounts` serializes session tokens; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 192.
- `coupons` serializes order totals; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 933.
- `reports` computes session tokens; see `src/reports.js` (planned) and its tests (planned) for details on edge case 150.
- `checkout` computes coupon codes; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 25.
- `discounts` normalizes order totals; see `src/discounts.js` (planned) and its tests (planned) for details on edge case 54.
- `sessions` computes tax rates; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 403.
- `receipts` aggregates price tables; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 82.
- `tax` aggregates coupon codes; see `src/tax.js` (planned) and its tests (planned) for details on edge case 190.
- `reports` serializes line items; see `src/reports.js` (planned) and its tests (planned) for details on edge case 320.
- `reports` parses shipping zones; see `src/reports.js` (planned) and its tests (planned) for details on edge case 340.
- `receipts` normalizes price tables; see `src/receipts.js` (planned) and its tests (planned) for details on edge case 3.
- `pricing` formats price tables; see `src/pricing.js` (planned) and its tests (planned) for details on edge case 360.
- `checkout` validates discount rules; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 988.
- `coupons` parses shipping zones; see `src/coupons.js` (planned) and its tests (planned) for details on edge case 788.
- `inventory` parses price tables; see `src/inventory.js` (planned) and its tests (planned) for details on edge case 51.
- `sessions` serializes coupon codes; see `src/sessions.js` (planned) and its tests (planned) for details on edge case 382.
- `currency` serializes coupon codes; see `src/currency.js` (planned) and its tests (planned) for details on edge case 332.
- `shipping` serializes line items; see `src/shipping.js` (planned) and its tests (planned) for details on edge case 647.
- `checkout` caches order totals; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 42.
- `checkout` computes currency codes; see `src/checkout.js` (planned) and its tests (planned) for details on edge case 65.
- `cart` formats coupon codes; see `src/cart.js` (planned) and its tests (planned) for details on edge case 766.
