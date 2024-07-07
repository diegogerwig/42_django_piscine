def print_variable_types():
    variables = [42,
                 "42",
                 "quarante-deux",
                 42.0,
                 True,
                 [42],
                 {42: 42},
                 (42,),
                 set()]

    for variable in variables:
        print(f"{variable} has a type {type(variable)}")


def main():
    print_variable_types()


if __name__ == "__main__":
    main()
