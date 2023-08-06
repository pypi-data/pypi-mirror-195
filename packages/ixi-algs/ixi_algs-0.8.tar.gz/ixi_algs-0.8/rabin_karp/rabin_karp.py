def rabin_karp(text, pattern):
    """
    Поиск всех вхождений алгоритмом Рабина-Карпа
    Параметры:
    ----------
        text: str
            текст
        pattern: str
            образец
    Возвращаемое значение
    ---------------------
        список позиций в тексте, с которых начинаются вхождения образца
    """
    d = 256
    mod_num = 11
    text_len = len(text)
    pattern_len = len(pattern)
    h = pow(d, pattern_len - 1) % mod_num
    multiplier_pattern = 0
    multiplier_text = 0
    result = []
    if text_len == 0:
        return result

    if pattern_len == 0:
        return list(range(text_len))

    for i in range(pattern_len):
        multiplier_pattern = (d * multiplier_pattern + ord(pattern[i])) % mod_num
        multiplier_text = (d * multiplier_text + ord(text[i])) % mod_num

    for s in range(text_len - pattern_len + 1):
        if multiplier_pattern == multiplier_text:
            match = True
            for i in range(pattern_len):
                if pattern[i] != text[s+i]:
                    match = False
                    break
            if match:
                result = result + [s]

        if s < text_len - pattern_len:
            multiplier_text = (multiplier_text - h * ord(text[s])) % mod_num
            multiplier_text = (multiplier_text * d + ord(text[s + pattern_len])) % mod_num
            multiplier_text = (multiplier_text + mod_num) % mod_num
    return result