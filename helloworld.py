(
    (lambda msg:
        (lambda key:
            (lambda encode:
                (lambda decode:
                    (lambda get_print:
                        get_print()(decode(encode(msg)))
                    )(
                        lambda: __builtins__.__dict__["print"]
                    )
                )(
                    lambda s: "".join(chr(ord(c) ^ key) for c in s)
                )
            )(
                lambda s: "".join(chr(ord(c) ^ key) for c in s)
            )
        )(42)
    )("Hello, World!")
)
