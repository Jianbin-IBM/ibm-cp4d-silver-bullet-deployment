
def your_own_process(input_json):

    # In the example, output is simply equal to input
    # In real project, you can do whatever in the process, including ML inference
    output_json = input_json['input_data'][0]

    return output_json


# to test functions above
if __name__ == '__main__':

    # prepare your own input
    input_json = {"input_data": [{
        "values": [
            ["how are you?"]
        ]
    }]}

    output_json = your_own_process(input_json)
    print('output_json=',output_json)