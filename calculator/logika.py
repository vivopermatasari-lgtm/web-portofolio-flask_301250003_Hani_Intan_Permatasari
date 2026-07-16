def hitung_logika(form):
    # Expect inputs like a, b, operator
    a = form.get('a', '0') == '1' or form.get('a', '').lower() == 'true'
    b = form.get('b', '0') == '1' or form.get('b', '').lower() == 'true'
    op = form.get('operator', 'AND')
    if op == 'AND':
        res = a and b
    elif op == 'OR':
        res = a or b
    elif op == 'NOT':
        res = not a
    else:
        res = False
    return {
        'rumus': f"{a} {op} {b} = {res}" if op != 'NOT' else f"{op} {a} = {res}",
        'hasil': res
    }
