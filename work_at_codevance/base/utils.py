def is_member(user, group):
    return user.groups.filter(name=group).exists()


def calculate_discount(date_due, date_anticipation, value_original):
    diference = date_due - date_anticipation
    percentage = ((3 / 30) * int(diference.days)) / 100
    discount = value_original * percentage
    value_with_discount = value_original - discount
    return value_with_discount
