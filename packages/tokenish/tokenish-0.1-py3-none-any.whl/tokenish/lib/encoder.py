import base64
import re

SUPPORTED_ENCODING = ["base64"]


def encode_expressions(expressions, encoding):
    return list(map(lambda expression: encode_expression(expression, encoding), expressions))


def encode_expression(expression, encoding):
    if ("&ENC[" in expression and "]ODE&" not in expression) or \
            ("&ENC[" not in expression and "]ODE&" in expression):
        raise ValueError(
            "invalid encoding pattern: both \"&ENC[\" and \"]ODE&\" expected to encode specific part "
            "or nothing to encode all expression."
            "\"Hello &ENC[World]ODE&\" will encode \"World\", \"Hello World\" will encode \"Hello World\".")
    if "&ENC[" in expression and "]ODE&" in expression:
        match = re.search("&ENC\[(.*?)]ODE&", expression).group(1)
        encoded_match = apply_encoding(match, encoding)
        return expression.replace("&ENC[{}]ODE&".format(match), encoded_match)
    else:
        return apply_encoding(expression, encoding)


def apply_encoding(expression, encoding):
    if encoding.lower() not in SUPPORTED_ENCODING:
        raise ValueError("unsupported {} encoding: available {}".format(encoding, SUPPORTED_ENCODING))
    if encoding.lower() == "base64":
        return encode_base64(expression)


def encode_base64(expression):
    expression_bytes = expression.encode("utf-8")
    base64_bytes = base64.b64encode(expression_bytes)
    base64_expression = base64_bytes.decode("utf-8")
    return base64_expression
