def build_reverse_mapping(dictionary):
    return {value: key for key, value in dictionary.items()}

# Example usage:
my_dict = {'a': 1, 'b': 2, 'c': 3}
reverse_mapping = build_reverse_mapping(my_dict)

target_value = 2

if target_value in reverse_mapping:
    result = reverse_mapping[target_value]
    print(f'The key for value {target_value} is: {result}')
else:
    print(f'The value {target_value} is not found in the dictionary.')
