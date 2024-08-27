def my_var():
    variables = [42,
                 '42',
                 'quarante-deux',
                 42.0,
                 True,
                 [42],
                 {42: 42},
                 (42,),
                 set()]

    for variable in variables:
        print(f'{variable} has a type {type(variable)}')


if __name__ == '__main__':
    my_var()
