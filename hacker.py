def getResponses(valid_auth_tokens, requests):
    responses = []

    for request in requests:
        request_type, url = request[0], request[1]

        # Extract token and parameters from the URL
        url_parts = url.split('?')
        if len(url_parts) == 2:
            token_param, *param_pairs = url_parts[1].split('&')
            token_key, token_value = token_param.split('=')

            # Check if the authentication token is valid
            if token_value in valid_auth_tokens:
                if request_type == "GET":
                    # For GET requests, validate and parse parameters
                    valid_params = validate_and_parse_params(param_pairs)
                    response_str = f"VALID,{valid_params}" if valid_params else "VALID"
                elif request_type == "POST":
                    # For POST requests, validate CSRF token and parse parameters
                    csrf_param = next((pair for pair in param_pairs if pair.startswith("csrf=")), None)
                    csrf_value = csrf_param.split('=')[1] if csrf_param else None

                    if csrf_value and len(csrf_value) >= 8 and csrf_value.isalnum():
                        valid_params = validate_and_parse_params(param_pairs)
                        response_str = f"VALID,{valid_params}" if valid_params else "VALID"
                    else:
                        response_str = "INVALID"
                else:
                    response_str = "INVALID"
            else:
                response_str = "INVALID"
        else:
            response_str = "INVALID"

        responses.append(response_str)

    return responses

def validate_and_parse_params(param_pairs):
    valid_params = []
    for pair in param_pairs:
        key, value = pair.split('=')
        valid_params.extend([key, value])
    return ','.join(valid_params)

# Example usage
valid_auth_tokens = ["ah37j2ha483u", "safh34ywb0p5", "ba34wyi8t902"]
requests = [
    ["GET", "https://example.com/?token=347sd6yk8iu2&name=alex"],
    ["GET", "https://example.com/?token=safh34ywb0p5&name=sam"],
    ["POST", "https://example.com/?token=safh34ywb0p5&name=alex"],
    ["POST", "https://example.com/?token=safh34ywb0p5&csrf=ak2sh32dy&name=chris"],
]

responses = getResponses(valid_auth_tokens, requests)
print(responses)
