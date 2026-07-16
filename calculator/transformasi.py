def hitung_transformasi(form):
    # Dummy transformation: just echo input
    value = form.get('value', '')
    return {
        'rumus': f'Input: {value}',
        'hasil': value,
        'ringkasan': f'Transformasi applied to {value}'
    }
