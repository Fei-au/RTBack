
def string_to_float_decimal(s):
    # try:
        frm = '{price:.2f}'
        fv = None
        print('s', s)
        if isinstance(s, float) or isinstance(s,int):
            fv = s
        if isinstance(s,str):
            fv = float(s)
        print('fv', fv)
        result = frm.format(price=fv)
        print('result', result)
        return float(result)
    # except:
    #     print('string_to_float_decimal error')
    #     return None

