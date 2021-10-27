if __name__ == '__main__':
    print('hello world!!')
    while (1):
        try:
            s = input('>>>')
            print('you input', s)
            assert s != '123'
        except:
            import traceback

            traceback.print_exc()
            pass
