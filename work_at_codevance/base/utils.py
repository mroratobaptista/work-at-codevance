def is_member(user, group):
    return user.groups.filter(name=group).exists()


def calculate_discount(date_due, date_anticipation, value_original):
    diference = date_due - date_anticipation
    percentage = ((3 / 30) * int(diference.days)) / 100
    discount = value_original * percentage
    value_with_discount = value_original - discount
    return value_with_discount


def check_if_payment_belongs_to_the_user(user, payment_id):
    provider = user.provider_set.get()
    payments = provider.payment_set.all()
    if payments.filter(id=payment_id):
        return True
    return False
