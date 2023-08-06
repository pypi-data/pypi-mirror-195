import lib_dzne_seq
import lib_dzne_data

def main(*, seq, sub_region_table, alignment_table):
    infos = [
        (sub_region_table, 'start', 'end'),
        (alignment_table, 'from', 'to'),
    ]
    previous_end = 0
    ans = dict()
    regions = list()
    for y in range(1, 4):
        for x in ('fr', 'cdr'):
            regions.append(f"{x}{y}")
    for reg in regions:
        for table, a, b in infos:
            if lib_dzne_data.isna(table):
                continue
            start = None
            end = None
            for index, (row,) in table.items():
                if index.startswith(reg):
                    start = row.get(a)
                    end = row.get(b)
                    break
            if lib_dzne_data.isna(start, end):
                continue
            ans[reg] = dict()
            if not (previous_end <= start - 1 <= end):
                raise ValueError()
            previous_end = end
            if lib_dzne_data.isna(seq):
                continue
            ans[reg] = lib_dzne_seq.data(
                seq=seq,
                go=start-1,
                end=end,
            )
            break
    return ans



 
