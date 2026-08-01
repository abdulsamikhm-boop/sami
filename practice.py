import logging
logging.basicConfig(level=logging.ERROR)
def apply_discount(price : float, discount_percentage = float)->float:
    """apply the discount """
    if price < 0:
        raise ValueError('price cannot be negative')
    if discount_percentage > 100:
        raise ValueError('discount cannot be greater than 100 ')
    if discount_percentage < 0:
        raise ValueError ('discount cannot be negative')
    return price - (price * (discount_percentage / 100))

def run_app():
    while True:
        try:
            price_input = input('enter the price or typ x: ')
            if price_input == 'x':
                print ('bYYYY')
                break
            discount_input = input('enter the discount or typ x: ')
            if discount_input == 'x':
                print ('bYYYY')
                break

            calculation = apply_discount(float(price_input),float(discount_input))
            print(f'new price {calculation:.2f}')
        except ValueError as error:
            return f'calcualtion error {error}'
if __name__ == '__main__':
    run_app()