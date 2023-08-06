from nodeset_parser import Transformer, Lark_StandAlone
from vfio_isolate.nodeset import NodeSetParser


class LarkTransformer(Transformer):

    def list_form(self, children):
        union = set()
        for item in children:
            union = union.union(item)
        return union

    def list_entry(self, children):
        v = children[0]
        if isinstance(v, str):
            return {int(v)}
        elif isinstance(v, range):
            return set(v)
        else:
            raise Exception("don't know how to handle")


    def mask_form(self, children):
        inputs = []
        for item in children:
            inputs.insert(0, int(item.value, 16))
        bit = 0
        result = set()
        for input in inputs:
            for n in range(32):
                if input & 1:
                    result.add(bit)
                input = input >> 1
                bit = bit + 1
        return result

    def range(self, children):
        return range(int(children[0].value), int(children[1].value) + 1)


if __name__ == '__main__':
    parse = NodeSetParser.parse("ff000fff,00001111")
    print(parse)


