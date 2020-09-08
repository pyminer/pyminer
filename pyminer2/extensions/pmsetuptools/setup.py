import sys

if len(sys.argv)<2:
    pass
elif sys.argv[1] == 'init':
    if len(sys.argv) == 3 and sys.argv[2] == '--en':
        from init_extension import init_extension
    else:
        from init_extension_cn import init_extension

    init_extension()
    sys.exit(0)

print(
    'Command list:\n'
    '  init --en|cn\n'
    '  pack'
)
sys.exit(1)