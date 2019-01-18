import execjs

def get_token_from_file(filepath, fun, *args):
    def get_js():
        codejs = ''
        try:
            f = open(filepath, 'rb')
            line = f.readline()
            while line:
                codejs = codejs + line.decode("utf-8")
                line = f.readline()
        except Exception as ex:
            raise ex

        return codejs
    codejs = get_js()
    ctx = execjs.compile(codejs)
    info = ctx.call(fun, *args)
    return info



def get_token_from_code(code_info,fun, *args):
    ctx = execjs.compile(code_info)
    info = ctx.call(fun, *args)
    return info