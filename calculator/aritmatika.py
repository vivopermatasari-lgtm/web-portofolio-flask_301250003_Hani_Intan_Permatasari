def hitung_aritmatika(form):
    # Simple dummy: just echo the input expression
    expr = form.get('expression', '')
    try:
        # Evaluate safely? We'll just compute if simple
        result = eval(expr, {"__builtins__": {}}, {})
    except Exception:
        result = "Error"
    return {
        'rumus': f"{expr} = {result}",
        'hasil': result
    }
