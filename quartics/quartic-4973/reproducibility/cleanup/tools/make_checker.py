"""Embed independent elimination rules in the exact released full checker."""
import argparse
import hashlib
from pathlib import Path

BASE_SHA256 = 'd2079177a4960740c5b7d42fbd0756dfc4ce8953cc947cee91c8786ba26fa8ba'


def main():
    assert __debug__, 'Assertions must remain enabled.'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert hashlib.sha256(args.base.read_bytes()).hexdigest() == BASE_SHA256
    source = args.base.read_text()
    marker = 'def verify(root,write_report=True):'
    assert source.count(marker) == 1
    embed = ''
    for filename, namespace, exports in [
            ('check_relation_eliminate.py', '_relation_rules', ['relation_eliminate_expected']),
            ('check_localized.py', '_localized_rules', ['expected', 'relation_expected'])]:
        rule = (Path(__file__).parent/filename).read_text().split("if __name__ == '__main__':", 1)[0]
        embed += namespace + " = {'__name__': 'independent_elimination_rule'}\n"
        embed += 'exec(' + repr(rule) + ', ' + namespace + ')\n'
        for function in exports:
            exported = 'localized_expected' if function == 'expected' else function
            embed += exported + ' = ' + namespace + '[' + repr(function) + ']\n'
    source = source.replace(marker, embed + '\n' + marker, 1)
    marker = "            elif kind=='unit_scale':"
    assert source.count(marker) == 1
    dispatch = ("            elif kind=='relation_eliminate':\n"
                "                expected=relation_eliminate_expected(rows,d,nextvar,incidence)\n"
                "            elif kind=='localized_eliminate':\n"
                "                expected=localized_expected(rows,d,nextvar,incidence,event['patches'])\n"
                "            elif kind=='localized_relation':\n"
                "                expected=relation_expected(rows,d,nextvar,incidence,event['patches'])\n")
    assert "patch(event['patches'],expected)" in source
    source = source.replace(marker, dispatch + marker, 1)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(source, encoding='utf-8', newline='\n')
    print(hashlib.sha256(args.output.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
